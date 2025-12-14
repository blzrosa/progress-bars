from abc import abstractmethod
from typing import Optional, TypeVar, overload

from src.colors.types.color_space import ColorSpace
from src.colors.types.color_spaces import sRGB


class Color:
    foreground: sRGB
    background: Optional[sRGB]

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def interpolate(self, other: "Color", ratio: float) -> "Color":
        raise NotImplementedError


class ColorWithoutBackground(Color):
    def __init__(self, foreground: ColorSpace) -> None:
        self.foreground: sRGB = sRGB(*foreground.to_rgb())
        self.background = None

    def __str__(self) -> str:
        fg = str(self.foreground)
        return f"38;{fg}"

    def interpolate(self, other: Color, ratio: float) -> "ColorWithoutBackground":
        new_foreground: sRGB = sRGB(
            *(
                int(left * (1 - ratio) + right * ratio)
                for left, right in zip(
                    self.foreground.to_rgb(), other.foreground.to_rgb(), strict=True
                )
            )
        )
        return ColorWithoutBackground(new_foreground)


class ColorWithBackground(Color):
    def __init__(self, foreground: ColorSpace, background: ColorSpace) -> None:
        self.foreground: sRGB = sRGB(*foreground.to_rgb())
        self.background: sRGB = sRGB(*background.to_rgb())

    def __str__(self) -> str:
        fg = str(self.foreground)
        bg = str(self.background)
        return f"38;{fg};48;{bg}"

    def interpolate(self, other: Color, ratio: float) -> "ColorWithBackground":
        new_foreground: sRGB = sRGB(
            *(
                int(left * (1 - ratio) + right * ratio)
                for left, right in zip(
                    self.foreground.to_rgb(), other.foreground.to_rgb(), strict=True
                )
            )
        )
        new_background: sRGB = (
            sRGB(
                *(
                    int(left * (1 - ratio) + right * ratio)
                    for left, right in zip(
                        self.background.to_rgb(), other.background.to_rgb(), strict=True
                    )
                )
            )
            if other.background is not None
            else self.background
        )

        return ColorWithBackground(new_foreground, new_background)


ColorType = TypeVar("ColorType", ColorWithoutBackground, ColorWithBackground)


@overload
def color(foreground: ColorSpace) -> ColorWithoutBackground: ...
@overload
def color(foreground: ColorSpace, background: ColorSpace) -> ColorWithBackground: ...


def color(foreground: ColorSpace, background: Optional[ColorSpace] = None) -> Color:
    fg = sRGB.from_color(foreground)
    if background is None:
        return ColorWithoutBackground(fg)
    else:
        bg = sRGB.from_color(background)
        return ColorWithBackground(fg, bg)
