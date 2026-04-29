"""sin — sine via Taylor series."""
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
from .transcendentals import half_pi, pi, two_pi


def sin(x):
    pi_value = pi()
    half_pi_value = half_pi()
    two_pi_value = two_pi()
    while x > two_pi_value:
        x -= two_pi_value
    while x < -two_pi_value:
        x += two_pi_value
    if x > pi_value:
        x = x - two_pi_value
    if x < -pi_value:
        x = x + two_pi_value
    if x < 0:
        return -sin(-x)
    if x > half_pi_value:
        x = pi_value - x
    x2 = x * x
    return x - x2 * x / 6 + x2 * x2 * x / 120
