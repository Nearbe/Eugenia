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

from numpy import abs, ndarray, sqrt, sum

from .spine import L


def delta_distance(a: ndarray, b: ndarray) -> ndarray:
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
    return abs(La - Lb)


def euclidean_distance(a: ndarray, b: ndarray) -> ndarray:
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
    diff = a - b
    return sqrt(sum(diff**2, axis=-1))
