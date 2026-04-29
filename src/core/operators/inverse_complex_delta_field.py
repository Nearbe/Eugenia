"""Inverse complex delta field: ``z → X`` on the closed pixel interval."""

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
from .constants import PIXEL_MAX, PIXEL_MIN


def inverse_complex_delta_field(z) -> float:
    re = z.real if hasattr(z, "real") else z[0]
    im = z.imag if hasattr(z, "imag") else z[1]
    denominator = re + im
    if denominator == 0:
        return PIXEL_MIN
    return clamp_pixel(PIXEL_MAX * re / denominator)
