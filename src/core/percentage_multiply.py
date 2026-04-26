"""Percentage multiplication: (a) ⊗ (b)."""
from .ridge_level import ridge_level

def percentage_multiply(a, b):
    return 2.0 ** ((ridge_level(a) + ridge_level(b)) / 2.0)
