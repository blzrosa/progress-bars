from time import sleep
from typing import Iterator

from src.colors.gradient import ColorWithBackground, GradientGenerator
from src.colors.types.colors import sRGB
from src.colors.types.numeric import Float01


class BarBackend:
    def __init__(
        self,
        iterations: int,
        size: int = 25,
        *colors: ColorWithBackground,
        positions: list[Float01] | None = None,
    ) -> None:
        if iterations <= 0:
            raise ValueError("iterations must be >= 1")
        self.iterations: int = iterations
        if size <= 0:
            raise ValueError("size must be >= 1")
        self.size: int = size

        self.gradient_colors: list[ColorWithBackground] = list(
            GradientGenerator(size, *colors, positions=positions)
        )

        self.colored_blocks: list[str] = [
            f"\033[{color}m█" for color in self.gradient_colors
        ]

        # Unfilled style
        self.unfilled_char = " "
        self.unfilled_block = "\033[38;2;90;90;90m" + self.unfilled_char

        self._cached_filled: int = -1
        self._cached_visual: str = ""
        self._total_str = "/" + str(self.iterations)
        self._percentage_text = " (  0.00%)"
        self._ratio = 0.0

    def _build_visual(self, filled: int) -> str:
        if filled <= 0:
            return self.unfilled_block * self.size + "\033[0m"
        if filled >= self.size:
            return "".join(self.colored_blocks) + "\033[0m"

        revealed = "".join(self.colored_blocks[:filled])
        unfilled = self.unfilled_block * (self.size - filled)
        return revealed + "\033[0m" + unfilled + "\033[0m"

    def generate_bar(self, iteration: int) -> str:
        ratio = iteration / self.iterations if self.iterations > 0 else 1.0
        filled = min(int(ratio * self.size + 1e-9), self.size)

        if filled != self._cached_filled:
            self._cached_filled = filled
            self._cached_visual = self._build_visual(filled)

        if ratio - self._ratio > 0.001:
            self._percentage_text = " (%6.2f%%)" % (ratio * 100)

        iterations_text = f" {iteration}{self._total_str}"

        return self._cached_visual + iterations_text + self._percentage_text

    def __iter__(self) -> Iterator[str]:
        self._cached_filled = -1
        self._cached_visual = self._build_visual(0)

        for iteration in range(self.iterations + 1):
            yield self.generate_bar(iteration)


if __name__ == "__main__":
    red_on_black = ColorWithBackground(sRGB(255, 0, 0), sRGB(0, 0, 0))
    green_on_white = ColorWithBackground(sRGB(0, 255, 0), sRGB(255, 255, 255))
    bar_backend = BarBackend(100, 50, red_on_black, green_on_white)

    for bar in bar_backend:
        print(f"\r\033[2K{bar}", end="", flush=True)
        sleep(0.05)

    print()
