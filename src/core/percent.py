"""
Percentage / Fraction algebra — Алгебра Долей

ℙ = {a : b | b ∉ Ω} — отношение к Полноте.
Это не «числа». Это уровни вовлечённости в Акт.
"""

from numpy import (
    arctanh,
    clip,
    ndarray,
    tanh,
)


def to_percentage(x: ndarray) -> ndarray:
    """
    Преобразование в долю (процент) от Π.

    ℙ = {a : b | b ∉ Ω} — отношение к Полноте.
    Это не «числа». Это уровни вовлечённости в Акт.

    percentage = x / Π → [0, 1]
    Для конечных x: percentage = x / max(|x|, Π)
    Для Π: percentage = 1 (стабильна)

    Args:
        x: Input array of values.

    Returns:
        Array mapped to (−1, 1) via tanh — fraction of Π.
    """
    return clip(tanh(x), -1.0, 1.0)


def from_percentage(p: ndarray) -> ndarray:
    """
    Обратное преобразование: доля → абсолютное значение.

    p ∈ [−1, 1] → x ∈ ℝ
    p = 1  → Π (Полнота)
    p = 0  → Ω (Потенциал)
    p = −1 → −Π

    Args:
        p: Input array of fractions (−1 to 1).

    Returns:
        Array of absolute values.
    """
    return arctanh(clip(p, -0.9999, 0.9999))


def percentage_add(a: ndarray, b: ndarray) -> ndarray:
    """
    Сложение долей: (a:Π) ⊕ (b:Π) = (a⊕b) : Π.

    Сумма вкладов в Полноту.

    Args:
        a: First value.
        b: Second value.

    Returns:
        Sum of fractions mapped back to absolute scale.
    """
    pa = to_percentage(a)
    pb = to_percentage(b)
    return from_percentage(clip(pa + pb, -1, 1))


def percentage_multiply(a: ndarray, b: ndarray) -> ndarray:
    """
    Умножение долей: (a:Π) ⊗ (b:Π) = (a⊗b) : Π.

    Пересечение долей — совместная вовлечённость.

    Args:
        a: First value.
        b: Second value.

    Returns:
        Product of fractions mapped back to absolute scale.
    """
    pa = to_percentage(a)
    pb = to_percentage(b)
    return from_percentage(pa * pb)
