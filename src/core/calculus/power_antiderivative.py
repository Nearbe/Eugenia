from __future__ import annotations

from ..algebra import add, divide, power
from .differential_state import IDENTITY_VELOCITY


def power_antiderivative(exponent: object, point: object) -> object:
    """Return primitive of ``x^b`` at ``point``: ``x^(b⊕Id) : (b⊕Id)``."""
    next_exponent = add(exponent, IDENTITY_VELOCITY)
    return divide(power(point, next_exponent), next_exponent)
