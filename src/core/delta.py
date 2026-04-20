"""
Delta field operators — Операторы дельта-поля.

Дельта-поле: D = log2(X+1) - log2(256-X)
Отображает X ∈ [0, 255] в D ∈ [-8, 8].

256 = 2⁸ = D⁸(Id) — 8 уровней ветвления.
L(256) = log2(256) = 8 — глубина рекурсии Хребта.
"""

from numpy import (
    asarray,
    clip,
    exp2,
    float64,
    log2,
    ndarray,
)


def delta_field(X: ndarray) -> ndarray:
    """
    Дельта-поле: D = log2(X+1) - log2(256-X).

    Отображает X ∈ [0, 255] в D ∈ [-8, 8].

    D = +8 при X=255 → ветвление (a:Ω), 8 уровней глубины
    D = −8 при X=0 → сжатие (a:D(Id)⁸)
    D = 0 при X=127.5 → mid-gray, баланс

    256 = 2⁸ = D⁸(Id) — 8 уровней ветвления (Хребет).
    L(256) = log2(256) = 8 — информация по Essentials [30_Информация.md].
    """
    X = asarray(X, dtype=float64)
    X_clamped = clip(X, 0, 254.999)
    return log2(X_clamped + 1.0) - log2(256.0 - X_clamped)


def inverse_delta_field(D: ndarray) -> ndarray:
    """
    Обратное отображение: D → X.

    D = log2(X+1) - log2(256-X)
    X = (256*2^D - 1) / (2^D + 1)
    """
    D = asarray(D, dtype=float64)
    exp_D = exp2(D)  # 2^D, not e^D — inverse of log2
    return (256.0 * exp_D - 1.0) / (exp_D + 1.0)
