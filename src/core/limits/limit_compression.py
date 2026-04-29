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

from core.constants.constants import OMEGA
from core.algebra import compress


def compression_term(a: float, n: int) -> float:
    """Return Hⁿ(a)."""
    value = a
    for _ in range(n):
        value = float(compress(value))
    return value


def limit_compression(a: float) -> float:
    """Return lim Hⁿ(a) = Ω."""
    return OMEGA
