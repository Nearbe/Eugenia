"""Atomic scalar/vector operations for the Eugenia math core.

The vector contract follows Universe/Essentials/Vectorization.md: scalar core
operators lift component-wise to vectors, while binary vector operations require
matching dimensions.
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
from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import TypeVar

ScalarResult = TypeVar("ScalarResult")
VectorizedResult = ScalarResult | list[ScalarResult]

STRING_LIKE_TYPES = (str, bytes)


def is_scalar(value: object) -> bool:
    """Return true for numeric scalar values accepted by core operators."""

    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_vector(value: object) -> bool:
    """Return true for list-like mathematical vectors, excluding text bytes."""

    return isinstance(value, Iterable) and not isinstance(value, STRING_LIKE_TYPES)


def to_scalar(value: object, *, name: str = "value") -> float:
    """Normalize one numeric scalar to ``float`` or raise a precise error."""

    if not is_scalar(value):
        raise TypeError(f"{name} must be a numeric scalar")
    return float(value)


def to_vector(value: object, *, name: str = "value") -> list[float]:
    """Normalize a vector-like value to a plain list of floats."""

    if is_scalar(value):
        return [float(value)]
    if not is_vector(value):
        raise TypeError(f"{name} must be a numeric scalar or vector")
    return [to_scalar(component, name=f"{name} component") for component in value]


def map_scalar_or_vector(
    value: object,
    scalar_fn: Callable[[float], ScalarResult],
    *,
    name: str = "value",
) -> VectorizedResult[ScalarResult]:
    """Apply ``scalar_fn`` to a scalar or component-wise to a vector."""

    if is_scalar(value):
        return scalar_fn(float(value))
    if not is_vector(value):
        raise TypeError(f"{name} must be a numeric scalar or vector")
    return [scalar_fn(to_scalar(component, name=f"{name} component")) for component in value]


def zip_vectors(left: object, right: object, *, name: str = "vectors") -> list[tuple[float, float]]:
    """Normalize and pair two vectors, requiring equal dimensions."""

    values_left = to_vector(left, name=f"{name} left")
    values_right = to_vector(right, name=f"{name} right")
    if len(values_left) != len(values_right):
        raise ValueError(
            f"{name} require equal dimensions, got {len(values_left)} and {len(values_right)}"
        )
    return list(zip(values_left, values_right))


def vector_delta(vector_a: object, vector_b: object) -> list[float]:
    """Return linear vector deviation ``ΔV = V_B - V_A``."""

    return [right - left for left, right in zip_vectors(vector_a, vector_b, name="vector_delta")]


def last_or_default(sequence: Sequence[float] | Iterable[float], default: float = 0.0) -> float:
    """Return the last observed sequence value as a finite limit proxy."""

    if isinstance(sequence, Sequence):
        return float(sequence[-1]) if sequence else float(default)
    last = float(default)
    for value in sequence:
        last = float(value)
    return last
