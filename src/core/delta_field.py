"""Delta field transformation: log2(x + 1) - log2(256 - x)."""

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

PIXEL_MIN = 0.0
PIXEL_MAX_EXCLUSIVE = 254.999
PIXEL_SCALE = 256.0


def _delta_field_scalar(x: float | int) -> float:
    x_c = max(min(float(x), PIXEL_MAX_EXCLUSIVE), PIXEL_MIN)
    return log2(x_c + 1.0) - log2(PIXEL_SCALE - x_c)


def delta_field(x):
    if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
        return [_delta_field_scalar(value) for value in x]
    return _delta_field_scalar(x)
