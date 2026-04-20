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

import math
from typing import Sequence, Tuple, Union

Number = Union[int, float]


def _clip(val: float, lo: float, hi: float) -> float:
    """Pure Python clip."""
    if val < lo:
        return lo
    if val > hi:
        return hi
    return val


def complex_delta_field(X: Union[Number, Sequence[Number]]) -> Union[complex, list[complex]]:
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
    if isinstance(X, (int, float)):
        x_clamped = _clip(float(X), 0, 254.999)
        x = x_clamped / 255.0
        y = 1.0 - x
        return complex(x, y)
    return [
        complex(float(x) / 255.0, 1.0 - float(x) / 255.0)
        for x in X
    ]


def complex_delta_properties(X: Union[Number, Sequence[Number]]) -> Tuple[Union[float, list[float]], Union[float, list[float]]]:
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
    if isinstance(X, (int, float)):
        x_clamped = _clip(float(X), 0, 254.999)
        x = x_clamped / 255.0
        y = 1.0 - x
        delta = x / y
        Q = math.exp(delta)
        return delta, Q
    deltas = []
    Qs = []
    for x in X:
        x_clamped = _clip(float(x), 0, 254.999)
        x_val = x_clamped / 255.0
        y = 1.0 - x_val
        delta = x_val / y
        deltas.append(delta)
        Qs.append(math.exp(delta))
    return deltas, Qs


def inverse_complex_delta_field(z: Union[complex, Sequence[complex]]) -> Union[float, list[float]]:
    """
    Обратное преобразование комплексного делья-поля: z → X.

    Из z = x + i·y где x = X/255, y = 1 - X/255:
    X = 255 · Re(z) / (Re(z) + Im(z))

    Args:
        z: Комплексный массив (x + i·y).

    Returns:
        Массив X ∈ [0, 255].
    """
    if isinstance(z, complex):
        real = z.real
        imag = z.imag
        denom = real + imag
        denom = denom if denom != 0 else 1e-300
        X = 255.0 * real / denom
        return _clip(X, 0, 255.0)
    results = []
    for c in z:
        real = c.real
        imag = c.imag
        denom = real + imag
        denom = denom if denom != 0 else 1e-300
        X = 255.0 * real / denom
        results.append(_clip(X, 0, 255.0))
    return results
