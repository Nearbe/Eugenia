"""Has potential: x ≠ Ω."""
from .__math_constants import OMEGA

def has_potential(x):
    return x != OMEGA if isinstance(x, (int, float)) else any(v != OMEGA for v in x)
