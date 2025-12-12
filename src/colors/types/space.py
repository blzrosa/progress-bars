from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from .numeric import Uint8


@dataclass
class BaseColorSpace(ABC):
    @abstractmethod
    def to_rgb(self) -> Tuple[Uint8, Uint8, Uint8]:
        raise NotImplementedError

    def __str__(self) -> str:
        """Ansii representation"""
        r, g, b = self.to_rgb()
        return f"2;{r};{g};{b}"
