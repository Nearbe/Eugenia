"""
Cosine similarity — на алгебре долей.

Вместо евклидова косинуса (который ломается на нуле),
используем отношение долей от Π:

    Sim(a, b) = (a:Π) ⊗ (b:Π) / (||a:Π|| ⊕ ||b:Π||)

Это работает на всех уровнях Хребта, включая Π и Ω.
"""

import math
from typing import Sequence, Union

from .percent import to_percentage

Number = Union[int, float]


def _clip(val: float, lo: float, hi: float) -> float:
    """Pure Python clip."""
    if val < lo:
        return lo
    if val > hi:
        return hi
    return val


def similarity(
    a: Union[Number, Sequence[Number]], b: Union[Number, Sequence[Number]]
) -> Union[float, list[float]]:
    """
    Сходство через алгебру долей (процентов).

    Args:
        a: First vector.
        b: Second vector.

    Returns:
        Cosine similarity in [-1, 1] computed in percentage space.
    """
    # Scalar case
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        pa = to_percentage(a)
        pb = to_percentage(b)
        norm_a = math.sqrt(pa**2)  # type: ignore[operator]
        norm_b = math.sqrt(pb**2)  # type: ignore[operator]
        dot = pa * pb  # type: ignore[operator]
        denom = norm_a * norm_b
        if denom < 1e-10:
            return 1.0
        return _clip(dot / denom, -1.0, 1.0)

    # Sequence case: element-wise cosine similarity
    pa = to_percentage(a)
    pb = to_percentage(b)
    norm_a = math.sqrt(sum(x**2 for x in pa))  # type: ignore[arg-type]
    norm_b = math.sqrt(sum(x**2 for x in pb))  # type: ignore[arg-type]
    dot = sum(x * y for x, y in zip(pa, pb))  # type: ignore[arg-type]
    denom = norm_a * norm_b
    if denom < 1e-10:
        return 1.0
    return _clip(dot / denom, -1.0, 1.0)
