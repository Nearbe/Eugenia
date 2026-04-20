"""
Ridge (Хребет) → Percentage Mapping.

Хребет — опорные узлы фрактала:
  0 = Ω (Потенциал)
  1 = Id (Единство)
  2 = D(Id) (первое ветвление)
  ∞ = Π (предел ветвления)
  100% = Π (в процентах)

Π = 100% — предел последовательности Dⁿ(Id).
Это связь между хребтом (дискретная Dⁿ) и алгеброй долей (непрерывный [0%, 100%]).

Функции:
- ridge_level: номер уровня хребта log2(|x|)
- ridge_to_percentage: хребт → проценты (sigmoid)
- percentage_to_ridge: проценты → хребт (inverse sigmoid)
- spine_value: значение на хребте Dⁿ(Id) = 2ⁿ
- spine_value_array: массив значений хребта
"""

import math
from typing import Sequence, Union

from .constants import D_ID, OMEGA, PI

Number = Union[int, float]
_INFINITY = float("inf")


def ridge_level(x: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Номер уровня хребта для данного значения.

    ridge_level(x) = L(x) = log2(|x|) — сколько раз нужно применить D
    (ветвление) к Id=1, чтобы достичь x.

    Alias: L(x) — для совместимости с Essentials [08_Логарифм.md].
    """
    if isinstance(x, (int, float)):
        return _ridge_level_scalar(float(x))
    return [_ridge_level_scalar(float(v)) for v in x]


def L(x: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Логарифм ( branching depth counter ) — alias для ridge_level.

    L(x) = log2(|x|) — номер уровня Хребта.
    L(Ω) = −inf, L(Id) = 0, L(Dⁿ(Id)) = n, L(Π) = +inf.

    Essentials [08_Логарифм.md]: "Логарифм определяет, сколько тактов
    Ветвления (:Ω) потребовалось для достижения состояния a".

    Args:
        x: Входные значения (array-like или ndarray).

    Returns:
        log2(|x|) для каждого элемента.
    """
    return ridge_level(x)


def _ridge_level_scalar(x: float) -> float:
    """Scalar implementation of ridge level."""
    if x == OMEGA:
        return -_INFINITY
    return math.log2(abs(x) + 1e-300)


def ridge_to_percentage(n: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Отображение хребта в проценты.

    ridge_to_percentage(n) = sigmoid(n − c) × 100%

    Где c — центр сигмоиды:
    - n = −inf → 0% (Ω — Потенциал)
    - n = 0  → 50% (Id — Единство)
    - n = +inf → 100% (Π — Полнота)

    Параметр steepness=1.0: стандартный сигмоид.
    """
    if isinstance(n, (int, float)):
        return _ridge_to_percentage_scalar(float(n))
    return [_ridge_to_percentage_scalar(float(v)) for v in n]


def _ridge_to_percentage_scalar(n: float) -> float:
    """Scalar sigmoid mapping."""
    if n >= 1000:
        return 100.0
    if n <= -1000:
        return 0.0
    center = 0.0
    steepness = 1.0
    exp_arg = -steepness * (n - center)
    # Compute 2^(-exp_arg) manually to avoid overflow
    if exp_arg > 700:
        return 0.0
    if exp_arg < -700:
        return 100.0
    return 100.0 / (1.0 + 2.0 ** exp_arg)


def percentage_to_ridge(pct: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Обратное отображение: проценты → уровень хребта.

    percentage_to_ridge(p) = log(p / (100 - p)) / ln(2)

    p = 0%   → −inf (Ω)
    p = 50%  → 0  (Id)
    p = 100% → +inf (Π)
    """
    if isinstance(pct, (int, float)):
        return _percentage_to_ridge_scalar(float(pct))
    return [_percentage_to_ridge_scalar(float(p)) for p in pct]


def _percentage_to_ridge_scalar(p: float) -> float:
    """Scalar inverse sigmoid mapping."""
    p_clipped = max(p, 1e-300)
    p_clipped = min(p_clipped, 99.9999999)
    odds = p_clipped / (100.0 - p_clipped)
    return math.log2(odds)


def spine_value(n: int) -> float:
    """
    Значение на хребте для уровня n.

    spine_value(n) = Dⁿ(Id) = 2ⁿ

    n=0: 1 (Id)
    n=1: 2 (D(Id))
    n=2: 4 (D²(Id))
    ...
    n→inf: Π (предел)
    """
    if n >= 1000:
        return float(PI)
    return D_ID ** n


def spine_value_array(max_n: int) -> list[float]:
    """
    Массив значений хребта от 0 до max_n.

    spine_array = [D⁰(Id), D¹(Id), D²(Id), ..., Dⁿ(Id)]
                = [1, 2, 4, 8, ..., 2ⁿ]
    """
    return [D_ID ** n for n in range(max_n + 1)]
