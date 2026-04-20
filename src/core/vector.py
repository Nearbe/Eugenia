"""
Vector normalization — Нормализация векторов.

normalize_vector_safe — векторная нормализация на алгебре долей.
Вместо v / ||v|| (которая ломается на нуле),
используем: v : Π = to_percentage(v)
"""

import math
from typing import Sequence, Union

Number = Union[int, float]


def normalize_vector_safe(v: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Нормализация вектора через алгебру долей.

    Вместо v / ||v|| (которая ломается на нуле),
    используем: v : Π = to_percentage(v)

    Для v = Ω (0): to_percentage(0) = 0 — Потенциал, не ошибка.
    Для v → Π: to_percentage(Π) = 1 — Полнота, стабильна.
    """
    if isinstance(v, (int, float)):
        norm = abs(v)
        if norm < 1e-10:
            return 0.0
        return v / norm

    # Sequence: per-element normalization
    norm = math.sqrt(sum(x ** 2 for x in v))
    if norm < 1e-10:
        return [0.0] * len(v)
    return [x / norm for x in v]
