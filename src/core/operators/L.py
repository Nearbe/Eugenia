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

from ..constants.constants import OMEGA
from ..infinity.infinity import is_fullness
from ..utils.logarithmic_axis import LOG_NEGATIVE_INFINITY, LOG_POSITIVE_INFINITY
from ..states.spine import SpineLevel
from ..utils.vectorization import map_scalar_or_vector
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
