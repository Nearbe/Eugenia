"""Fractal similarity: 0.7 * Jaccard + 0.3 * (1 - betti_diff)."""
from .count_components import count_components
from .union_sets import union_sets
from .intersection_sets import intersection_sets

def fractal_similarity_score(mask_a, mask_b):
    fa, fb = {v for row in mask_a for v in row if v > 0}, {v for row in mask_b for v in row if v > 0}
    u, i = union_sets(list(fa), list(fb)), intersection_sets(list(fa), list(fb))
    j = i / u if u > 0 else 0.0
    ba, bb = count_components(mask_a), count_components(mask_b)
    return 0.7 * j + 0.3 * (1.0 - abs(ba - bb) / max(ba, bb, 1))
