from typing import Any, Tuple


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
