"""Domain bounds used by core mathematical transforms."""

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
from .constants import DELTA_MAX, DELTA_MIN, PIXEL_MAX, PIXEL_MIN


def clamp(value: float | int, lower: float, upper: float) -> float:
    """Clamp a numeric value to a closed interval."""

    value_f = float(value)
    return max(min(value_f, upper), lower)


def clamp_pixel(value: float | int) -> float:
    """Clamp a value to the closed pixel domain."""

    return clamp(value, PIXEL_MIN, PIXEL_MAX)


def clamp_delta(value: float | int) -> float:
    """Clamp a value to the closed delta-field domain."""

    return clamp(value, DELTA_MIN, DELTA_MAX)
