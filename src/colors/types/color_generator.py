from abc import ABC, abstractmethod
from typing import Generic, Iterator

from .color import ColorType, ColorWithoutBackground


class ColorGenerator(ABC, Generic[ColorType]):
    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterator[ColorType]:
        raise NotImplementedError

    def no_background(self) -> "ColorGenerator[ColorWithoutBackground]":
        """
        Return a new ColorGenerator that yields only the foreground
        of each color as a ColorWithoutBackground instance.
        """
        return ForegroundOnlyGenerator(self)


class ForegroundOnlyGenerator(ColorGenerator[ColorWithoutBackground]):
    def __init__(self, generator: ColorGenerator) -> None:
        self._generator = generator

    def __len__(self) -> int:
        return len(self._generator)  # delegate to original

    def __iter__(self) -> Iterator[ColorWithoutBackground]:
        for color in self._generator:
            # Extract foreground and wrap as ColorWithoutBackground
            yield ColorWithoutBackground(color.foreground)
