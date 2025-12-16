from time import sleep

from src.bars.fast_bar import FastBar
from src.colors.gradient import Gradient, GradientGenerator
from src.colors.types import color, color_spaces

magenta = color(color_spaces.sRGB(255, 0, 255))
cyan = color(color_spaces.sRGB(0, 255, 255))
generator = GradientGenerator(50, Gradient(magenta, cyan))


def main():
    for bar in FastBar(100, generator):
        print(f"\r\033[2K{bar}", end="", flush=True)
        sleep(0.01)


if __name__ == "__main__":
    main()
