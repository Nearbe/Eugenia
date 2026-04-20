"""
Complex numbers — z = x + i·y (реальный + мнимый поток).

Комплексные числа: реальный поток (Явное) + мнимый поток (Скрытое).
Согласно Essentials [09_Комплексные.md]:
- z = x + i·y где x ∈ Re, y ∈ Im
- z̄ = x − i·y (комплексное сопряжение)
- ‖z‖ = √(x² + y²) (норма)
- ‖z‖² = x² + y² (квадрат нормы)
- (x₁+i·y₁)⊗(x₂+i·y₂) = (x₁x₂−y₁y₂) + i(x₁y₂+x₂y₁)
- z : Ω = D(x) + i·D(y) (ветвление)
- z : D(Id) = (x:D(Id)) + i·(y:D(Id)) (сжатие)
- z · e^(i·θ) = (x·cos(θ) − y·sin(θ)) + i(x·sin(θ) + y·cos(θ)) (вращение)
"""

import math
from typing import Sequence, Tuple, Union

Number = Union[int, float]


def complex_norm(
    x: Union[Number, Sequence[Number]], y: Union[Number, Sequence[Number]]
) -> Union[float, list[float]]:
    """
    Норма комплексного числа: ‖z‖ = √(x² + y²).

    Общая интенсивность Явного и Скрытого потоков.

    Note: Docstring previously claimed ‖z‖² but code returned ‖z‖.
    This function returns ‖z‖ (square root). For ‖z‖², use complex_norm_squared.

    Args:
        x: Real part.
        y: Imaginary part.

    Returns:
        Norm ‖z‖ = √(x² + y²).
    """
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return math.sqrt(x**2 + y**2)
    return [math.sqrt(xi**2 + yi**2) for xi, yi in zip(x, y)]  # type: ignore[arg-type]


def complex_norm_squared(
    x: Union[Number, Sequence[Number]], y: Union[Number, Sequence[Number]]
) -> Union[float, list[float]]:
    """
    Квадрат нормы комплексного числа: ‖z‖² = x² + y².

    Согласно Essentials [09_Комплексные.md]:
    ‖z‖² = x² + y² — общая интенсивность.

    Args:
        x: Real part.
        y: Imaginary part.

    Returns:
        Squared norm ‖z‖² = x² + y².
    """
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return x**2 + y**2
    return [xi**2 + yi**2 for xi, yi in zip(x, y)]  # type: ignore[arg-type]


def complex_conjugate(
    x: Union[Number, Sequence[Number]], y: Union[Number, Sequence[Number]]
) -> Tuple[Union[float, list[float]], Union[float, list[float]]]:
    """
    Сопряжение: z̄ = x − i·y.

    Отражение в Явном потоке.

    Args:
        x: Real part.
        y: Imaginary part.

    Returns:
        Tuple (real, imag) for conjugate: (x, -y).
    """
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return x, -y
    return x, [-yi for yi in y]  # type: ignore[return-value]


def complex_multiply(
    x1: Union[Number, Sequence[Number]],
    y1: Union[Number, Sequence[Number]],
    x2: Union[Number, Sequence[Number]],
    y2: Union[Number, Sequence[Number]],
) -> Tuple[Union[float, list[float]], Union[float, list[float]]]:
    """
    Умножение комплексных чисел:

    (x1 + i·y1) ⊗ (x2 + i·y2) = (x1·x2 − y1·y2) + i·(x1·y2 + x2·y1)

    Args:
        x1: Real part of first number.
        y1: Imaginary part of first number.
        x2: Real part of second number.
        y2: Imaginary part of second number.

    Returns:
        Tuple (real, imag) of the product.
    """
    if all(isinstance(v, (int, float)) for v in (x1, y1, x2, y2)):
        real = x1 * x2 - y1 * y2  # type: ignore[operator]
        imag = x1 * y2 + x2 * y1  # type: ignore[operator]
        return real, imag
    real = [xi1 * xi2 - yi1 * yi2 for xi1, yi1, xi2, yi2 in zip(x1, y1, x2, y2)]  # type: ignore[arg-type]
    imag = [xi1 * yi2 + xi2 * yi1 for xi1, yi1, xi2, yi2 in zip(x1, y1, x2, y2)]  # type: ignore[arg-type]
    return real, imag


def complex_branch(
    x: Union[Number, Sequence[Number]], y: Union[Number, Sequence[Number]]
) -> Tuple[Union[float, list[float]], Union[float, list[float]]]:
    """
    Ветвление комплексного числа: z : Ω = D(x) + i·D(y).

    Согласно Essentials [09_Комплексные.md]:
    Акт масштабирует оба потока одновременно.
    Скрытое и Явное растут синхронно.

    Args:
        x: Real part.
        y: Imaginary part.

    Returns:
        Tuple (D(x), D(y)) — both components doubled.
    """
    from .branching import D

    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return D(x), D(y)
    return D(x), D(y)


def complex_compress(
    x: Union[Number, Sequence[Number]], y: Union[Number, Sequence[Number]]
) -> Tuple[Union[float, list[float]], Union[float, list[float]]]:
    """
    Сжатие комплексного числа: z : D(Id) = (x:D(Id)) + i·(y:D(Id)).

    Согласно Essentials [09_Комплексные.md]:
    Возврат по обоим потокам одновременно.

    Args:
        x: Real part.
        y: Imaginary part.

    Returns:
        Tuple (H(x), H(y)) — both components halved.
    """
    from .branching import H

    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return H(x), H(y)
    return H(x), H(y)


def complex_rotate(
    x: Union[Number, Sequence[Number]], y: Union[Number, Sequence[Number]], theta: float
) -> Tuple[Union[float, list[float]], Union[float, list[float]]]:
    """
    Вращение комплексного числа на угол θ.

    z · e^(i·θ) = (x·cos(θ) − y·sin(θ)) + i·(x·sin(θ) + y·cos(θ))

    Согласно Essentials [09_Комплексные.md]:
    Вращение — это обмен энергией между x и y без потери нормы.

    Args:
        x: Real part.
        y: Imaginary part.
        theta: Rotation angle in radians.

    Returns:
        Tuple (real', imag') after rotation.
    """
    c = math.cos(theta)
    s = math.sin(theta)
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        real = x * c - y * s
        imag = x * s + y * c
        return real, imag
    real = [xi * c - yi * s for xi, yi in zip(x, y)]  # type: ignore[arg-type]
    imag = [xi * s + yi * c for xi, yi in zip(x, y)]  # type: ignore[arg-type]
    return real, imag
