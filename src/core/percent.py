"""
Percentage / Fraction algebra — Алгебра Долей

ℙ = {a : b | b ∉ Ω} — отношение к Полноте.
Это не «числа». Это уровни вовлечённости в Акт.

Реализация через spine mapping:
- to_percentage(x) = ridge_to_percentage(ridge_level(x))
  maps x ∈ ℝ → [0%, 100%] via log2 spine scale
- from_percentage(pct) = percentage_to_ridge(pct)
  maps [0%, 100%] → ℝ

This is consistent with Essentials [12_Алгебра_процентов.md]:
- Π = 100% (limit of branching)
- Id = 50% (spine level 0)
- Ω = 0% (spine level -∞)
"""

from typing import Sequence, Union

from .spine import percentage_to_ridge, ridge_level, ridge_to_percentage

Number = Union[int, float]


def to_percentage(x: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Преобразование в долю (процент) от Π.

    to_percentage(x) = ridge_to_percentage(ridge_level(x))

    x = Ω (0)     → 0%   (спин-уровень −∞)
    x = Id (1)    → 50%  (спин-уровень 0)
    x = Dⁿ(Id)    → 50·sigmoid(n)%  (спин-уровень n)
    x = Π (∞)     → 100% (спин-уровень +∞)

    Это согласовано с Essentials [12_Алгебра_процентов.md]:
    ℙ = {a : b | b ∉ Ω} — отношение к Полноте.

    Args:
        x: Входные значения.

    Returns:
        Array mapped to [0, 100] — percentage of Π.
    """
    return ridge_to_percentage(ridge_level(x))


def from_percentage(pct: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Обратное преобразование: проценты → абсолютное значение.

    from_percentage(p) = percentage_to_ridge(p)

    p = 0%   → −inf (Ω)
    p = 50%  → 0  (Id in spine level)
    p = 100% → +inf (Π)

    Args:
        pct: Input array of percentages (0 to 100).

    Returns:
        Array of spine levels (log2 scale).
    """
    if isinstance(pct, (int, float)):
        return percentage_to_ridge(max(min(float(pct), 100.0), 0.0))
    return [percentage_to_ridge(max(min(float(p), 100.0), 0.0)) for p in pct]  # type: ignore[misc]


def percentage_add(
    a: Union[Number, Sequence[Number]], b: Union[Number, Sequence[Number]]
) -> Union[float, list[float]]:
    """
    Сложение долей: (a:Π) ⊕ (b:Π) = (a⊕b) : Π.

    Сумма вкладов в Полноту.

    В spine terms: сложение на линейной шкале спин-уровней.
    L(a) + L(b) → ridge level of product.

    Args:
        a: First value (in spine level or absolute).
        b: Second value (in spine level or absolute).

    Returns:
        Sum in percentage space mapped back to absolute scale.
    """
    pa = to_percentage(a)
    pb = to_percentage(b)
    # Convert percentages to spine levels, add, convert back
    sa = percentage_to_ridge(pa)
    sb = percentage_to_ridge(pb)
    s_sum = sa + sb  # type: ignore[operator]
    # Map back: spine level → absolute value = 2^spine_level
    return 2.0**s_sum


def percentage_multiply(
    a: Union[Number, Sequence[Number]], b: Union[Number, Sequence[Number]]
) -> Union[float, list[float]]:
    """
    Умножение долей: (a:Π) ⊗ (b:Π) = (a⊗b) : Π.

    Пересечение долей — совместная вовлечённость.

    В spine terms: умножение на линейной шкале спин-уровней = сложение логарифмов.
    L(a·b) = L(a) + L(b).

    Args:
        a: First value.
        b: Second value.

    Returns:
        Product in percentage space mapped back to absolute scale.
    """
    pa = to_percentage(a)
    pb = to_percentage(b)
    # In log-space, multiplication = addition
    sa = percentage_to_ridge(pa)
    sb = percentage_to_ridge(pb)
    # Geometric mean: average of log-spaces
    s_mean = (sa + sb) / 2.0  # type: ignore[operator]
    return 2.0**s_mean
