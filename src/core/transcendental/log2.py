"""Base-2 logarithm on the U-logarithmic axis."""

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

from ..constants.constants import OMEGA
from ..infinity.infinity import is_fullness
from ..utils.logarithmic_axis import LOG_NEGATIVE_INFINITY, LOG_POSITIVE_INFINITY


def log2(x: object) -> object:
    """Return ``L`` in base 2 with algebraic boundaries for Ω and Π."""
    if is_fullness(x):
        return LOG_POSITIVE_INFINITY
    if x == OMEGA:
        return LOG_NEGATIVE_INFINITY
    x_value = float(x)
    if x_value <= OMEGA:
        return LOG_NEGATIVE_INFINITY
    return math.log2(x_value)
