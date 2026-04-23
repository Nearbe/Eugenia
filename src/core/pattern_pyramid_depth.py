"""
pattern_pyramid_depth — Глубина пирамиды для значения.

Maps a value to its spine level (ridge_level), which corresponds
to the pyramid level at which this value first appears.

Per Essentials: ridge_level(x) = log2(|x|) = branching depth.
"""

from .spine import ridge_level


def pattern_pyramid_depth(value: float) -> int:
    """
    Compute the fractal pyramid depth for a given value.

    Args:
        value: A numeric value.

    Returns:
        Pyramid level (spine level) for the value.
    """
    lvl = ridge_level(value)
    if isinstance(lvl, list):
        lvl = lvl[0] if lvl else 0
    return int(lvl)
