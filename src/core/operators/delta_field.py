"""Pixel delta-field transformation.

The visualization pipeline is pinned to the existing log2 pixel contract from
``src.models.config`` and README::

    Δ(x) = log2(x + 1) - log2(256 - x),    x ∈ [0, 255]

Inputs are clamped to the closed pixel interval so boundary values are finite
and deterministic: ``delta_field(0) == -8`` and ``delta_field(255) == 8``.
Universe also describes a natural-log ``ln|Re|-ln|Im|`` form; this module keeps
log2 because the sweep configuration is based on the binary spine ``D^8``.
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
from ..foundations.bounds import clamp_pixel
from ..foundations.constants import DELTA_MAX, DELTA_MIN, PIXEL_MAX, PIXEL_MIN, PIXEL_SCALE
from ..foundations.vectorization import map_scalar_or_vector
from ..transcendental.log2 import log2


def _delta_field_scalar(x: float | int) -> float:
    x_c = clamp_pixel(x)
    return log2(x_c + 1.0) - log2(PIXEL_SCALE - x_c)


def delta_field(x):
    """Return scalar delta or element-wise deltas for list-like pixel values."""
    return map_scalar_or_vector(x, _delta_field_scalar, name="delta_field input")
