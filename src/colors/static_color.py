from typing import Generic, Iterator

from src.colors.types.color import ColorType, color

from .types import ColorGenerator
from .types.color_spaces import sRGB


class StaticColorGenerator(ColorGenerator, Generic[ColorType]):
    def __init__(
        self,
        count: int,
        color: ColorType,
    ) -> None:
        if count <= 0:
            raise ValueError("count must be >= 1")
        self._count = count
        self._color = color

    def __len__(self) -> int:
        return self._count

    def __iter__(self) -> Iterator[ColorType]:
        for _ in range(self._count):
            yield self._color


if __name__ == "__main__":
    red_on_black = color(sRGB(255, 0, 0), sRGB(0, 0, 0))
    green = color(sRGB(0, 255, 0))

    for i, color in enumerate(StaticColorGenerator(10, red_on_black)):
        print(f"\033[{color}m{'█' * 40} t={i:.1f} \033[0m")
