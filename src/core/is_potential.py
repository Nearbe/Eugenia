"""Is potential: x == Ω."""
from .constants import OMEGA

def is_potential(x):
    return x == OMEGA if isinstance(x, (int, float)) else all(v == OMEGA for v in x)
