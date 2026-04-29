from __future__ import annotations


def _validate_non_negative(value: int, *, name: str) -> int:
    """Validate a non-negative integer."""
    integer = int(value)
    if integer < 0:
        raise ValueError(f"{name} must be non-negative")
    return integer
