"""
Dual numbers — Z = x + v·ε (форма + скорость).

Дуальные числа: форма (Явное) + скорость/потенциал (Скрытое).
ε² = Ω — ускорение пренебрежимо.
"""

from typing import Tuple

from numpy import ndarray

from .branching import D, H


def dual_form(x: ndarray, v: ndarray) -> Tuple[ndarray, ndarray]:
    """
    Создание дуального числа: Z = x + v·ε.

    x — Текущая Форма (Явное).
    v — Потенциал Роста (Скрытое).
    ε² = Ω — ускорение пренебрежимо.

    L(v) = x · L(D(Id)) — скорость связана с позицией.
    """
    return x, v


def dual_multiply(x1: ndarray, v1: ndarray, x2: ndarray, v2: ndarray) -> Tuple[ndarray, ndarray]:
    """
    Умножение дуальных чисел:

    (x1 + v1·ε) ⊗ (x2 + v2·ε) = (x1⊗x2) + (x1⊗v2 ⊕ x2⊗v1)·ε
    """
    x_result = x1 * x2
    v_result = x1 * v2 + x2 * v1
    return x_result, v_result


def dual_branch(x: ndarray, v: ndarray) -> Tuple[ndarray, ndarray]:
    """
    Ветвление дуального числа:

    (x + v·ε) : Ω = D(x) + D(v)·ε
    """
    return D(x), D(v)


def dual_compress(x: ndarray, v: ndarray) -> Tuple[ndarray, ndarray]:
    """
    Сжатие дуального числа:

    (x + v·ε) : D(Id) = (x:D(Id)) + (v:D(Id))·ε
    """
    return H(x), H(v)
