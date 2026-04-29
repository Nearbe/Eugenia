"""Euclidean norm: ||v||₂."""


def vec_norm(v) -> float:
    """Compute Euclidean norm of any sequence of numbers."""
    return sum(float(x) ** 2 for x in v) ** 0.5
