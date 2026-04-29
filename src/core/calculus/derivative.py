from __future__ import annotations

from collections.abc import Callable

from .differential_state import differential_state


def derivative(
    fn: Callable[[object], object],
    derivative_fn: Callable[[object], object],
    point: object,
) -> object:
    """Isolate `f'(x)` to represent the concealed coefficient related to unit velocity."""
    return differential_state(fn, derivative_fn, point).velocity
