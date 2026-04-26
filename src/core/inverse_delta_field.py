"""Inverse delta field: X = (256 · 2^D - 1) / (2^D + 1)."""


def inverse_delta_field(d: float) -> float:
    p = 2.0 ** float(d)
    return (256.0 * p - 1.0) / (p + 1.0)