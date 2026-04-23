"""
pattern_distance_from_delta — Расстояние на delta-field.

Uses delta_distance on the spine levels of the delta field values,
which respects the branching structure of the data.
"""

from .delta import delta_field
from .distance import delta_distance


def pattern_distance_from_delta(
    values_a: list[float],
    values_b: list[float],
) -> float:
    """
    Compute delta-aware distance between two data series.

    Args:
        values_a: First data series.
        values_b: Second data series.

    Returns:
        Distance on the logarithmic spine scale.
    """
    if not values_a or not values_b:
        return float("inf")

    delta_a = delta_field(values_a)
    delta_b = delta_field(values_b)
    dist = delta_distance(delta_a, delta_b)

    if isinstance(dist, list):
        return sum(dist) / len(dist) if dist else 0.0
    return dist
