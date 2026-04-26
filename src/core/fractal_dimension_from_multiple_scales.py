"""Fractal dimension at multiple scales."""
from .ln import ln


def fractal_dimension_from_multiple_scales(betti_values, thresholds, n_scales: int = 5):
    return [(s, ln(betti_values[min(len(betti_values)-1, s-1)]) / ln(s)) for s in range(1, n_scales + 1) if betti_values[min(s-1, len(betti_values)-1)] > 0]