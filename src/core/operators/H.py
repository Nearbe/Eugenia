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

from .constants import D_ID
from .vectorization import map_scalar_or_vector


def H(x: float | int | Iterable[float]) -> float | list[float]:
    """Return the U-system compression of ``x``."""
    return map_scalar_or_vector(x, lambda value: value / D_ID, name="H input")
