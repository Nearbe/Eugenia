"""Complex delta field helpers."""

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


def _complex_delta_scalar(x: float | int) -> complex:
    x_c = max(min(float(x), 255.0), 0.0)
    normalized = x_c / 255.0
    return complex(normalized, 1.0 - normalized)


def complex_delta_field(x):
    """Map a scalar or iterable of pixel-like values to complex delta points."""
    if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
        return [_complex_delta_scalar(v) for v in x]
    return _complex_delta_scalar(x)
