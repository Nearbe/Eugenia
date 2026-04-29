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
from ..constants.bounds import clamp_pixel
from ..states.complex_plane import complex_state, is_complex_fullness
from ..constants.constants import PIXEL_MAX, PIXEL_MIN


def inverse_complex_delta_field(z) -> float:
    """Collapse a Re/Im delta state back to a pixel coordinate."""
    state = complex_state(z)
    if is_complex_fullness(state):
        return PIXEL_MAX
    denominator = state.real + state.imaginary
    if denominator == 0:
        return PIXEL_MIN
    return clamp_pixel(PIXEL_MAX * state.real / denominator)
