from __future__ import annotations

from collections.abc import Callable

from ..algebra import add


def add_derivative(
    left_derivative: Callable[[object], object],
    right_derivative: Callable[[object], object],
    point: object,
) -> object:
    """Return derivative of ``f⊕g``."""
    return add(left_derivative(point), right_derivative(point))
