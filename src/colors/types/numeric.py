from typing import Annotated

Uint8 = Annotated[int, "[0, 255]"]

Float01 = Annotated[float, "[0.0, 1.0]"]
Float360 = Annotated[float, "[0.0, 360.0]"]
Float8 = Annotated[float, "[-128.0, 127.0]"]
Float100 = Annotated[float, "[0.0, 100.0]"]

FloatOklab = Annotated[float, "[-0.4, 0.4]"]
FloatOklch = Annotated[float, "[0.0, 0.4]"]

Xd65 = Annotated[float, "[0.0, 95.047]"]
Zd65 = Annotated[float, "[0.0, 108.883]"]
Xd50 = Annotated[float, "[0.0, 96.6797]"]
Zd50 = Annotated[float, "[0.0, 82.5188]"]
