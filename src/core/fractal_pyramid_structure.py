"""
fractal_pyramid_structure — Структура фрактальной пирамиды.

Per Essentials: the pyramid has Ω (0) at the center of each level,
with branching (right: 1, 2, 3, ...) and compression (left: 3, 2, 1)
forming a bridge through potential.
"""

from .pyramid import fractal_pyramid_level, fractal_bridge_analysis


def fractal_pyramid_structure(max_level: int = 10) -> list[dict]:
    """
    Generate fractal pyramid structure as analysis-ready dicts.

    Args:
        max_level: Maximum pyramid level.

    Returns:
        List of dicts with level, left, center, right, and analysis.
    """
    pyramid = []
    for level in range(1, max_level + 1):
        left, center, right = fractal_pyramid_level(level)
        bridge = fractal_bridge_analysis(level)
        pyramid.append(
            {
                "level": level,
                "left": left,
                "center": center,
                "right": right,
                "bridge_analysis": bridge,
            }
        )
    return pyramid
