"""Bridge identity diagnostics for pattern values via Eugenia core math."""

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

from .L import L
from .linear_algebra import EPSILON, mean, to_vector, variance


def pattern_bridge_identity(values) -> dict:
    if isinstance(values, Iterable) and not isinstance(values, (str, bytes)):
        source = values
    else:
        source = [float(values)]

    vector = to_vector(source)
    if not vector:
        return {"bridge_identity": False, "variance": 0.0, "mean_spine_level": 0.0}

    levels = [L(float(value)) for value in vector]
    level_variance = float(variance(levels))
    return {
        "bridge_identity": level_variance < EPSILON,
        "variance": level_variance,
        "mean_spine_level": float(mean(levels)),
    }
