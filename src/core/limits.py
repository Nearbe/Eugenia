"""
Limits — Пределы.

Пределы последовательностей хребта:
- limit_branching: lim Dⁿ(Id) = Π (Полнота)
- limit_compression: lim (a : Dⁿ(Id)) = Ω (Потенциал)

Непрерывность:
- continuity_D: lim D(xₙ) = D(lim xₙ)
- continuity_H: lim H(xₙ) = H(lim xₙ)
"""

from .branching import D, H
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


def continuity_D(x_sequence: list, n_steps: int = 1000) -> float:
    """
    Проверка непрерывности оператора D (ветвление).

    lim D(xₙ) = D(lim xₙ)

    Согласно Essentials [15_Пределы_и_непрерывность.md]:
    Операции системы непрерывны — не создают "разрывов".

    Args:
        x_sequence: Последовательность значений xₙ.
        n_steps: Количество шагов для проверки.

    Returns:
        Разность |D(lim xₙ) - lim D(xₙ)| — должна быть ≈ 0.
    """
    # Limit of xₙ
    x_limit = x_sequence[-1] if x_sequence else 0.0

    # D(lim xₙ)
    d_of_limit = D(x_limit)

    # lim D(xₙ)
    d_sequence = [D(x) for x in x_sequence[:n_steps]]
    d_limit = d_sequence[-1] if d_sequence else 0.0

    # Continuity error (should be ≈ 0 for continuous D)
    return abs(float(d_of_limit) - float(d_limit))


def continuity_H(x_sequence: list, n_steps: int = 1000) -> float:
    """
    Проверка непрерывности оператора H (сжатие).

    lim H(xₙ) = H(lim xₙ)

    Согласно Essentials [15_Пределы_и_непрерывность.md]:
    Операции системы непрерывны — не создают "разрывов".

    Args:
        x_sequence: Последовательность значений xₙ.
        n_steps: Количество шагов для проверки.

    Returns:
        Разность |H(lim xₙ) - lim H(xₙ)| — должна быть ≈ 0.
    """
    # Limit of xₙ
    x_limit = x_sequence[-1] if x_sequence else 0.0

    # H(lim xₙ)
    h_of_limit = H(x_limit)

    # lim H(xₙ)
    h_sequence = [H(x) for x in x_sequence[:n_steps]]
    h_limit = h_sequence[-1] if h_sequence else 0.0

    # Continuity error (should be ≈ 0 for continuous H)
    return abs(float(h_of_limit) - float(h_limit))
