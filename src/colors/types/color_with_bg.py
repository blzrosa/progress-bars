from src.colors.types.colors import sRGB
from src.colors.types.space import BaseColorSpace


class ColorWithBackground:
    def __init__(self, foreground: BaseColorSpace, background: BaseColorSpace) -> None:
        self.foreground: sRGB = sRGB(*foreground.to_rgb())
        self.background: sRGB = sRGB(*background.to_rgb())

    def __str__(self) -> str:
        fg = str(self.foreground)
        bg = str(self.background)
        return f"38;{fg};48;{bg}"

    def interpolate(
        self, other: "ColorWithBackground", ratio: float
    ) -> "ColorWithBackground":
        new_foreground: sRGB = sRGB(
            *(
                int(left * (1 - ratio) + right * ratio)
                for left, right in zip(
                    self.foreground.to_rgb(), other.foreground.to_rgb(), strict=True
                )
            )
        )
        new_background: sRGB = sRGB(
            *(
                int(left * (1 - ratio) + right * ratio)
                for left, right in zip(
                    self.background.to_rgb(), other.background.to_rgb(), strict=True
                )
            )
        )
        return ColorWithBackground(new_foreground, new_background)
