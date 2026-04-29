"""Resolve potential: Ω → default."""
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
from .constants import OMEGA
from .vectorization import is_scalar, to_vector


def resolve_potential(x, default: float = 0.0):
    if x is None:
        return default
    if is_scalar(x):
        return default if float(x) == OMEGA else float(x)
    for value in to_vector(x, name="resolve_potential input"):
        if value != OMEGA:
            return value
    return default
