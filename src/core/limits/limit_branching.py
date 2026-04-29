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
from core.infinity.infinity import PI
from core.algebra import branch


def branching_term(n: int) -> float:
    """Return Dⁿ(Id)."""
    value = 1.0
    for _ in range(n):
        value = float(branch(value))
    return value


def limit_branching() -> float:
    """Return lim Dⁿ(Id) = Π."""
    return PI
