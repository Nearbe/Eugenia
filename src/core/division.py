"""
Branching-aware division — a : b с учётом ветвления.

Для b = Ω (0): a : Ω = D(a) = a ⊕ a — Ветвление, не ошибка.
Для b = D(Id) (2): a : D(Id) = H(a) = a/2 — Сжатие.
Для b ≠ Ω: стандартное деление a/b.

Это не «защита от деления на ноль». Это **смена масштаба**.
"""

from numpy import abs, any, ndarray, zeros_like

from .branching import D, H
from .constants import D_ID, OMEGA


def safe_divide(a: ndarray, b: ndarray) -> ndarray:
    """
    Деление a : b с учётом ветвления.

    Args:
        a: Numerator.
        b: Denominator.

    Returns:
        Branching-aware division result.
    """
    result = zeros_like(a, dtype=float)

    # Case 1: b = Ω → Ветвление (branching)
    # a : Ω = D(a) = a ⊕ a
    mask_branch = b == OMEGA
    if any(mask_branch):
        result[mask_branch] = D(a[mask_branch])

    # Case 2: b = D(Id) → Сжатие (compression)
    # a : D(Id) = H(a) = a / 2
    mask_compress = (abs(b - D_ID) < 1e-10) & ~mask_branch
    if any(mask_compress):
        result[mask_compress] = H(a[mask_compress])

    # Case 3: Standard division
    # a : b = a / b (b ∉ Ω)
    mask_normal = ~mask_branch & ~mask_compress
    if any(mask_normal):
        result[mask_normal] = a[mask_normal] / b[mask_normal]

    return result


def div_safe(a: ndarray, b: ndarray) -> ndarray:
    """Alias for safe_divide."""
    return safe_divide(a, b)
