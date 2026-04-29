"""2-adic distance helpers."""

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
from ..foundations.logarithmic_axis import LOG_POSITIVE_INFINITY
from ..foundations.vectorization import is_vector, zip_vectors
from ..number_theory.v2_adic_valuation import v2_adic_valuation


def _p_adic_scalar(a: float | int, b: float | int) -> float:
    """Return the 2-adic distance ``2**(-v₂(a-b))`` for scalar values."""
    valuation = v2_adic_valuation(float(a) - float(b))
    if valuation == LOG_POSITIVE_INFINITY:
        return 0.0
    return 2.0 ** (-valuation)


def p_adic_distance(a, b):
    """Return scalar or element-wise 2-adic distances.

    Integer inputs follow the strict formula ``d₂(x, y)=2**(-v₂(x-y))`` with
    ``d₂(x, x)=0``.  Non-integer floats are deterministically coerced in
    :func:`v2_adic_valuation`; callers that need rigorous p-adics should pass
    integer deltas.
    """
    if is_vector(a) or is_vector(b):
        return [_p_adic_scalar(x, y) for x, y in zip_vectors(a, b, name="p_adic_distance")]
    return _p_adic_scalar(a, b)
