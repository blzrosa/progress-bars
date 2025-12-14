from typing import Tuple

from src.colors.utils.get_setter_decorator import channel_getter_setter

from .color_space import ColorSpace
from .numeric import (
    Float01,
    Float8,
    Float100,
    Float360,
    FloatOklab,
    FloatOklch,
    Uint8,
    Xd50,
    Xd65,
    Zd50,
    Zd65,
)
from .validators import (
    validate_float01,
    validate_float8,
    validate_float100,
    validate_float360,
    validate_float_oklab,
    validate_float_oklch,
    validate_uint8,
    validate_Xd50,
    validate_Xd65,
    validate_Zd50,
    validate_Zd65,
)


# ─────────────────────────────────────────────────────────────────────────────
# Color Implementations
# ─────────────────────────────────────────────────────────────────────────────
@channel_getter_setter("red", validate_uint8)
@channel_getter_setter("green", validate_uint8)
@channel_getter_setter("blue", validate_uint8)
@channel_getter_setter("alpha", validate_float01)
class sRGB(ColorSpace):
    def __init__(self, r: Uint8, g: Uint8, b: Uint8, a: Float01 = 1.0) -> None:
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    @classmethod
    def from_color(cls, color: ColorSpace) -> "sRGB":
        rgb = color.to_rgb()
        return cls(*rgb, color.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        return (self.red, self.green, self.blue)


@channel_getter_setter("hue", validate_float360)
@channel_getter_setter("saturation", validate_float01)
@channel_getter_setter("value", validate_float01)
@channel_getter_setter("alpha", validate_float01)
class HSV(ColorSpace):
    def __init__(self, h: Float360, s: Float01, v: Float01, a: Float01 = 1.0) -> None:
        self.hue = h
        self.saturation = s
        self.value = v
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("hue", validate_float360)
@channel_getter_setter("saturation", validate_float01)
@channel_getter_setter("lightness", validate_float01)
@channel_getter_setter("alpha", validate_float01)
class HSL(ColorSpace):
    def __init__(self, h: Float360, s: Float01, L: Float01, a: Float01 = 1.0) -> None:
        self.hue = h
        self.saturation = s
        self.lightness = L
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("hue", validate_float360)
@channel_getter_setter("whiteness", validate_float01)
@channel_getter_setter("blackness", validate_float01)
@channel_getter_setter("alpha", validate_float01)
class HWB(ColorSpace):
    def __init__(self, h: Float360, w: Float01, b: Float01, a: Float01 = 1.0) -> None:
        self.hue = h
        self.whiteness = w
        self.blackness = b
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("red", validate_uint8)
@channel_getter_setter("green", validate_uint8)
@channel_getter_setter("blue", validate_uint8)
@channel_getter_setter("alpha", validate_float01)
class DisplayP3(ColorSpace):
    def __init__(self, r: Uint8, g: Uint8, b: Uint8, a: Float01 = 1.0) -> None:
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("red", validate_uint8)
@channel_getter_setter("green", validate_uint8)
@channel_getter_setter("blue", validate_uint8)
@channel_getter_setter("alpha", validate_float01)
class Rec2020(ColorSpace):
    def __init__(self, r: Uint8, g: Uint8, b: Uint8, a: Float01 = 1.0) -> None:
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("red", validate_uint8)
@channel_getter_setter("green", validate_uint8)
@channel_getter_setter("blue", validate_uint8)
@channel_getter_setter("alpha", validate_float01)
class A98RGB(ColorSpace):
    def __init__(self, r: Uint8, g: Uint8, b: Uint8, a: Float01 = 1.0) -> None:
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("red", validate_uint8)
@channel_getter_setter("green", validate_uint8)
@channel_getter_setter("blue", validate_uint8)
@channel_getter_setter("alpha", validate_float01)
class ProPhotoRGB(ColorSpace):
    def __init__(self, r: Uint8, g: Uint8, b: Uint8, a: Float01 = 1.0) -> None:
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("lightness", validate_float100)
@channel_getter_setter("a_channel", validate_float8)
@channel_getter_setter("b_channel", validate_float8)
@channel_getter_setter("alpha", validate_float01)
class CIELAB(ColorSpace):
    def __init__(self, L: Float100, a: Float8, b: Float8, alpha: Float01 = 1.0) -> None:
        self.lightness = L
        self.a_channel = a
        self.b_channel = b
        self.alpha = alpha

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("lightness", validate_float100)
@channel_getter_setter("chroma", validate_float100)
@channel_getter_setter("hue", validate_float360)
@channel_getter_setter("alpha", validate_float01)
class LCH(ColorSpace):
    def __init__(self, L: Float100, c: Float100, h: Float360, a: Float01 = 1.0) -> None:
        self.lightness = L
        self.chroma = c
        self.hue = h
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("lightness", validate_float100)
@channel_getter_setter("a_channel", validate_float_oklab)
@channel_getter_setter("b_channel", validate_float_oklab)
@channel_getter_setter("alpha", validate_float01)
class Oklab(ColorSpace):
    def __init__(
        self, L: Float100, a: FloatOklab, b: FloatOklab, alpha: Float01 = 1.0
    ) -> None:
        self.lightness = L
        self.a_channel = a
        self.b_channel = b
        self.alpha = alpha

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("lightness", validate_float100)
@channel_getter_setter("chroma", validate_float_oklch)
@channel_getter_setter("hue", validate_float360)
@channel_getter_setter("alpha", validate_float01)
class Oklch(ColorSpace):
    def __init__(
        self, L: Float100, c: FloatOklch, h: Float360, a: Float01 = 1.0
    ) -> None:
        self.lightness = L
        self.chroma = c
        self.hue = h
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("X", validate_Xd65)
@channel_getter_setter("Y", validate_float100)
@channel_getter_setter("Z", validate_Zd65)
@channel_getter_setter("alpha", validate_float01)
class XYZd65(ColorSpace):
    def __init__(self, X: Xd65, Y: Float100, Z: Zd65, a: Float01 = 1.0) -> None:
        self.X = X
        self.Y = Y
        self.Z = Z
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("X", validate_Xd50)
@channel_getter_setter("Y", validate_float100)
@channel_getter_setter("Z", validate_Zd50)
@channel_getter_setter("alpha", validate_float01)
class XYZd50(ColorSpace):
    def __init__(self, X: Xd50, Y: Float100, Z: Zd50, a: Float01 = 1.0) -> None:
        self.X = X
        self.Y = Y
        self.Z = Z
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("red", validate_float01)
@channel_getter_setter("green", validate_float01)
@channel_getter_setter("blue", validate_float01)
@channel_getter_setter("alpha", validate_float01)
class sRGBLinear(ColorSpace):
    def __init__(self, r: Float01, g: Float01, b: Float01, a: Float01 = 1.0) -> None:
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@channel_getter_setter("cyan", validate_float01)
@channel_getter_setter("magenta", validate_float01)
@channel_getter_setter("yellow", validate_float01)
@channel_getter_setter("black", validate_float01, "k")
@channel_getter_setter("alpha", validate_float01)
class CMYK(ColorSpace):
    def __init__(
        self, c: Float01, m: Float01, y: Float01, k: Float01, a: Float01 = 1.0
    ) -> None:
        self.cyan = c
        self.magenta = m
        self.yellow = y
        self.black = k
        self.alpha = a

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError
