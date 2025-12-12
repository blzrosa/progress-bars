from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Tuple

from .numeric import Float01, Float8, Float100, Float360, Uint8


class OutOfBoundsException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DefaultChannelOutOfBounds(OutOfBoundsException):
    def __init__(
        self, channel: str, value: Any, ranges: Tuple[int | float, int | float]
    ) -> None:
        self.channel = channel
        self.value = value
        message = f"{value} is out of bounds for the {channel} channel."
        if isinstance(ranges[0], int):
            message += f"\nExpected range: [{ranges[0]}, {ranges[1]}]"
        else:
            message += f"\nExpected range: [{ranges[0]:.1f}, {ranges[1]:.1f}]"
        super().__init__(message)


@dataclass
class BaseColorSpace(ABC):
    def _validate_uint8(self, name: str, value: Uint8) -> None:
        if not (0 <= value <= 255):
            raise DefaultChannelOutOfBounds(name, value, (0, 255))

    def _validate_float01(self, name: str, value: Float01) -> None:
        if not (0.0 <= value <= 1.0):
            raise DefaultChannelOutOfBounds(name, value, (0.0, 1.0))

    def _validate_float360(self, name: str, value: Float360) -> None:
        if not (0.0 <= value <= 360.0):
            raise DefaultChannelOutOfBounds(name, value, (0.0, 360.0))

    def _validate_float100(self, name: str, value: Float100) -> None:
        if not (0.0 <= value <= 100.0):
            raise DefaultChannelOutOfBounds(name, value, (0.0, 100.0))

    def _validate_float8(self, name: str, value: Float8) -> None:
        if not (-128.0 <= value <= 127.0):
            raise DefaultChannelOutOfBounds(name, value, (-128.0, 127.0))

    @abstractmethod
    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError

    def __str__(self) -> str:
        """Ansii representation"""
        r, g, b = self.to_rgb()
        return f"2;{r};g;b"
