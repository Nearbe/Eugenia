"""
pattern_similarity_from_delta — Косинусное сходство на delta-field.

Pipeline:
    1. Transform raw values through delta_field: X → log2(X+1) - log2(256-X)
    2. Compute cosine similarity in delta-space (RealMath-aware)

This is more robust than raw cosine similarity because the delta field
maps pixel intensities to a logarithmic spine scale where branching
structure is preserved (Essentials [08_Логарифм.md], [22_Геометрия.md]).
"""

from .delta import delta_field


def pattern_similarity_from_delta(
    values_a: list[float],
    values_b: list[float],
) -> float:
    """
    Compute similarity between two data series using delta field transformation.

    Args:
        values_a: First data series (pixel values 0-255 or normalized).
        values_b: Second data series (pixel values 0-255 or normalized).

    Returns:
        Cosine similarity in delta-space ∈ [-1, 1].
    """
    if not values_a or not values_b:
        return 0.0

    delta_a = delta_field(values_a)
    delta_b = delta_field(values_b)

    if isinstance(delta_a, float):
        delta_a = [delta_a]
    if isinstance(delta_b, float):
        delta_b = [delta_b]

    norm_a = sum(x**2 for x in delta_a) ** 0.5
    norm_b = sum(x**2 for x in delta_b) ** 0.5

    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0

    dot = sum(x * y for x, y in zip(delta_a, delta_b))
    return dot / (norm_a * norm_b)
