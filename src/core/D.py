"""Branching: D(a) = a : Ω = a ⊕ a (doubling)."""
from .constants import D_ID


def D(x: float | int | list) -> float | list:
    if isinstance(x, (int, float)):
        return x * D_ID
    return [float(v) * D_ID for v in x]