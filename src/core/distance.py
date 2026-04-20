"""
Distance functions — на логарифмической шкале Хребта.

delta_distance(a, b) — расстояние между состояниями на логарифмической шкале.
    d(a, b) = |L(a) − L(b)|
    Для дельта-поля: D = log(X+1) - log(256-X)
    Это уже логарифмическая шкала — расстояние = |D₁ - D₂|.

euclidean_distance(a, b) — стандартное евклидово расстояние.
    d(a, b) = sqrt(sum((a-b)²))
    Внимание: не учитывает ветвление. Используйте delta_distance
    для дельта-поля и других логарифмических представлений.
"""

import math
from typing import Sequence, Union

from .spine import L

Number = Union[int, float]


def delta_distance(a: Union[Number, Sequence[Number]], b: Union[Number, Sequence[Number]]) -> Union[float, list[float]]:
    """
    Расстояние между состояниями на логарифмической шкале Хребта.

    В отличие от евклидова расстояния (которое не учитывает ветвление),
    это расстояние по уровням D:

    d(a, b) = |L(a) − L(b)|

    Args:
        a: First state.
        b: Second state.

    Returns:
        Distance on the logarithmic spine scale.
    """
    La = L(a)
    Lb = L(b)
    if isinstance(La, (int, float)) and isinstance(Lb, (int, float)):
        return abs(La - Lb)
    # Element-wise distance
    if isinstance(La, list) and isinstance(Lb, list):
        return [abs(x - y) for x, y in zip(La, Lb)]
    return abs(La - Lb)


def euclidean_distance(a: Union[Number, Sequence[Number]], b: Union[Number, Sequence[Number]]) -> float:
    """
    Евклидово расстояние — стандартное, для сравнения.

    d(a, b) = sqrt(sum((a-b)²))

    Внимание: не учитывает ветвление. Используйте delta_distance
    для дельта-поля и других логарифмических представлений.

    Args:
        a: First vector.
        b: Second vector.

    Returns:
        Euclidean distance.
    """
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.sqrt((a - b) ** 2)
    diff = [float(x) - float(y) for x, y in zip(a, b)]
    return math.sqrt(sum(d ** 2 for d in diff))
