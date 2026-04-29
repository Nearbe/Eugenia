"""cos — cosine via sin: cos(x) = sin(π/2 - x)."""
from .sin import sin
from .__math_constants import HALF_PI


def cos(x):
    return sin(HALF_PI - x)