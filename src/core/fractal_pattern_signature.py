"""
fractal_pattern_signature — Топологический fingerprint паттерна.

Combines:
    1. Binary sweep profile (n_thresholds thresholds)
    2. Jump events (topological changes)
    3. Fractal dimension (Betti scaling)
    4. Spine levels (ridge mapping)
"""

from .fractal_dimension import fractal_dimension_from_betti
from .spine import ridge_level, ridge_to_percentage
from .delta import delta_field


def fractal_pattern_signature(
    values: list[float],
    n_thresholds: int = 64,
) -> dict:
    """
    Compute a fractal pattern signature for a data series.

    Args:
        values: Data values (pixel intensities, normalized data, etc.).
        n_thresholds: Number of sweep thresholds.

    Returns:
        Dictionary with fractal signature components.
    """
    thresholds = [i / n_thresholds for i in range(n_thresholds + 1)]
    binary_profile = [float(v > t) for v in values for t in thresholds]

    profile = []
    bin_size = len(values)
    for i in range(n_thresholds + 1):
        start = i * bin_size
        end = start + bin_size
        profile.append(sum(binary_profile[start:end]) / bin_size)

    jumps = [abs(profile[i + 1] - profile[i]) for i in range(len(profile) - 1)]
    top_jumps = sorted(jumps, reverse=True)[:5]

    betti_values = [max(1, int(p * len(values))) for p in profile]
    try:
        fd = fractal_dimension_from_betti(betti_values, thresholds, reference_threshold=0.5)
    except (ValueError, ZeroDivisionError):
        fd = 0.0

    avg_val = sum(values) / len(values) if values else 0.0
    spine_lvl = ridge_level(avg_val)

    return {
        "profile": profile,
        "top_jumps": top_jumps,
        "fractal_dimension": fd,
        "spine_level": spine_lvl,
        "percentage": ridge_to_percentage(spine_lvl),
        "avg_value": avg_val,
        "delta_value": delta_field(avg_val) if values else 0.0,
    }
