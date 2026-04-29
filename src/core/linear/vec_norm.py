"""Euclidean norm: ||v||₂."""


def vec_norm(v: list[float]) -> float:
    return sum(x ** 2 for x in v) ** 0.5