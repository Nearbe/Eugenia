"""Ridge to percentage: sigmoid(n) × 100%."""

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
from core.transcendental.exp import exp

RIDGE_EXP_MIN = -700.0
RIDGE_EXP_MAX = 700.0
PERCENT_MAX = 100.0
PERCENT_MIN = 0.0


def ridge_to_percentage(n):
    value = float(n)
    if RIDGE_EXP_MIN < value < RIDGE_EXP_MAX:
        return PERCENT_MAX / (1.0 + exp(-value))
    return PERCENT_MAX if value > 0.0 else PERCENT_MIN
