"""
pattern_similarity_from_complex — Косинусное сходство на complex delta-field.

Pipeline:
    1. Transform through complex_delta_field: X → complex(x, 1-x)
    2. Compute norm-based similarity in complex space

This captures both magnitude AND phase information of the data,
providing richer pattern comparison than real-valued delta_field alone.
"""

from .complex_delta import complex_delta_field


def pattern_similarity_from_complex(
    values_a: list[float],
    values_b: list[float],
) -> float:
    """
    Compute similarity between two data series using complex delta field.

    Args:
        values_a: First data series.
        values_b: Second data series.

    Returns:
        Cosine similarity in complex delta-space ∈ [-1, 1].
    """
    if not values_a or not values_b:
        return 0.0

    complex_a = complex_delta_field(values_a)
    complex_b = complex_delta_field(values_b)

    if isinstance(complex_a, complex):
        complex_a = [complex_a]
    if isinstance(complex_b, complex):
        complex_b = [complex_b]

    real_a = [c.real for c in complex_a]
    imag_a = [c.imag for c in complex_a]
    real_b = [c.real for c in complex_b]
    imag_b = [c.imag for c in complex_b]

    norm_a = (sum(r**2 + i**2 for r, i in zip(real_a, imag_a))) ** 0.5
    norm_b = (sum(r**2 + i**2 for r, i in zip(real_b, imag_b))) ** 0.5

    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0

    dot = sum(r1 * r2 + i1 * i2 for r1, i1, r2, i2 in zip(real_a, imag_a, real_b, imag_b))
    return dot / (norm_a * norm_b)
