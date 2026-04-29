from __future__ import annotations

from collections.abc import Callable

from ..algebra import add


def definite_integral(
    primitive_fn: Callable[[object], object],
    lower: object,
    upper: object,
) -> object:
    """Return ``∫ₐᵇ f(x)dx = F(b) ⊖ F(a)``."""
    return add(primitive_fn(upper), -float(primitive_fn(lower)))
