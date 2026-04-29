from __future__ import annotations

from ._validate_non_negative import _validate_non_negative
from .paths_count import paths_count
from ..number_theory.number_structure import binary_address


def routes(depth: int) -> tuple[tuple[int, ...], ...]:
    """Return all binary routes at a finite branching depth."""
    depth_value = _validate_non_negative(depth, name="depth")
    return tuple(
        binary_address(value, depth=depth_value) for value in range(paths_count(depth_value))
    )
