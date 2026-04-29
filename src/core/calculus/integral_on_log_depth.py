from __future__ import annotations

from collections.abc import Callable

from ..states.spine import SpineLevel
from ..algebra import multiply
from ..operators.L import L
from ..constants.constants import D_ID


def integral_on_log_depth(fn: Callable[[object], object], depth: SpineLevel) -> object:
    """Return log-depth integrand ``f(D^ℓ)·L(D(Id))·D^ℓ``."""
    state = depth.value()
    return multiply(multiply(fn(state), L(D_ID)), state)
