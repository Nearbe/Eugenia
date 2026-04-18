"""
Vector normalization — Нормализация векторов.

normalize_vector_safe — векторная нормализация на алгебре долей.
Вместо v / ||v|| (которая ломается на нуле),
используем: v : Π = to_percentage(v)
"""

from numpy import (
    any,
    linalg,
    ndarray,
    zeros_like,
)


def normalize_vector_safe(v: ndarray) -> ndarray:
    """
    Нормализация вектора через алгебру долей.

    Вместо v / ||v|| (которая ломается на нуле),
    используем: v : Π = to_percentage(v)

    Для v = Ω (0): to_percentage(0) = 0 — Потенциал, не ошибка.
    Для v → Π: to_percentage(Π) = 1 — Полнота, стабильна.
    """
    if v.ndim == 1:
        norm = linalg.norm(v)
        if norm < 1e-10:
            return zeros_like(v, dtype=float)
        return v / norm

    # 2D+ batch: per-row normalization
    norm = linalg.norm(v, axis=-1)
    mask_zero = norm < 1e-10

    result = zeros_like(v, dtype=float)
    if any(~mask_zero):
        result[~mask_zero] = v[~mask_zero] / norm[~mask_zero, None]

    return result
