from __future__ import annotations

from collections.abc import Callable

from ..algebra import branch, compress


def branched_integral(primitive_fn: Callable[[object], object], point: object) -> object:
    """Return ``∫ f(D(x))dx = (∫ f(u)du) : D(Id)``."""
    return compress(primitive_fn(branch(point)))
