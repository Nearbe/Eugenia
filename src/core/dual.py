"""
Dual numbers — Z = x + v·ε (форма + скорость).

Дуальные числа: форма (Явное) + скорость/потенциал (Скрытое).
ε² = Ω — ускорение пренебрежимо.

Согласно Essentials [14_Дуальные_числа.md]:
- Z = x + v·ε
- (x₁+v₁ε) ⊕ (x₂+v₂ε) = (x₁⊕x₂) + (v₁⊕v₂)ε  — сложение
- (x₁+v₁ε) ⊗ (x₂+v₂ε) = (x₁⊗x₂) + (x₁⊗v₂ ⊕ x₂⊗v₁)ε  — умножение
- (x+vε) : Ω = D(x) + D(v)ε  — ветвление
- (x+vε) : D(Id) = (x:D(Id)) + (v:D(Id))ε  — сжатие
- Zⁿ = xⁿ + n·xⁿ⁻¹·v·ε  — степень
- f(Z) = f(x) + f'(x)·v·ε  — автоматическое дифференцирование
"""

from typing import Sequence, Tuple, Union

from .branching import D, H

Number = Union[int, float]
NDArray = Union[Sequence[float], float]


def dual_form(x: Union[Number, Sequence[Number]], v: Union[Number, Sequence[Number]]) -> Tuple[Union[float, list[float]], Union[float, list[float]]]:
    """
    Создание дуального числа: Z = x + v·ε.

    x — Текущая Форма (Явное).
    v — Потенциал Роста (Скрытое).
    ε² = Ω — ускорение пренебрежимо.

    Args:
        x: Форма (текущее значение).
        v: Скорость (потенциал роста).

    Returns:
        Tuple (x, v) representing Z = x + v·ε.
    """
    return x, v


def dual_add(x1: NDArray, v1: NDArray, x2: NDArray, v2: NDArray) -> Tuple[NDArray, NDArray]:
    """
    Сложение дуальных чисел:

    (x₁ + v₁·ε) ⊕ (x₂ + v₂·ε) = (x₁ ⊕ x₂) + (v₁ ⊕ v₂)·ε

    Согласно Essentials [14_Дуальные_числа.md]:
    Сумма форм и импульсов.

    Args:
        x1: Real part of first number.
        v1: Infinitesimal part of first number.
        x2: Real part of second number.
        v2: Infinitesimal part of second number.

    Returns:
        Tuple (x_sum, v_sum).
    """
    if isinstance(x1, (int, float)) and isinstance(x2, (int, float)):
        return x1 + x2, v1 + v2
    x_sum = [a + b for a, b in zip(x1, x2)]
    v_sum = [a + b for a, b in zip(v1, v2)]
    return x_sum, v_sum


def dual_multiply(x1: NDArray, v1: NDArray, x2: NDArray, v2: NDArray) -> Tuple[NDArray, NDArray]:
    """
    Умножение дуальных чисел:

    (x₁ + v₁·ε) ⊗ (x₂ + v₂·ε) = (x₁·x₂) + (x₁·v₂ + x₂·v₁)·ε

    Согласно Essentials [14_Дуальные_числа.md]:
    Формы перемножаются, скорости складываются с учётом перекрёстных членов.

    Args:
        x1: Real part of first number.
        v1: Infinitesimal part of first number.
        x2: Real part of second number.
        v2: Infinitesimal part of second number.

    Returns:
        Tuple (x_prod, v_prod).
    """
    if isinstance(x1, (int, float)) and isinstance(x2, (int, float)):
        x_result = x1 * x2
        v_result = x1 * v2 + x2 * v1
        return x_result, v_result
    x_result = [a * b for a, b in zip(x1, x2)]
    v_result = [a * b2 + b * a2 for a, b, a2, b2 in zip(x1, v2, x2, v1)]
    return x_result, v_result


def dual_branch(x: NDArray, v: NDArray) -> Tuple[NDArray, NDArray]:
    """
    Ветвление дуального числа:

    (x + v·ε) : Ω = D(x) + D(v)·ε

    Согласно Essentials [14_Дуальные_числа.md]:
    Масштабируется и форма, и скорость.

    Args:
        x: Форма.
        v: Скорость.

    Returns:
        Tuple (D(x), D(v)).
    """
    return D(x), D(v)


def dual_compress(x: NDArray, v: NDArray) -> Tuple[NDArray, NDArray]:
    """
    Сжатие дуального числа:

    (x + v·ε) : D(Id) = (x:D(Id)) + (v:D(Id))·ε

    Согласно Essentials [14_Дуальные_числа.md]:
    Возврат по обоим компонентам.

    Args:
        x: Форма.
        v: Скорость.

    Returns:
        Tuple (H(x), H(v)).
    """
    return H(x), H(v)


def dual_power(x: NDArray, v: NDArray, n: int) -> Tuple[NDArray, NDArray]:
    """
    Степень дуального числа:

    Zⁿ = (x + v·ε)ⁿ = xⁿ + n·xⁿ⁻¹·v·ε

    Согласно Essentials [14_Дуальные_числа.md]:
    Формула для степени дуального числа.

    Args:
        x: Real part.
        v: Infinitesimal part.
        n: Integer exponent.

    Returns:
        Tuple (real_part, infinitesimal_part) of Zⁿ.
    """
    if isinstance(x, (int, float)):
        x_result = x ** n
        v_result = n * (x ** (n - 1)) * v
        return x_result, v_result
    x_result = [xi ** n for xi in x]
    v_result = [n * (xi ** (n - 1)) * vi for xi, vi in zip(x, v)]
    return x_result, v_result


def dual_func(x: NDArray, v: NDArray, f, df) -> Tuple[NDArray, NDArray]:
    """
    Автоматическое дифференцирование дуальных чисел:

    f(Z) = f(x + v·ε) = f(x) + f'(x)·v·ε

    Согласно Essentials [14_Дуальные_числа.md]:
    Коэффициент при ε после применения функции — это f'(x)·v.

    Args:
        x: Real part.
        v: Infinitesimal part.
        f: Function to apply (acts on real part).
        df: Derivative of f (acts on real part).

    Returns:
        Tuple (f(x), f'(x)·v).
    """
    return f(x), df(x) * v
