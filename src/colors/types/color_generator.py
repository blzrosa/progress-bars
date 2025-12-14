from abc import ABC, abstractmethod
from typing import Generic, Iterator

from .color import ColorType


class ColorGenerator(ABC, Generic[ColorType]):
    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterator[ColorType]:
        raise NotImplementedError
