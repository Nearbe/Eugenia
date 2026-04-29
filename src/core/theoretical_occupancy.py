"""Theoretical occupancy: P(δ > t) ≈ sum of binomial probabilities."""
from math import comb


def theoretical_occupancy(n_pixels: int, threshold_fraction: float) -> float:
    k = int(threshold_fraction * n_pixels)
    total = 0.0
    for i in range(k, n_pixels + 1):
        total += comb(n_pixels, i) / (2 ** n_pixels)
    return total