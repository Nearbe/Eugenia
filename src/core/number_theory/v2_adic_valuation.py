"""2-adic valuation helpers.

For integers, ``v₂(n)`` is the largest exponent ``k`` such that ``2**k`` divides
``n``.  The valuation of zero is ``+inf``; this makes the induced distance obey
``d(x, x) = 0``.  Non-integer floats are not rigorous p-adic integers, so they
are handled by a deterministic integer coercion: round to the nearest integer,
except non-zero values that round to zero are treated as valuation ``0``.
"""

#  Copyright (c) 2026.
#  ╔═══════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═══════════════════════════════════╝
import math

from ..foundations.logarithmic_axis import LOG_POSITIVE_INFINITY


def _coerce_integer_delta(val: float | int) -> int:
    value = float(val)
    if not math.isfinite(value):
        raise ValueError("2-adic valuation is defined only for finite values")
    if value == 0.0:
        return 0
    rounded = int(round(value))
    return rounded if rounded != 0 else 1


def v2_adic_valuation(val: float | int) -> float | object:
    """Return ``v₂(val)`` with ``v₂(0) = +∞`` on the U-logarithmic axis."""
    integer = _coerce_integer_delta(val)
    if integer == 0:
        return LOG_POSITIVE_INFINITY
    value = abs(integer)
    exponent = 0
    while value % 2 == 0:
        value //= 2
        exponent += 1
    return float(exponent)
