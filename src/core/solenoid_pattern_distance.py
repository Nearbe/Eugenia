"""
solenoid_pattern_distance — Расстояние соленоидов.

Per Essentials [23_Соленоид.md, XI. Метрика Близости]:
Two points are close if their binary histories match on many
initial steps. If histories diverge early — points are far,
even if current values are close.
"Происхождение важнее текущего вида."
"""

from .solenoid_encode_pattern import solenoid_encode_pattern
from .sweep import solenoid_distance


def solenoid_pattern_distance(
    values_a: list[float],
    values_b: list[float],
    depth: int = 30,
) -> float:
    """
    Compute solenoid distance between two data patterns.

    Args:
        values_a: First data pattern.
        values_b: Second data pattern.
        depth: Bit depth for encoding.

    Returns:
        Closeness: 2^(-k) where k is the first differing bit.
    """
    traj_a = solenoid_encode_pattern(values_a, depth)
    traj_b = solenoid_encode_pattern(values_b, depth)
    return solenoid_distance(traj_a, traj_b)
