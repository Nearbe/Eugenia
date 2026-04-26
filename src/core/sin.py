"""sin — sine via Taylor series."""
from .__math_constants import PI, HALF_PI, TWO_PI


def sin(x):
    while x > TWO_PI:
        x -= TWO_PI
    while x < -TWO_PI:
        x += TWO_PI
    if x > PI:
        x = x - TWO_PI
    if x < -PI:
        x = x + TWO_PI
    if x < 0:
        return -sin(-x)
    if x > HALF_PI:
        x = PI - x
    x2 = x * x
    return x - x2*x/6 + x2*x2*x/120