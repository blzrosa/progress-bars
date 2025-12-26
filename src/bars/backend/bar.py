from time import sleep
from typing import Generic

from src.colors.gradient import Gradient, GradientGenerator
from src.colors.pallete import Pallete, PalleteGenerator
from src.colors.static_color import StaticColorGenerator
from src.colors.types import Color, ColorType, color
from src.colors.types.color_spaces import sRGB


def clip01(n: float) -> float:
    return 0.0 if n < 0.0 else 1.0 if n > 1.0 else n


PARTIAL_BLOCKS = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]


class BarBackend(Generic[ColorType]):
    def __init__(
        self,
        colors: ColorType | Pallete | Gradient,
        size: int = 50,
        repeat_pallete: bool = False,
    ) -> None:
        if isinstance(colors, Pallete):
            generator = PalleteGenerator(size, colors, repeat_pallete)
        elif isinstance(colors, Gradient):
            generator = GradientGenerator(size, colors)
        else:
            generator = StaticColorGenerator(size, colors)

        if len(generator) <= 0:
            raise ValueError("size must be >= 1")
        self.size: int = len(generator)
        self.bins: int = 8 * self.size

        self.gradient_colors: list[Color] = list(generator.no_background())

        self.colored_blocks: list[str] = [
            f"\033[{color}m█" for color in self.gradient_colors
        ]

        # Unfilled style
        self.unfilled_char = "░"
        self.unfilled_block = "\033[38;2;90;90;90m" + self.unfilled_char

        self.bars = [self._build_visual(i) for i in range(self.bins + 1)]

    def _build_visual(self, filled: int) -> str:
        if filled <= 0:
            return self.unfilled_block * self.size + "\033[0m"
        if filled >= self.bins:
            return "".join(self.colored_blocks) + "\033[0m"

        actual_filed = filled // 8
        partial_eights = filled % 8

        revealed = "".join(self.colored_blocks[:actual_filed])

        if partial_eights > 0:
            partial = self.colored_blocks[actual_filed].replace(
                "█", PARTIAL_BLOCKS[partial_eights]
            )
            unfilled_count = self.size - actual_filed - 1
        else:
            partial = ""
            unfilled_count = self.size - actual_filed

        unfilled = self.unfilled_block * unfilled_count
        return revealed + partial + unfilled + "\033[0m"

    def __call__(self, progress: float) -> str:
        progress = clip01(progress)
        bins = int(self.bins * progress)
        return self.bars[bins]


if __name__ == "__main__":
    MAX_ITER = 100

    white = color(sRGB(255, 255, 255))
    black_on_white = color(sRGB(0, 0, 0), sRGB(255, 255, 255))
    red_on_black = color(sRGB(255, 0, 0), sRGB(0, 0, 0))
    green_on_white = color(sRGB(0, 255, 0), sRGB(255, 255, 255))

    bars = [
        BarBackend(Gradient(red_on_black, green_on_white)),
        BarBackend(white),
        BarBackend(Pallete(black_on_white, red_on_black, green_on_white)),
        BarBackend(
            Pallete(black_on_white, red_on_black, green_on_white), repeat_pallete=True
        ),
    ]

    for bar in bars:
        for i in range(0, MAX_ITER + 1):
            progress = i / MAX_ITER
            print(f"\r\033[2K{bar(progress)}", end="", flush=True)
            sleep(0.01)
    print()
