"""Spine value: D^n(Id) = 2^n."""


def spine_value(n):
    return 2.0 ** float(n) if float(n) < 700 else float("inf")