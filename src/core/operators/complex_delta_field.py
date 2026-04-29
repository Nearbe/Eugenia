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
from .bounds import clamp_pixel
from .constants import PIXEL_MAX
from .vectorization import map_scalar_or_vector


def _complex_delta_scalar(x: float | int) -> complex:
    x_c = clamp_pixel(x)
    normalized = x_c / PIXEL_MAX if PIXEL_MAX else 0.0
    return complex(normalized, 1.0 - normalized)


def complex_delta_field(x):
    """Map a scalar or iterable of pixel-like values to complex delta points."""
    return map_scalar_or_vector(x, _complex_delta_scalar, name="complex_delta_field input")
