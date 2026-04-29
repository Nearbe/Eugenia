"""sqrt — square root."""
from .isinf import isinf


def sqrt(x: float) -> float:
    if isinf(x):
        return float("inf")
    if x == 0:
        return 0.0
    if x < 0:
        return 0.0
    return x ** 0.5