from time import sleep, time
from typing import Iterator, Optional

from src.colors.gradient import Gradient, GradientGenerator
from src.colors.static_color import StaticColorGenerator
from src.colors.types import ColorGenerator, color
from src.colors.types.color_spaces import sRGB

from .bar_backend import BarBackend

WHITE_BLACK_BG = color(sRGB(255, 255, 255), sRGB(0, 0, 0))
DEFAULT_WHITE_BAR = StaticColorGenerator(50, WHITE_BLACK_BG)


class FastBar:
    def __init__(
        self,
        iterations: int,
        generator: ColorGenerator = DEFAULT_WHITE_BAR,
        update_every: Optional[int] = 1,
    ) -> None:
        self.backend = BarBackend(iterations, generator)
        self.update_every = update_every
        self.last_stats = "0.0it/s | ETA ?:??"
        self.frame_count = 0
        self.start_time = self.last_time = time()

    def __len__(self) -> int:
        return self.backend.iterations

    def __iter__(self) -> Iterator[str]:
        if self.update_every is not None:
            for i, base_bar in enumerate(self.backend):
                self.frame_count += 1

                if (
                    self.frame_count % self.update_every == 0
                    or i == self.backend.iterations
                ):
                    now = time()
                    elapsed = now - self.last_time
                    if elapsed > 0:
                        speed = self.update_every / elapsed
                        remaining = self.backend.iterations - i
                        eta = remaining / speed if speed > 0 else float("inf")
                        eta_str = f"{eta:.0f}s" if eta < 999 else "∞"
                        self.last_stats = f"{speed:.1f}it/s | ETA {eta_str}"

                    self.last_time = now

                yield f"{base_bar} | {self.last_stats}"
        else:
            yield from self.backend


if __name__ == "__main__":
    red_on_black = color(sRGB(255, 0, 0), sRGB(0, 0, 0))
    green_on_white = color(sRGB(0, 255, 0), sRGB(255, 255, 255))
    red_green_gradient = GradientGenerator(25, Gradient(red_on_black, green_on_white))
    bar = FastBar(1000, red_green_gradient)
    bar_no_speed = FastBar(1000, red_green_gradient, update_every=None)

    for bar_str in bar:
        print(f"\r\033[2K{bar_str}", end="", flush=True)
        sleep(0.0002)

    for bar_str in bar_no_speed:
        print(f"\r\033[2K{bar_str}", end="", flush=True)
        sleep(0.0002)

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
            pass
    b = time()
    normal_print_time = b - a
    print()
    print(f"Custom bar time: {custom_bar_time:.6f}s")
    print(f"Custom bar (no speed) time: {custom_bar_no_speed_time:.6f}s")
    print(f"Normal print time: {normal_print_time:.6f}s")
