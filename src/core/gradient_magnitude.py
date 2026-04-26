"""Gradient magnitude helpers."""

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
from __future__ import annotations

import math
from collections.abc import Iterable
from numbers import Real


def gradient_magnitude(*components: Real | Iterable[Real]) -> float:
    """Return Euclidean magnitude for scalars or iterables of components."""

    values: list[float] = []
    for component in components:
        if isinstance(component, Real):
            values.append(float(component))
            continue
        values.extend(float(value) for value in component)

    return math.sqrt(sum(value * value for value in values))
