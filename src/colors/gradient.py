from typing import Generic, Iterator

from .types import (
    ColorGenerator,
    ColorType,
    ColorWithBackground,
    ColorWithoutBackground,
    Float01,
)
from .types.color_spaces import sRGB


class Gradient(Generic[ColorType]):
    def __init__(
        self,
        *colors: ColorType,
        positions: list[Float01] | None = None,
    ) -> None:
        if positions is None:
            _positions = [i / (len(colors) - 1) for i in range(len(colors))]
        else:
            if len(positions) != len(colors):
                raise ValueError("Length of positions must match length of colors")
            _positions = positions
        self.color_positions: list[tuple[float, ColorType]] = sorted(
            zip(_positions, colors, strict=True), key=lambda x: x[0]
        )

    def __len__(self) -> int:
        return len(self.color_positions)

    def get_color_at(
        self,
        t: Float01,
    ) -> ColorType:
        if len(self.color_positions) == 1:
            return self.color_positions[0][1]

        if t <= self.color_positions[0][0]:
            return self.color_positions[0][1]
        if t >= self.color_positions[-1][0]:
            return self.color_positions[-1][1]

        lo = 1
        hi = len(self.color_positions) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            pos_mid = self.color_positions[mid][0]
            if pos_mid < t:
                lo = mid + 1
            else:
                hi = mid - 1
        pos0, color0 = self.color_positions[lo - 1]
        pos1, color1 = self.color_positions[lo]
        if pos1 == pos0:
            return color1
        ratio = (t - pos0) / (pos1 - pos0)

        return color0.interpolate(color1, ratio)


class GradientGenerator(ColorGenerator, Generic[ColorType]):
    def __init__(
        self,
        count: int,
        gradient: Gradient[ColorType],
    ) -> None:
        if count <= 0:
            raise ValueError("count must be >= 1")
        self._count = count
        self._gradient = gradient

    def __len__(self) -> int:
        return self._count

    def __iter__(self) -> Iterator[ColorType]:
        if self._count == 1:
            yield self._gradient.get_color_at(0.0)
            return
        for i in range(self._count):
            t = i / (self._count - 1)
            yield self._gradient.get_color_at(t)


if __name__ == "__main__":
    red_on_black = ColorWithBackground(sRGB(255, 0, 0), sRGB(0, 0, 0))
    green_on_white = ColorWithBackground(sRGB(0, 255, 0), sRGB(255, 255, 255))
    gradient_with_bg = Gradient(red_on_black, green_on_white)
    red = ColorWithoutBackground(sRGB(255, 0, 0))
    green = ColorWithoutBackground(sRGB(0, 255, 0))
    gradient_no_bg = Gradient(red, green)

    for i, color in enumerate(GradientGenerator(10, gradient_with_bg)):
        print(f"\033[{color}m{'█' * 40} t={i:.1f} \033[0m")

    for i, color in enumerate(GradientGenerator(10, gradient_no_bg)):
        print(f"\033[{color}m{'█' * 40} t={i:.1f} \033[0m")
