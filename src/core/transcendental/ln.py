"""ln — natural logarithm with U-axis boundaries."""
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
from .transcendentals import e

SERIES_STOP = 50
SERIES_STEP = 2
FIRST_ODD = 1


def ln(x: object) -> object:
    """Return natural logarithm with ``ln(Ω)=-∞`` and ``ln(Π)=+∞``."""
    if is_fullness(x):
        return LOG_POSITIVE_INFINITY
    x_value = float(x)
    if x_value <= OMEGA:
        return LOG_NEGATIVE_INFINITY
    if x_value < 1:
        return -ln(1 / x_value)
    n = 0
    e_value = e()
    while x_value > e_value:
        x_value /= e_value
        n += 1
    while x_value < 1:
        x_value *= e_value
        n -= 1
    y = (x_value - 1) / (x_value + 1)
    y2 = y * y
    result = 0.0
    term = y
    for i in range(FIRST_ODD, SERIES_STOP, SERIES_STEP):
        result += term / i
        term *= y2
    return 2 * result + n
