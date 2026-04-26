"""Delta distance on spine scale: |L(a) - L(b)|."""
from .L import L


def delta_distance(a, b):
    la, lb = L(a), L(b)
    if isinstance(la, (int, float)) and isinstance(lb, (int, float)):
        return abs(la - lb)
    return [abs(x - y) for x, y in zip(la, lb)]
