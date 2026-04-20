"""
Complex delta field — Комплексное дельта-поле.

Согласно Essentials [09_Комплексные.md]:
- Система состоит из двух потоков: Скрытого (Im) и Явного (Re)
- z = x + i·y где x ∈ Re, y ∈ Im
- z̄ = x − i·y (комплексное сопряжение)
- ‖z‖² = x² + y² (квадрат нормы)
- (x₁+i·y₁)⊗(x₂+i·y₂) = (x₁x₂−y₁y₂) + i·(x₁y₂+x₂y₁)

Согласно Essentials — Essentials mathematics:
- x = X/255        ← Re (доля яркости)
- y = 1 - X/255    ← Im (доля тьмы)
- Δ = x / y         ← отношение (не разность!)
- Q = exp(Δ)        ← энергия вибрации
"""

from numpy import (
    asarray,
    clip,
    exp,
    float64,
    ndarray,
    tuple,
)


def complex_delta_field(X: ndarray) -> ndarray:
    """
    Комплексное дельта-поле: z = x + i·y.

    x = X/255 (Re — доля яркости)
    y = 1 - X/255 (Im — доля тьмы)
    Δ = x / y (отношение)
    Q = exp(Δ) (энергия вибрации)

    Согласно Essentials — Essentials mathematics.

    Args:
        X: Входные данные (пиксели 0-255)

    Returns:
        Комплексный массив: x + i·y
    """
    X = asarray(X, dtype=float64)
    X_clamped = clip(X, 0, 254.999)
    x = X_clamped / 255.0
    y = 1.0 - x
    return x + 1j * y


def complex_delta_properties(X: ndarray) -> tuple[ndarray, ndarray]:
    """
    Возвращает (delta, Q) для каждого пикселя.

    Δ = x / y (отношение)
    Q = exp(Δ) (энергия вибрации)

    Согласно Essentials — Essentials mathematics.

    Args:
        X: Входные данные (пиксели 0-255)

    Returns:
        Кортеж (delta, Q)
    """
    X = asarray(X, dtype=float64)
    X_clamped = clip(X, 0, 254.999)
    x = X_clamped / 255.0
    y = 1.0 - x
    delta = x / y
    Q = exp(delta)
    return delta, Q
