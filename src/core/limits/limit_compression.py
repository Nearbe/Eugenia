"""Limit of compression: ``lim (a : Dⁿ(Id)) = Ω``."""

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
from ..foundations.u_algebra import divide


def compression_term(value: object, depth: int) -> object:
    """Return finite compression term ``value : Dⁿ(Id)``."""
    if depth < 0:
        raise ValueError("compression depth must be non-negative")
    result = value
    for _ in range(depth):
        result = divide(result, 2.0)
    return result


def limit_compression(value: object) -> float:
    """Return the algebraic attractor of infinite compression: Ω."""
    return OMEGA
