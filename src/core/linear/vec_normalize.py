"""Normalize vector to unit length."""


def vec_normalize(v: list[float]) -> list[float]:
    n = sum(x ** 2 for x in v) ** 0.5
    return [x / n for x in v] if n > 1e-10 else [0.0] * len(v)