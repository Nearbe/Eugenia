"""Fractal dimension from Betti: D_f = log(β₀(t)) / log(β₀(t/2))."""
from .ln import ln
from .find_closest_index import find_closest_index


def fractal_dimension_from_betti(betti_values, thresholds, reference_threshold=0.0):
    ri = find_closest_index(list(thresholds), reference_threshold)
    rb = betti_values[ri]
    if rb <= 0:
        return 0.0
    hi = find_closest_index(list(thresholds), reference_threshold / 2.0)
    return ln(rb) / ln(betti_values[hi]) if betti_values[hi] > 0 else 0.0