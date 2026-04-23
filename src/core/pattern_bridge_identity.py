"""
pattern_bridge_identity — Идентичность моста через Ω.

For a value v at pyramid level n:
    - left: reverse sequence (n-1, n-2, ..., 1) → compression H
    - right: forward sequence (1, 2, ..., n-1) → branching D
    - center: 0 = Ω (bridge, not barrier)

Identity: left:Ω:right = Id (through potential, not division)
"""

from .pyramid import fractal_bridge_analysis
from .pattern_pyramid_depth import pattern_pyramid_depth


def pattern_bridge_identity(value: float) -> dict:
    """
    Check the bridge identity for a value through Ω.

    Args:
        value: A numeric value to analyze.

    Returns:
        Bridge analysis dict with identity check results.
    """
    depth = pattern_pyramid_depth(value)
    return fractal_bridge_analysis(max(depth, 1))
