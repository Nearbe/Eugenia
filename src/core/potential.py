"""
Potential operators — Проверки и разрешение потенциала (Ω).

Блоки:
- has_potential: проверка наличия структуры
- is_potential: проверка что значение = Ω
- resolve_potential: переход от Скрытого к Явному
"""

from typing import Sequence, Union

from .constants import OMEGA


def has_potential(x: Union[float, int, Sequence[float]]) -> bool:
    """
    Проверка наличия потенциала.

    x ≠ Ω → есть структура (не чистый потенциал)
    x = Ω → чистый потенциал, нет формы
    """
    if isinstance(x, (int, float)):
        return x != OMEGA
    return any(v != OMEGA for v in x)


def is_potential(x) -> bool:
    """
    Проверка: является ли x потенциалом (Ω).

    x = Ω → чистый потенциал
    x ≠ Ω → есть структура
    """
    if isinstance(x, (int, float)):
        return x == OMEGA
    if hasattr(x, "__iter__"):
        return all(v == OMEGA for v in x)
    return x == OMEGA


def resolve_potential(x, default: float = 0.0) -> float:
    """
    Разрешение потенциала.

    Если x = Ω → default (Потенциал схлопывается к значению по умолчанию)
    Иначе → x

    Это не «схлопывание» — это переход от Скрытого к Явному.
    """
    if isinstance(x, (int, float)):
        return default if x == OMEGA else float(x)
    if hasattr(x, "__iter__"):
        if all(v == OMEGA for v in x):
            return default
        for v in x:
            if v != OMEGA:
                return float(v)
        return default
    return default if x == OMEGA else float(x)
