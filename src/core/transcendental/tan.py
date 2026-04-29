"""tan — tangent via sin/cos."""

from .sin import sin
from .cos import cos
from ..constants.constants import OMEGA


def tan(x: float) -> float:
    """Return tan(x) = sin(x) / cos(x)."""
    cos_value = cos(x)
    if cos_value == 0.0:
        return OMEGA
    return sin(x) / cos_value
