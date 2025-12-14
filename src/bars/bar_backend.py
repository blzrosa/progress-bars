from time import sleep
from typing import Iterator, Literal

from src.colors.color import ColorGenerator
from src.colors.gradient import GradientGenerator
from src.colors.pallete import PalleteGenerator
from src.colors.types import BaseGenerator, ColorWithBackground
from src.colors.types.colors import sRGB


# TODO: Implement partial rendering in bar
def partial_block(eights: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8] = 8) -> str:
    match eights:
        case 0:
            return " "
        case 1:
            return "▏"
        case 2:
            return "▎"
        case 3:
            return "▍"
        case 4:
            return "▌"
        case 5:
            return "▋"
        case 6:
            return "▊"
        case 7:
            return "▉"
        case 8:
            return "█"


class BarBackend:
    def __init__(
        self,
        iterations: int,
        generator: BaseGenerator,
    ) -> None:
        if iterations <= 0:
            raise ValueError("iterations must be >= 1")
        self.iterations: int = iterations
        if len(generator) <= 0:
            raise ValueError("size must be >= 1")
        self.size: int = len(generator)

        self.gradient_colors: list[ColorWithBackground] = list(generator)

        self.colored_blocks: list[str] = [
            f"\033[{color}m█" for color in self.gradient_colors
        ]

        # Unfilled style
        self.unfilled_char = " "
        self.unfilled_block = "\033[38;2;90;90;90m" + self.unfilled_char

        self._cached_filled: int = -1
        self._cached_visual: str = ""
        self._total_str = "/" + str(self.iterations)
        self._total_str_size = len(str(self.iterations))
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

        iterations_text = f" {iteration:{self._total_str_size}}{self._total_str}"

        return self._cached_visual + iterations_text + self._percentage_text

    def __iter__(self) -> Iterator[str]:
        self._cached_filled = -1
        self._cached_visual = self._build_visual(0)

        for iteration in range(self.iterations + 1):
            yield self.generate_bar(iteration)


if __name__ == "__main__":
    color_black = sRGB(0, 0, 0)
    light_blue = ColorWithBackground(sRGB(91, 206, 250), color_black)
    pink = ColorWithBackground(sRGB(245, 169, 184), color_black)
    white = ColorWithBackground(sRGB(255, 255, 255), color_black)
    red_on_black = ColorWithBackground(sRGB(255, 0, 0), sRGB(0, 0, 0))
    green_on_white = ColorWithBackground(sRGB(0, 255, 0), sRGB(255, 255, 255))

    bars = [
        BarBackend(100, GradientGenerator(50, red_on_black, green_on_white)),
        BarBackend(100, ColorGenerator(50, white)),
        BarBackend(
            100, PalleteGenerator(50, light_blue, pink, white, pink, light_blue)
        ),
        BarBackend(
            100,
            PalleteGenerator(50, red_on_black, green_on_white, light_blue, repeat=True),
        ),
    ]

    for backend in bars:
        for bar in backend:
            print(f"\r\033[2K{bar}", end="", flush=True)
            sleep(0.01)
        print()

    print()
