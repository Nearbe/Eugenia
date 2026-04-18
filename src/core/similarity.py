"""
Cosine similarity — на алгебре долей.

Вместо евклидова косинуса (который ломается на нуле),
используем отношение долей от Π:

    Sim(a, b) = (a:Π) ⊗ (b:Π) / (||a:Π|| ⊕ ||b:Π||)

Это работает на всех уровнях Хребта, включая Π и Ω.
"""

from numpy import clip, ndarray, sqrt, sum, where


def similarity(a: ndarray, b: ndarray) -> ndarray:
    """
    Сходство через алгебру долей (процентов).

    Args:
        a: First vector.
        b: Second vector.

    Returns:
        Cosine similarity in [-1, 1] computed in percentage space.
    """
    from .percent import to_percentage

    # Convert to percentages (fractions of Π)
    pa = to_percentage(a)
    pb = to_percentage(b)

    # Norms in percentage space
    norm_a = sqrt(sum(pa**2, axis=-1, keepdims=True))
    norm_b = sqrt(sum(pb**2, axis=-1, keepdims=True))

    # Dot product in percentage space
    dot = sum(pa * pb, axis=-1, keepdims=True)

    # Cosine similarity with branching-aware normalization
    # When norm → 0 (Ω), return 1 (identity: Π:Π = Id)
    denom = norm_a * norm_b
    mask_zero = denom < 1e-10
    result = where(mask_zero, 1.0, dot / denom)

    return clip(result, -1.0, 1.0)
