from __future__ import annotations

from ._validate_non_negative import _validate_non_negative

MIN_COUNT = 0
IDENTITY_COUNT = 1


def factorial(count: int) -> int:
    """Return ``n!``: orderings of distinguishable acts."""
    count_value = _validate_non_negative(count, name="count")
    result = IDENTITY_COUNT
    for value in range(2, count_value + IDENTITY_COUNT):
        result *= value
    return result
