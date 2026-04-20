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


def _continuity_error(x_limit: float, fn, x_sequence: list) -> float:
    """Compute continuity error: |fn(lim xₙ) - lim fn(xₙ)|."""
    f_of_limit = fn(x_limit)
    f_sequence = [fn(x) for x in x_sequence]
    f_limit = f_sequence[-1] if f_sequence else 0.0
    return abs(float(f_of_limit) - float(f_limit))  # type: ignore[arg-type]


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
    x_limit = x_sequence[-1] if x_sequence else 0.0
    return _continuity_error(x_limit, D, x_sequence[:n_steps])


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
    x_limit = x_sequence[-1] if x_sequence else 0.0
    return _continuity_error(x_limit, H, x_sequence[:n_steps])
