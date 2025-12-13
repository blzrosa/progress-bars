from typing import Iterator

from src.colors.types.numeric import Float01

from .types.color_with_bg import ColorWithBackground
from .types.colors import sRGB


class Pallete:
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

    def __len__(self) -> int:
        return len(self.color_positions)

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
        dist0 = abs(pos0 - t)
        dist1 = abs(pos1 - t)
        return color0 if dist0 < dist1 else color1


class PalleteGenerator:
    def __init__(
        self,
        count: int,
        *colors: ColorWithBackground,
        repeat: bool = False,
    ) -> None:
        if count <= 0:
            raise ValueError("count must be >= 1")
        self._count = count
        self._pallete = Pallete(*colors)
        self.repeat = repeat

    def __len__(self) -> int:
        return self._count

    def __iter__(self) -> Iterator[ColorWithBackground]:
        if self._count == 1:
            yield self._pallete.get_color_at(0.0)
            return
        if not self.repeat:
            for i in range(self._count):
                t = i / (self._count - 1)
                yield self._pallete.get_color_at(t)
        else:
            for i in range(self._count):
                yield self._pallete.color_positions[i % len(self._pallete)][1]


if __name__ == "__main__":
    red_on_black = ColorWithBackground(sRGB(255, 0, 0), sRGB(0, 0, 0))
    green_on_white = ColorWithBackground(sRGB(0, 255, 0), sRGB(255, 255, 255))
    gradient = Pallete(red_on_black, green_on_white)

    for i, color in enumerate(PalleteGenerator(10, red_on_black, green_on_white)):
        print(f"\033[{color}m{'█' * 40} t={i:.1f} \033[0m")

    print("\n")

    for i, color in enumerate(
        PalleteGenerator(10, red_on_black, green_on_white, repeat=True)
    ):
        print(f"\033[{color}m{'█' * 40} t={i:.1f} \033[0m")
