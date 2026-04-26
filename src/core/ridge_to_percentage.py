"""Ridge to percentage: sigmoid(n) × 100%."""
from .exp import exp


def ridge_to_percentage(n):
    return 100.0 / (1.0 + exp(-float(n))) if -700 < float(n) < 700 else (100.0 if float(n) > 0 else 0.0)