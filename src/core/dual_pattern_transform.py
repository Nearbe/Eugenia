"""Dual pattern transformation."""

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
from .dual_form import dual_form

DERIVATIVE_SCALE = 0.1


def dual_pattern_transform(values: list[float], velocities: list[float] | None = None):
    if not values:
        return [], []

    if velocities is None:
        mean_value = sum(values) / len(values)
        velocities = [DERIVATIVE_SCALE * (value - mean_value) for value in values]

    forms = [dual_form(value, velocity)[0] for value, velocity in zip(values, velocities)]
    growth = [dual_form(value, velocity)[1] for value, velocity in zip(values, velocities)]
    return forms, growth
