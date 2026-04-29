"""Continuity defect ``|f(lim xₙ) - lim f(xₙ)|`` for finite samples."""

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

from ..foundations.vectorization import last_or_default
from ..metrics.euclidean_distance import euclidean_distance


def continuity_error(
    fn: Callable[[float], object],
    x_sequence: Sequence[float] | Iterable[float],
    *,
    x_limit: float | None = None,
) -> float:
    """Return finite-sample defect for the continuity contract."""
    observed_values = list(x_sequence)
    observed_limit = last_or_default(observed_values, 0.0) if x_limit is None else float(x_limit)
    transformed_sequence = [fn(value) for value in observed_values]
    transformed_limit = last_or_default(transformed_sequence, fn(observed_limit))
    expected_limit = fn(observed_limit)
    return float(euclidean_distance([float(expected_limit)], [float(transformed_limit)]))
