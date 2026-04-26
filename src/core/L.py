"""Spine function: L(x) = log2(|x|)."""
from .log2 import log2


def L(x: float | int) -> float:
    if x == 0:
        return float("-inf")
    return log2(abs(float(x)))