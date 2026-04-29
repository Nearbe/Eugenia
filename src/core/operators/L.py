"""Binary spine depth ``L(x) = log2(|x|)``.

The strict scalar domain is non-zero finite magnitude.  ``x == 0`` is kept as a
compatibility sentinel for the U-system potential ``Ω`` and returns ``-inf``.
Iterable inputs are mapped element-wise and return a plain list.
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

from .log2 import log2
from .vectorization import map_scalar_or_vector


def _L_scalar(x: float | int) -> float:
    if x == 0:
        return float("-inf")
    return log2(abs(float(x)))


def L(x: float | int | Iterable[float]) -> float | list[float]:
    """Return the binary depth for a scalar or list-like vector."""
    return map_scalar_or_vector(x, _L_scalar, name="L input")
