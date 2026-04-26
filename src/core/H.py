"""Compression: H(a) = a : D(Id) = a/2."""


def H(x: float | int | list) -> float | list:
    if isinstance(x, (int, float)):
        return x / 2
    return [float(v) / 2 for v in x]