"""
Potential operators — Проверки и разрешение потенциала (Ω).

Блоки:
- has_potential: проверка наличия структуры
- is_potential: проверка что значение = Ω
- resolve_potential: переход от Скрытого к Явному
"""

from numpy import (
    all,
    any,
    ndarray,
    where,
)

from .constants import OMEGA


def has_potential(x: ndarray) -> bool:
    """
    Проверка наличия потенциала.

    x ≠ Ω → есть структура (не чистый потенциал)
    x = Ω → чистый потенциал, нет формы
    """
    return bool(any(x != OMEGA))


def is_potential(x) -> bool:
    """
    Проверка: является ли x потенциалом (Ω).

    x = Ω → чистый потенциал
    x ≠ Ω → есть структура
    """
    if isinstance(x, ndarray):
        return bool(all(x == OMEGA))
    return x == OMEGA


def resolve_potential(x, default: float = 0.0) -> float:
    """
    Разрешение потенциала.

    Если x = Ω → default (Потенциал схлопывается к значению по умолчанию)
    Иначе → x

    Это не «схлопывание» — это переход от Скрытого к Явному.
    """
    if isinstance(x, ndarray):
        if all(x == OMEGA):
            return default
        return float(where(x == OMEGA, default, x).flat[0])
    return default if x == OMEGA else float(x)
