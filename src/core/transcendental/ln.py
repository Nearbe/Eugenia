"""ln — natural logarithm."""
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
from .__math_constants import E


def ln(x: float) -> float:
    if x <= 0:
        return float("-inf")
    if x < 1:
        return -ln(1 / x)
    n = 0
    while x > E:
        x /= E
        n += 1
    while x < 1:
        x *= E
        n -= 1
    y = (x - 1) / (x + 1)
    y2 = y * y
    result = 0.0
    term = y
    for i in range(1, 50, 2):
        result += term / i
        term *= y2
    return 2 * result + n
