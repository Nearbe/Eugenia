from __future__ import annotations

from collections.abc import Callable

from ..algebra import add


def antiderivative(
    primitive_fn: Callable[[object], object],
    point: object,
    *,
    constant: object = 0.0,
) -> object:
    """Return ``F(x) ⊕ C`` for an indefinite integral."""
    return add(primitive_fn(point), constant)
