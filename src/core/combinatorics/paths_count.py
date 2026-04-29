from __future__ import annotations

from ._validate_non_negative import _validate_non_negative
from ..number_theory.number_structure import modulus_from_depth

MIN_COUNT = 0


def paths_count(depth: int) -> int:
    """Return number of paths of length ``depth``: ``Dⁿ(Id)``."""
    depth_value = _validate_non_negative(depth, name="depth")
    return modulus_from_depth(depth_value)
