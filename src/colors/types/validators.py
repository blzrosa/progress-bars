from .exceptions import DefaultChannelOutOfBounds
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


def validate_uint8(name: str, value: Uint8) -> None:
    if not (0 <= value <= 255):
        raise DefaultChannelOutOfBounds(name, value, (0, 255))


def validate_float01(name: str, value: Float01) -> None:
    if not (0.0 <= value <= 1.0):
        raise DefaultChannelOutOfBounds(name, value, (0.0, 1.0))


def validate_float360(name: str, value: Float360) -> None:
    if not (0.0 <= value <= 360.0):
        raise DefaultChannelOutOfBounds(name, value, (0.0, 360.0))


def validate_float100(name: str, value: Float100) -> None:
    if not (0.0 <= value <= 100.0):
        raise DefaultChannelOutOfBounds(name, value, (0.0, 100.0))


def validate_float8(name: str, value: Float8) -> None:
    if not (-128.0 <= value <= 127.0):
        raise DefaultChannelOutOfBounds(name, value, (-128.0, 127.0))


def validate_float_oklab(name: str, value: FloatOklab) -> None:
    if not (-0.4 <= value <= 0.4):
        raise DefaultChannelOutOfBounds(name, value, (-0.4, 0.4))


def validate_float_oklch(name: str, value: FloatOklch) -> None:
    if not (-0.4 <= value <= 0.4):
        raise DefaultChannelOutOfBounds(name, value, (-0.4, 0.4))


def validate_Xd65(name: str, value: Xd65) -> None:
    if not (0.0 <= value <= 95.047):
        raise DefaultChannelOutOfBounds(name, value, (0.0, 95.047))


def validate_Zd65(name: str, value: Zd65) -> None:
    if not (0.0 <= value <= 108.883):
        raise DefaultChannelOutOfBounds(name, value, (0.0, 108.883))


def validate_Xd50(name: str, value: Xd50) -> None:
    if not (0.0 <= value <= 96.6797):
        raise DefaultChannelOutOfBounds(name, value, (0.0, 96.6797))


def validate_Zd50(name: str, value: Zd50) -> None:
    if not (0.0 <= value <= 82.5188):
        raise DefaultChannelOutOfBounds(name, value, (0.0, 82.5188))
