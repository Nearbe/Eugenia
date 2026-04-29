from __future__ import annotations

from collections.abc import Callable

from ..constants.constants import D_ID
from ..algebra import branch, multiply


def branched_derivative(derivative_fn: Callable[[object], object], point: object) -> object:
    """Return ``g'(x)`` for ``g(x)=f(D(x))``."""
    return multiply(D_ID, derivative_fn(branch(point)))
