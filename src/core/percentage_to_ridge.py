"""Percentage to ridge: log2(p / (100 - p))."""
from .ln import ln


def percentage_to_ridge(p):
    return ln(float(p) / (100.0 - float(p))) / 0.6931471805599453