"""
Complex numbers — z = x + i·y (реальный + мнимый поток).

Комплексные числа: реальный поток (Явное) + мнимый поток (Скрытое).
"""

from typing import Tuple

from numpy import ndarray


def complex_norm(x: ndarray, y: ndarray) -> ndarray:
    """
    Норма комплексного числа: ||z||² = x² + y².

    Общая интенсивность Явного и Скрытого потоков.
    """
    return (x**2 + y**2) ** 0.5


def complex_conjugate(x: ndarray, y: ndarray) -> Tuple[ndarray, ndarray]:
    """
    Сопряжение: z̄ = x − i·y.

    Отражение в Явном потоке.
    """
    return x, -y


def complex_multiply(x1: ndarray, y1: ndarray, x2: ndarray, y2: ndarray) -> Tuple[ndarray, ndarray]:
    """
    Умножение комплексных чисел:

    (x1 + i·y1) ⊗ (x2 + i·y2) = (x1⊗x2 − y1⊗y2) + i·(x1⊗y2 ⊕ x2⊗v1)
    """
    real = x1 * x2 - y1 * y2
    imag = x1 * y2 + x2 * y1
    return real, imag
