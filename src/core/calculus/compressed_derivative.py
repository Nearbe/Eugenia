from __future__ import annotations

from collections.abc import Callable

from ..constants.constants import D_ID
from ..algebra import compress, divide


def compressed_derivative(derivative_fn: Callable[[object], object], point: object) -> object:
    """Return ``h'(x)`` for ``h(x)=f(x : D(Id))``."""
    return divide(derivative_fn(compress(point)), D_ID)
