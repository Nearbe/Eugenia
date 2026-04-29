"""Limit of branching: ``lim Dⁿ(Id) = Π``."""

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
from ..foundations.infinity import PI
from ..foundations.u_algebra import branch


def branching_term(depth: int) -> object:
    """Return finite branch term ``Dⁿ(Id)``."""
    if depth < 0:
        raise ValueError("branching depth must be non-negative")
    result: object = 1.0
    for _ in range(depth):
        result = branch(result)
    return result


def limit_branching() -> object:
    """Return the algebraic attractor of infinite branching: Π."""
    return PI
