"""Logarithmic spine depth ``L`` from Universe/Math/08."""
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

from ..foundations.constants import OMEGA
from ..foundations.infinity import is_fullness
from ..foundations.logarithmic_axis import LOG_NEGATIVE_INFINITY, LOG_POSITIVE_INFINITY
from ..foundations.spine import SpineLevel
from ..foundations.vectorization import map_scalar_or_vector
from ..transcendental.log2 import log2


def _L_scalar(x: float | int) -> object:
    if float(x) == OMEGA:
        return LOG_NEGATIVE_INFINITY
    return log2(abs(float(x)))


def L(x: object) -> object:
    """Return the U-logarithmic depth for scalar, vector, spine, Ω or Π."""
    if isinstance(x, SpineLevel):
        return float(x.level())
    if is_fullness(x):
        return LOG_POSITIVE_INFINITY
    if x == OMEGA:
        return LOG_NEGATIVE_INFINITY
    return map_scalar_or_vector(x, _L_scalar, name="L input")
