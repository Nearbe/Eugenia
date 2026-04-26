"""Cosine similarity between vectors."""
from .vec_norm import vec_norm


def similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = vec_norm(a)
    norm_b = vec_norm(b)
    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0
    return dot / (norm_a * norm_b)