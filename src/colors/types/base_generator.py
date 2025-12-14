from abc import ABC, abstractmethod
from typing import Iterator

from .color_with_bg import ColorWithBackground


class BaseGenerator(ABC):
    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterator[ColorWithBackground]:
        raise NotImplementedError
