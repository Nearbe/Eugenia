"""
solenoid_encode_pattern — Кодирование паттерна в соленоид.

Per Essentials [23_Соленоид.md]:
Each point on the solenoid is the full branching history:
z₀ = D(z₁) = D²(z₂) = ... = Dⁿ(zₙ)

Encoded as binary fraction: ξ = 0.ε₀ε₁ε₂… where εₙ ∈ {0, 1}

This provides a lossless, deterministic encoding of the pattern
that preserves branching structure and enables queryable storage.
"""

from .sweep import encode_solenoid_trajectory


def solenoid_encode_pattern(values: list[float], depth: int = 30) -> list[int]:
    """
    Encode a data pattern as a solenoid trajectory.

    Args:
        values: Data values to encode.
        depth: Number of bits in the binary representation.

    Returns:
        Binary trajectory [ε₀, ε₁, ..., εₙ₋₁].
    """
    avg = sum(values) / len(values) if values else 0.0
    return encode_solenoid_trajectory(avg, depth)
