"""
Limits — Пределы.

Пределы последовательностей хребта:
- limit_branching: lim Dⁿ(Id) = Π (Полнота)
- limit_compression: lim (a : Dⁿ(Id)) = Ω (Потенциал)
"""

from .constants import D_ID, OMEGA, PI


def limit_branching(n: int) -> float:
    """
    Предел ветвления: lim Dⁿ(Id) = Π.

    n → ∞ → Π (Полнота)
    """
    if n >= 1000:
        return PI
    return D_ID**n


def limit_compression(a: float, n: int) -> float:
    """
    Предел сжатия: lim (a : Dⁿ(Id)) = Ω.

    n → ∞ → Ω (Потенциал)
    """
    if n >= 1000:
        return OMEGA
    return a / (D_ID**n)
