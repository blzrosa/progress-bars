from typing import Iterator

from .types import BaseGenerator, ColorWithBackground
from .types.colors import sRGB


class ColorGenerator(BaseGenerator):
    def __init__(
        self,
        count: int,
        color: ColorWithBackground,
    ) -> None:
        if count <= 0:
            raise ValueError("count must be >= 1")
        self._count = count
        self._color = color

    def __len__(self) -> int:
        return self._count

    def __iter__(self) -> Iterator[ColorWithBackground]:
        for _ in range(self._count):
            yield self._color


if __name__ == "__main__":
    red_on_black = ColorWithBackground(sRGB(255, 0, 0), sRGB(0, 0, 0))
    green_on_white = ColorWithBackground(sRGB(0, 255, 0), sRGB(255, 255, 255))

    for i, color in enumerate(ColorGenerator(10, red_on_black)):
        print(f"\033[{color}m{'█' * 40} t={i:.1f} \033[0m")
