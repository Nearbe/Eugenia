"""cot — cotangent via cos/sin."""

from .sin import sin
from .cos import cos
from ..constants.constants import OMEGA


def cot(x: float) -> float:
    """Return cot(x) = cos(x) / sin(x)."""
    sin_value = sin(x)
    if sin_value == 0.0:
        return OMEGA
    return cos(x) / sin_value
