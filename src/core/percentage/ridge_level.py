"""Ridge level from value: L(x) = log2(|x|)."""
from .log2 import log2


def ridge_level(x: float | int) -> float:
    return float("-inf") if x == float("-inf") else log2(abs(float(x)))