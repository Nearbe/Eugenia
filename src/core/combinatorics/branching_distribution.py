from __future__ import annotations

from ._validate_non_negative import _validate_non_negative
from .binomial_coefficient import binomial_coefficient


def branching_distribution(depth: int) -> tuple[int, ...]:
    """Return binomial layer distribution for all right-choice counts."""
    depth_value = _validate_non_negative(depth, name="depth")
    return tuple(binomial_coefficient(depth_value, choice) for choice in range(depth_value + 1))
