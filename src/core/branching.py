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

from numpy import ndarray

from .constants import D_ID


def D(x: ndarray) -> ndarray:
    """
    Ветвление (Branching): D(a) = a : Ω = a ⊕ a.

    Args:
        x: Input array of values.

    Returns:
        Doubled values (x * 2).
    """

    return x * D_ID


def H(x: ndarray) -> ndarray:
    """
    Сжатие (Compression): H(a) = a : D(Id).

    Args:
        x: Input array of values.

    Returns:
        Halved values (x / 2).
    """
    return x / D_ID
