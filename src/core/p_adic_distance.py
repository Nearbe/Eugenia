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
from collections.abc import Iterable

from .v2_adic_valuation import v2_adic_valuation


def _p_adic_scalar(a: float | int, b: float | int) -> float:
    valuation = v2_adic_valuation(float(a) - float(b))
    if valuation == float("inf"):
        return 0.0
    if valuation == float("-inf"):
        return float("inf")
    return 2.0 ** (-valuation)


def p_adic_distance(a, b):
    """Return scalar distance or element-wise distances for two iterables."""
    if isinstance(a, Iterable) and isinstance(b, Iterable):
        return [_p_adic_scalar(x, y) for x, y in zip(a, b)]
    return _p_adic_scalar(a, b)
