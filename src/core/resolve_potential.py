"""Resolve potential: Ω → default."""
from .__math_constants import OMEGA

def resolve_potential(x, default: float = 0.0):
    if x is None:
        return default
    if isinstance(x, (int, float)):
        return default if x == OMEGA else float(x)
    for v in x:
        if v != OMEGA:
            return float(v)
    return default
