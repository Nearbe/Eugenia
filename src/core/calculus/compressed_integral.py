from __future__ import annotations

from collections.abc import Callable

from ..algebra import branch, compress


def compressed_integral(primitive_fn: Callable[[object], object], point: object) -> object:
    """Return ``∫ f(x:D(Id))dx = (∫ f(u)du) ⊗ D(Id)``."""
    return branch(primitive_fn(compress(point)))
