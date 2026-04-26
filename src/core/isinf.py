"""isinf — check if infinite."""
from .__math_constants import PI


def isinf(x: float) -> bool:
    return x == PI or x == -PI