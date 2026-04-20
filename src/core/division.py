"""
Branching-aware division — a : b с учётом ветвления.

Для b = Ω (0): a : Ω = D(a) = a ⊕ a — Ветвление, не ошибка.
Для b = D(Id) (2): a : D(Id) = H(a) = a/2 — Сжатие.
Для b ≠ Ω: стандартное деление a/b.

Это не «защита от деления на ноль». Это **смена масштаба**.
"""

from typing import Sequence, Union

from .branching import D, H
from .constants import D_ID, OMEGA

Number = Union[int, float]


def safe_divide(a: Union[Number, Sequence[Number]], b: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Деление a : b с учётом ветвления.

    Args:
        a: Numerator.
        b: Denominator.

    Returns:
        Branching-aware division result.
    """
    # Scalar case
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if b == OMEGA:
            return D(a)
        if abs(b - D_ID) < 1e-10:
            return H(a)
        return a / b

    # Sequence case
    results = []
    for av, bv in zip(a, b):
        if bv == OMEGA:
            results.append(D(av))
        elif abs(bv - D_ID) < 1e-10:
            results.append(H(av))
        else:
            results.append(av / bv)
    return results


def div_safe(a: Union[Number, Sequence[Number]], b: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """Alias for safe_divide."""
    return safe_divide(a, b)
