from __future__ import annotations

from ._validate_non_negative import _validate_non_negative
from .factorial import factorial

MIN_COUNT = 0


def binomial_coefficient(total: int, chosen: int) -> int:
    """Return ``C(n,k)`` paths with exactly ``k`` right-branch choices."""
    total_value = _validate_non_negative(total, name="total")
    chosen_value = _validate_non_negative(chosen, name="chosen")
    if chosen_value > total_value:
        return MIN_COUNT
    left_count = chosen_value
    right_count = total_value - chosen_value
    return factorial(total_value) // (factorial(left_count) * factorial(right_count))
