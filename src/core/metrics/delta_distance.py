"""Delta distance on spine scale: |L(a) - L(b)|."""
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
from ..foundations.vectorization import is_scalar, zip_vectors
from ..operators.L import L


def delta_distance(a, b):
    la, lb = L(a), L(b)
    if is_scalar(la) and is_scalar(lb):
        return abs(float(la) - float(lb))
    return [abs(left - right) for left, right in zip_vectors(la, lb, name="delta_distance")]
