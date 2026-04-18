"""
Delta field operators — Операторы дельта-поля.

Дельта-поле: D = log(X+1) - log(256-X)
Отображает X ∈ [0, 255] в D ∈ [-5.546, 5.546].

256 = 2⁸ = D⁸(Id) — 8 уровней ветвления.
"""

from numpy import (
    asarray,
    clip,
    exp,
    float64,
    log,
    ndarray,
)


def delta_field(X: ndarray) -> ndarray:
    """
    Дельта-поле: D = log(X+1) - log(256-X).

    Отображает X ∈ [0, 255] в D ∈ [-5.546, 5.546].

    D = +5.546 при X=255 → ветвление (a:Ω)
    D = −5.546 при X=0 → сжатие (a:D(Id)⁸)
    D = 0 при X=127.5 → mid-gray, баланс

    256 = 2⁸ = D⁸(Id) — 8 уровней ветвления.
    """
    X = asarray(X, dtype=float64)
    X_clamped = clip(X, 0, 254.999)
    return log(X_clamped + 1.0) - log(256.0 - X_clamped)


def inverse_delta_field(D: ndarray) -> ndarray:
    """
    Обратное отображение: D → X.

    D = log(X+1) - log(256-X)
    X = (256*e^D - 1) / (e^D + 1)
    """
    D = asarray(D, dtype=float64)
    exp_D = exp(D)
    return (256.0 * exp_D - 1.0) / (exp_D + 1.0)
