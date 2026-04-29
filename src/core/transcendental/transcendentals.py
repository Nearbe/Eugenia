"""Computed transcendental values used by numerical series."""

PI_TERMS = 16
E_TERMS = 24
MACHIN_FIVE = 5.0
MACHIN_TWO_THIRTY_NINE = 239.0
D_ID = 2.0


def _arctan_inverse(value: float, terms: int = PI_TERMS) -> float:
    """Compute arctan(1 / value) with the alternating Taylor series."""
    inverse = 1.0 / value
    inverse_square = inverse * inverse
    term = inverse
    result = 0.0
    sign = 1.0
    for index in range(terms):
        denominator = D_ID * index + 1.0
        result += sign * term / denominator
        term *= inverse_square
        sign = -sign
    return result


def pi() -> float:
    """Compute π via Machin's formula."""
    return 16.0 * _arctan_inverse(MACHIN_FIVE) - 4.0 * _arctan_inverse(MACHIN_TWO_THIRTY_NINE)


def half_pi() -> float:
    """Compute π / 2."""
    return pi() / D_ID


def two_pi() -> float:
    """Compute 2π."""
    return pi() * D_ID


def e() -> float:
    """Compute Euler's number from the factorial reciprocal series."""
    result = 1.0
    factorial = 1.0
    for value in range(1, E_TERMS):
        factorial *= value
        result += 1.0 / factorial
    return result
