"""Spine value: D^n(Id) = 2^n."""
from core.foundations.logarithmic_axis import LogInfinity


def spine_value(n):
    if isinstance(n, LogInfinity):
        return float("inf")
    return 2.0 ** float(n) if float(n) < 700 else float("inf")