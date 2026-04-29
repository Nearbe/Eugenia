"""Compression operator ``H(a) = a : D(Id) = a/2``.

``H`` is the inverse scale operator for :func:`core.D.D`: ``H(D(a)) = a`` and
``D(H(a)) = a`` for scalar values and list-like numeric vectors.
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

from ..foundations.u_algebra import compress


def H(x: float | int | Iterable[float]) -> object:
    """Return the U-system compression of ``x``."""
    return compress(x)
