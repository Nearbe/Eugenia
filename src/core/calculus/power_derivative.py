from __future__ import annotations

from ..algebra import multiply, power
from .differential_state import IDENTITY_VELOCITY


def power_derivative(exponent: object, point: object) -> object:
    """Return derivative of ```x^b``` from the dual-expansion rule."""
    exponent_value = float(exponent)
    return multiply(exponent_value, power(point, exponent_value - IDENTITY_VELOCITY))
