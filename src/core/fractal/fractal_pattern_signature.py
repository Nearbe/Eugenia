"""Fractal-like pattern signature from numeric values via Eugenia core math."""

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
from .L import L
from .linear_algebra import diff, linspace, mean, std, to_vector
from .ridge_to_percentage import ridge_to_percentage

PROFILE_SIZE = 64
TOP_JUMP_COUNT = 5


def fractal_pattern_signature(values) -> dict:
    vector = to_vector(values)
    if not vector:
        return {
            "profile": [0.0] * PROFILE_SIZE,
            "top_jumps": [],
            "fractal_dimension": 0.0,
            "spine_level": 0.0,
            "percentage": 0.0,
            "avg_value": 0.0,
        }

    thresholds = linspace(min(vector), max(vector), PROFILE_SIZE)
    profile = [sum(1 for value in vector if value > threshold) / len(vector) for threshold in thresholds]
    jumps = [abs(value) for value in diff(profile)]
    top_jumps = sorted((float(value) for value in jumps), reverse=True)[:TOP_JUMP_COUNT]
    avg_value = float(mean(vector))
    spine_level = float(L(avg_value))

    return {
        "profile": profile,
        "top_jumps": top_jumps,
        "fractal_dimension": float(std(profile)),
        "spine_level": spine_level,
        "percentage": float(ridge_to_percentage(spine_level)),
        "avg_value": avg_value,
    }
