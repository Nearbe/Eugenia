"""Inverse of the pinned log2 pixel delta-field contract."""

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
from ..foundations.bounds import clamp_delta, clamp_pixel
from ..foundations.constants import PIXEL_SCALE
from ..foundations.vectorization import map_scalar_or_vector


def _inverse_delta_field_scalar(d: float | int) -> float:
    """Return ``x`` such that ``delta_field(x) ≈ d`` within pixel bounds."""
    d_c = clamp_delta(d)
    power = 2.0**d_c
    x = (PIXEL_SCALE * power - 1.0) / (power + 1.0)
    return clamp_pixel(x)


def inverse_delta_field(d):
    """Invert scalar or list-like delta values to the closed pixel interval."""
    return map_scalar_or_vector(d, _inverse_delta_field_scalar, name="inverse_delta_field input")
