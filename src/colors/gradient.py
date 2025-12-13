from typing import Iterator

from src.colors.types.numeric import Float01

from .types.colors import sRGB
from .types.space import BaseColorSpace


class ColorWithBackground:
    def __init__(self, foreground: BaseColorSpace, background: BaseColorSpace) -> None:
        self.foreground: sRGB = sRGB(*foreground.to_rgb())
        self.background: sRGB = sRGB(*background.to_rgb())

    def __str__(self) -> str:
        fg = str(self.foreground)
        bg = str(self.background)
        return f"38;{fg};48;{bg}"

    def interpolate(
        self, other: "ColorWithBackground", ratio: float
    ) -> "ColorWithBackground":
        new_foreground: sRGB = sRGB(
            *(
                int(left * (1 - ratio) + right * ratio)
                for left, right in zip(
                    self.foreground.to_rgb(), other.foreground.to_rgb(), strict=True
                )
            )
        )
        new_background: sRGB = sRGB(
            *(
                int(left * (1 - ratio) + right * ratio)
                for left, right in zip(
                    self.background.to_rgb(), other.background.to_rgb(), strict=True
                )
            )
        )
        return ColorWithBackground(new_foreground, new_background)


class Gradient:
    def __init__(
        self,
        *colors: ColorWithBackground,
        positions: list[Float01] | None = None,
    ) -> None:
        if positions is None:
            _positions = [i / (len(colors) - 1) for i in range(len(colors))]
        else:
            if len(positions) != len(colors):
                raise ValueError("Length of positions must match length of colors")
            _positions = positions
        self.color_positions: list[tuple[float, ColorWithBackground]] = sorted(
            zip(_positions, colors, strict=True), key=lambda x: x[0]
        )

    def get_color_at(
        self,
        t: Float01,
    ) -> ColorWithBackground:
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


class GradientGenerator:
    def __init__(
        self,
        count: int,
        *colors: ColorWithBackground,
        positions: list[Float01] | None = None,
    ) -> None:
        if count <= 0:
            raise ValueError("count must be >= 1")
        self._count = count
        self._gradient = Gradient(*colors, positions=positions)

    def __len__(self) -> int:
        return self._count

    def __iter__(self) -> Iterator[ColorWithBackground]:
        if self._count == 1:
            yield self._gradient.get_color_at(0.0)
            return
        for i in range(self._count):
            t = i / (self._count - 1)
            yield self._gradient.get_color_at(t)


if __name__ == "__main__":
    red_on_black = ColorWithBackground(sRGB(255, 0, 0), sRGB(0, 0, 0))
    green_on_white = ColorWithBackground(sRGB(0, 255, 0), sRGB(255, 255, 255))
    gradient = Gradient(red_on_black, green_on_white)

    for i, color in enumerate(GradientGenerator(10, red_on_black, green_on_white)):
        print(f"\033[{color}m{'█' * 40} t={i:.1f} \033[0m")
