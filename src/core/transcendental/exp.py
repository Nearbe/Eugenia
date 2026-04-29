"""exp — exponential function."""

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
from ..infinity.infinity import PI, is_fullness

# Thresholds for exponential function to avoid overflow
EXP_LARGE_POSITIVE_THRESHOLD = 700
EXP_LARGE_NEGATIVE_THRESHOLD = -700
# Number of terms in Taylor series expansion
EXP_TAYLOR_TERMS = 50


def exp(x: object) -> object:
    if is_fullness(x):
        return PI
    x_value = float(x)
    if x_value == OMEGA:
        return 1.0
    if x_value > EXP_LARGE_POSITIVE_THRESHOLD:
        return PI
    if x_value < EXP_LARGE_NEGATIVE_THRESHOLD:
        return 0.0
    result = 1.0
    term = 1.0
    for i in range(1, EXP_TAYLOR_TERMS):
        term *= x_value / i
        result += term
    return result
