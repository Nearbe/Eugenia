"""arctan — inverse tangent via Taylor series."""

from .transcendentals import pi, half_pi


def arctan(x: float) -> float:
    """Return arctan(x) using Taylor series with enough terms for accuracy."""
    if x == 0.0:
        return 0.0
    if x < 0.0:
        return -arctan(-x)
    if x > 1.0:
        return half_pi() - arctan(1.0 / x)
    x2 = x * x
    result = x
    term = x
    sign = -1.0
    for n in range(1, 100):
        term *= x2
        result += sign * term / (2 * n + 1.0)
        sign = -sign
    return result


def arctan2(y: float, x: float) -> float:
    """Return arctan2(y, x) — angle from origin to point (x, y)."""
    pi_value = pi()
    half_pi_value = half_pi()
    if x > 0.0:
        return arctan(y / x)
    if x < 0.0:
        if y >= 0.0:
            return arctan(y / x) + pi_value
        return arctan(y / x) - pi_value
    if y > 0.0:
        return half_pi_value
    if y < 0.0:
        return -half_pi_value
    return 0.0
