from dataclasses import dataclass
from typing import Tuple

from src.colors.utils.gen_docstring import generate_colorclass_docstring

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
from .space import BaseColorSpace, DefaultChannelOutOfBounds


@dataclass
class sRGB(BaseColorSpace):
    red: Uint8
    green: Uint8
    blue: Uint8
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_uint8("red", self.red)
        self._validate_uint8("green", self.green)
        self._validate_uint8("blue", self.blue)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        return (self.red, self.green, self.blue)


@dataclass
class HSV(BaseColorSpace):
    hue: Float360
    saturation: Float01
    value: Float01
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_float360("hue", self.hue)
        self._validate_float01("saturation", self.saturation)
        self._validate_float01("value", self.value)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class HSL(BaseColorSpace):
    hue: Float360
    saturation: Float01
    lightness: Float01
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_float360("hue", self.hue)
        self._validate_float01("saturation", self.saturation)
        self._validate_float01("lightness", self.lightness)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class HWB(BaseColorSpace):
    hue: Float360
    whiteness: Float01
    blackness: Float01
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_float360("hue", self.hue)
        self._validate_float01("saturation", self.whiteness)
        self._validate_float01("lightness", self.blackness)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class DisplayP3(BaseColorSpace):
    red: Uint8
    green: Uint8
    blue: Uint8
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_uint8("red", self.red)
        self._validate_uint8("green", self.green)
        self._validate_uint8("blue", self.blue)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class Rec2020(BaseColorSpace):
    red: Uint8
    green: Uint8
    blue: Uint8
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_uint8("red", self.red)
        self._validate_uint8("green", self.green)
        self._validate_uint8("blue", self.blue)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class A98RGB(BaseColorSpace):
    red: Uint8
    green: Uint8
    blue: Uint8
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_uint8("red", self.red)
        self._validate_uint8("green", self.green)
        self._validate_uint8("blue", self.blue)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class ProPhotoRGB(BaseColorSpace):
    red: Uint8
    green: Uint8
    blue: Uint8
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_uint8("red", self.red)
        self._validate_uint8("green", self.green)
        self._validate_uint8("blue", self.blue)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class CIELAB(BaseColorSpace):
    lightness: Float100
    a_channel: Float8
    b_channel: Float8
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_float100("lightness", self.lightness)
        self._validate_float8("a_channel", self.a_channel)
        self._validate_float8("b_channel", self.b_channel)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class LCH(BaseColorSpace):
    lightness: Float100
    chroma: Float100
    hue: Float360
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_float100("lightness", self.lightness)
        self._validate_float100("chroma", self.chroma)
        self._validate_float360("hue", self.hue)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class Oklab(BaseColorSpace):
    lightness: Float100
    a_channel: FloatOklab
    b_channel: FloatOklab
    alpha: Float01 = 1.0

    def _validate_float_oklab(self, name: str, value: FloatOklab) -> None:
        if not (-0.4 <= value <= 0.4):
            raise DefaultChannelOutOfBounds(name, value, (-0.4, 0.4))

    def __post_init__(self) -> None:
        self._validate_float100("lightness", self.lightness)
        self._validate_float_oklab("a_channel", self.a_channel)
        self._validate_float_oklab("b_channel", self.b_channel)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class Oklch(BaseColorSpace):
    lightness: Float100
    chroma: FloatOklch
    hue: Float360
    alpha: Float01 = 1.0

    def _validate_float_oklch(self, name: str, value: FloatOklch) -> None:
        if not (-0.4 <= value <= 0.4):
            raise DefaultChannelOutOfBounds(name, value, (-0.4, 0.4))

    def __post_init__(self) -> None:
        self._validate_float100("lightness", self.lightness)
        self._validate_float_oklch("chroma", self.chroma)
        self._validate_float360("hue", self.hue)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class XYZd65(BaseColorSpace):
    X: Xd65
    Y: Float100
    Z: Zd65
    alpha: Float01 = 1.0

    def _validate_Xd65(self, name: str, value: Xd65) -> None:
        if not (0.0 <= value <= 95.047):
            raise DefaultChannelOutOfBounds(name, value, (0.0, 95.047))

    def _validate_Zd65(self, name: str, value: Zd65) -> None:
        if not (0.0 <= value <= 108.883):
            raise DefaultChannelOutOfBounds(name, value, (0.0, 108.883))

    def __post_init__(self) -> None:
        self._validate_float100("X", self.X)
        self._validate_Xd65("Y", self.Y)
        self._validate_float360("Z", self.Z)
        self._validate_Zd65("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class XYZd50(BaseColorSpace):
    X: Xd50
    Y: Float100
    Z: Zd50
    alpha: Float01 = 1.0

    def _validate_Xd50(self, name: str, value: Xd50) -> None:
        if not (0.0 <= value <= 96.6797):
            raise DefaultChannelOutOfBounds(name, value, (0.0, 96.6797))

    def _validate_Zd50(self, name: str, value: Zd50) -> None:
        if not (0.0 <= value <= 82.5188):
            raise DefaultChannelOutOfBounds(name, value, (0.0, 82.5188))

    def __post_init__(self) -> None:
        self._validate_float100("X", self.X)
        self._validate_Xd50("Y", self.Y)
        self._validate_float360("Z", self.Z)
        self._validate_Zd50("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class sRGBLinear(BaseColorSpace):
    red: Float01
    green: Float01
    blue: Float01
    alpha: Float01 = 1.0

    def __post_init__(self) -> None:
        self._validate_float01("red", self.red)
        self._validate_float01("green", self.green)
        self._validate_float01("blue", self.blue)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


@dataclass
class CMYK(BaseColorSpace):
    cyan: Float01
    magenta: Float01
    yellow: Float01
    black: Float01
    alpha: Float01

    def __post_init__(self) -> None:
        self._validate_float01("cyan", self.cyan)
        self._validate_float01("magenta", self.magenta)
        self._validate_float01("yellow", self.yellow)
        self._validate_float01("black", self.black)
        self._validate_float01("alpha", self.alpha)

    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError


def main() -> None:
    print(generate_colorclass_docstring(sRGB))


if __name__ == "__main__":
    main()
