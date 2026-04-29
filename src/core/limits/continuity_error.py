"""Numerical continuity error ``|f(lim xₙ) - lim f(xₙ)|``."""

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
from collections.abc import Callable, Iterable, Sequence

from .vectorization import last_or_default


def continuity_error(
    fn: Callable[[float], float],
    x_sequence: Sequence[float] | Iterable[float],
    *,
    x_limit: float | None = None,
) -> float:
    """Return the finite-sample continuity defect for a scalar operator."""

    observed_limit = last_or_default(x_sequence, 0.0) if x_limit is None else float(x_limit)
    transformed_sequence = [float(fn(value)) for value in x_sequence]
    transformed_limit = last_or_default(transformed_sequence, float(fn(observed_limit)))
    return abs(float(fn(observed_limit)) - transformed_limit)
