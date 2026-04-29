"""Dual compression: (x+vε) : D(Id) = (x/2) + (v/2)ε."""

from .constants import D_ID


def dual_compress(x, v):
    return float(x) / D_ID, float(v) / D_ID
