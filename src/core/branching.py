"""
Branching (D) and Compression (H)

Branching (Ветвление): D(a) = a : Ω = a ⊕ a
    Удвоение состояния — переход на следующий уровень Хребта.
    Деление на Ω не является ошибкой — это акт создания различия.
    D(a) = 2a (в арифметике)
    L(D(a)) = L(a) + 1

Compression (Сжатие): H(a) = a : D(Id)
    Обратный процесс ветвлению — спуск на уровень.
    H(D(a)) = a, D(H(a)) = a.
    H(a) = a / 2 (в арифметике)
    L(H(a)) = L(a) - 1
"""

from typing import Sequence, Union

from .constants import D_ID

Number = Union[int, float]


def D(x: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Ветвление (Branching): D(a) = a : Ω = a ⊕ a.

    Args:
        x: Input scalar or sequence of values.

    Returns:
        Doubled values (x * 2).
    """
    if isinstance(x, (int, float)):
        return x * D_ID
    return [v * D_ID for v in x]


def H(x: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Сжатие (Compression): H(a) = a : D(Id).

    Args:
        x: Input scalar or sequence of values.

    Returns:
        Halved values (x / 2).
    """
    if isinstance(x, (int, float)):
        return x / D_ID
    return [v / D_ID for v in x]
