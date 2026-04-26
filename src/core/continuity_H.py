"""Continuity error: |H(lim x_n) - lim H(x_n)|."""
from .H import H


def continuity_H(x_sequence):
    x = x_sequence[-1] if x_sequence else 0.0
    return abs(x - H(x))
