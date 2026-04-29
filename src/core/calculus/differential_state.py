from __future__ import annotations

from collections.abc import Callable

from ..states.dual_number import DualNumber, dual_number

IDENTITY_VELOCITY = 1.0


def differential_state(
    fn: Callable[[object], object],
    derivative_fn: Callable[[object], object],
    point: object,
    *,
    velocity: object = IDENTITY_VELOCITY,
) -> DualNumber:
    """Return ``f(x + vε) = f(x) + f'(x)·vε``."""
    return dual_number(point, velocity).apply(fn, derivative_fn)
