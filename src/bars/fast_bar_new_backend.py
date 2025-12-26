from time import sleep, time
from typing import Iterator, Optional

from src.colors.gradient import Gradient
from src.colors.pallete import Pallete
from src.colors.types import ColorType, color
from src.colors.types.color_spaces import sRGB

from .backend.bar import BarBackend

WHITE_BLACK_BG = color(sRGB(255, 255, 255), sRGB(0, 0, 0))


class FastBar:
    def __init__(
        self,
        iterations: int,
        colors: ColorType | Pallete | Gradient = WHITE_BLACK_BG,
        size: int = 50,
        repeat_pallete: bool = False,
        update_every: Optional[int] = 1,
    ) -> None:
        self.iterations = iterations
        self.bar = BarBackend(colors, size, repeat_pallete)
        self.update_every = update_every
        self.last_stats = "0.0it/s | ETA ?:??"
        self.frame_count = 0
        self.start_time = self.last_time = time()

    def __len__(self) -> int:
        return self.iterations

    def __iter__(self) -> Iterator[str]:
        if self.update_every is not None:
            for i in range(self.iterations + 1):
                self.frame_count += 1

                if self.frame_count % self.update_every == 0 or i == self.iterations:
                    now = time()
                    elapsed = now - self.last_time
                    if elapsed > 0:
                        speed = self.update_every / elapsed
                        remaining = self.iterations - i
                        eta = remaining / speed if speed > 0 else float("inf")
                        eta_str = f"{eta:.0f}s" if eta < 999 else "∞"
                        self.last_stats = f"{speed:.1f}it/s | ETA {eta_str}"

                    self.last_time = now

                yield f"{self.bar(i / self.iterations)} | {self.last_stats}"
        else:
            for i in range(self.iterations + 1):
                yield f"{self.bar(i / self.iterations)}"


if __name__ == "__main__":
    red_on_black = color(sRGB(255, 0, 0), sRGB(0, 0, 0))
    green_on_white = color(sRGB(0, 255, 0), sRGB(255, 255, 255))
    red_green_gradient = Gradient(red_on_black, green_on_white)
    bar = FastBar(1000, red_green_gradient)
    bar_no_speed = FastBar(1000, red_green_gradient, update_every=None)

    for bar_str in bar:
        print(f"\r\033[2K{bar_str}", end="", flush=True)
        sleep(0.001)

    for bar_str in bar_no_speed:
        print(f"\r\033[2K{bar_str}", end="", flush=True)
        sleep(0.001)

    a = time()
    for _ in range(100):
        for _ in bar:
            pass
    b = time()
    custom_bar_time = b - a

    a = time()
    for _ in range(100):
        for _ in bar_no_speed:
            pass
    b = time()
    custom_bar_no_speed_time = b - a

    a = time()
    for _ in range(100):
        for _ in range(1000):
            print("", end="")
            pass
    b = time()
    normal_print_time = b - a
    print()
    print(f"Custom bar time: {custom_bar_time:.6f}s")
    print(f"Custom bar (no speed) time: {custom_bar_no_speed_time:.6f}s")
    print(f"Normal print time: {normal_print_time:.6f}s")
