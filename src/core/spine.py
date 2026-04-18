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

from numpy import (
    abs,
    arange,
    asarray,
    clip,
    exp,
    float64,
    full_like,
    inf,
    log,
    log2,
    ndarray,
)

from core.constants import D_ID, OMEGA, PI


def ridge_level(x: ndarray) -> ndarray:
    """
    Номер уровня хребта для данного значения.

    ridge_level(x) = L(x) = log2(|x|) — сколько раз нужно применить D
    (ветвление) к Id=1, чтобы достичь x.

    ridge_level(Ω) = −∞
    ridge_level(Id) = 0
    ridge_level(Dⁿ(Id)) = n
    ridge_level(Π) = +∞
    """
    result = full_like(x, -inf, dtype=float64)
    mask = x != OMEGA
    result[mask] = log2(abs(x[mask]) + 1e-300)
    return result


def ridge_to_percentage(n: ndarray) -> ndarray:
    """
    Отображение хребта в проценты.

    ridge_to_percentage(n) = sigmoid(n − c) × 100%

    Где c — центр сигмоиды:
    - n = −∞ → 0% (Ω — Потенциал)
    - n = 0  → 50% (Id — Единство)
    - n = +∞ → 100% (Π — Полнота)

    Параметр steepness=1.0: стандартный сигмоид.
    """
    n = asarray(n, dtype=float64)
    center = 0.0  # Id = 50%
    steepness = 1.0
    return 100.0 / (1.0 + exp(-steepness * (n - center)))


def percentage_to_ridge(pct: ndarray) -> ndarray:
    """
    Обратное отображение: проценты → уровень хребта.

    percentage_to_ridge(p) = log(p / (100 - p)) / ln(2)

    p = 0%   → −∞ (Ω)
    p = 50%  → 0  (Id)
    p = 100% → +∞ (Π)
    """
    pct = asarray(pct, dtype=float64)
    p_clipped = clip(pct, 1e-300, 99.9999999)
    odds = p_clipped / (100.0 - p_clipped)
    return log(odds)


def spine_value(n: int) -> float:
    """
    Значение на хребте для уровня n.

    spine_value(n) = Dⁿ(Id) = 2ⁿ

    n=0: 1 (Id)
    n=1: 2 (D(Id))
    n=2: 4 (D²(Id))
    ...
    n→∞: Π (предел)
    """
    if n >= 1000:
        return float(PI)
    return D_ID**n


def spine_value_array(max_n: int = 10) -> ndarray:
    """
    Массив значений хребта от 0 до max_n.

    spine_array = [D⁰(Id), D¹(Id), D²(Id), ..., Dⁿ(Id)]
                = [1, 2, 4, 8, ..., 2ⁿ]
    """
    n = arange(max_n + 1, dtype=float64)
    return D_ID**n
