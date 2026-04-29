from __future__ import annotations

from collections.abc import Callable

from .derivative import derivative


def second_derivative(
    first_derivative_fn: Callable[[object], object],
    second_derivative_fn: Callable[[object], object],
    point: object,
) -> object:
    """Return ```f''(x)``` by extracting dynamics of the first derivative."""
    return derivative(first_derivative_fn, second_derivative_fn, point)
