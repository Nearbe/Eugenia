"""Dual branching: (x+vε) : Ω = (2x) + (2v)ε."""

from .constants import D_ID


def dual_branch(x, v):
    return float(x) * D_ID, float(v) * D_ID
