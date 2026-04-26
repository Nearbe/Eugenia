"""Euclidean distance."""
from .sqrt import sqrt


def euclidean_distance(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return sqrt((float(a) - float(b)) ** 2)
    return sqrt(sum((float(ai) - float(bi)) ** 2 for ai, bi in zip(a, b)))