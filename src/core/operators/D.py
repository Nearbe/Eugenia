"""Branching operator ``D(a) = a : Ω = 2a``.

The public contract is intentionally small: scalars are doubled and list-like
vectors are doubled element-by-element.  The vector branch returns a plain list
for compatibility with the existing core/nucleus code.
"""
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
from collections.abc import Iterable

from ..algebra import branch


def D(x: float | int | Iterable[float]) -> object:
    """Return the U-system branching of ``x``.

    ``D`` is the linear scale operator from Universe/Math/13: ``D(a)=2a``.
    Vector inputs are lifted component-wise by the shared vectorization rule.
    """
    return branch(x)
