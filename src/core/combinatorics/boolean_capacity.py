from __future__ import annotations

from .paths_count import paths_count


def boolean_capacity(size: int) -> int:
    """Return power-set capacity ``|P(A)| = Dⁿ(Id)``."""
    return paths_count(size)
