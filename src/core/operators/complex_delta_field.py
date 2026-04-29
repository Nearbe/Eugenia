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
from ..foundations.bounds import clamp_pixel
from ..foundations.complex_plane import ComplexState
from ..foundations.constants import PIXEL_MAX
from ..foundations.vectorization import map_scalar_or_vector


def _complex_delta_scalar(x: float | int) -> ComplexState:
    x_c = clamp_pixel(x)
    normalized = x_c / PIXEL_MAX if PIXEL_MAX else 0.0
    return ComplexState(normalized, 1.0 - normalized)


def complex_delta_field(x):
    """Map a scalar or iterable of pixel-like values to Re/Im delta states."""
    return map_scalar_or_vector(x, _complex_delta_scalar, name="complex_delta_field input")
