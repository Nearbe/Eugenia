from __future__ import annotations

from collections.abc import Callable

from ..algebra import multiply


def chain_derivative(
    outer_derivative: Callable[[object], object],
    inner_fn: Callable[[object], object],
    inner_derivative: Callable[[object], object],
    point: object,
) -> object:
    """Return ``(f∘g)'(x) = f'(g(x)) · g'(x)``."""
    return multiply(outer_derivative(inner_fn(point)), inner_derivative(point))
