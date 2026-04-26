"""Safe division with branching awareness: a : b."""


def safe_divide(a: float | int, b: float | int) -> float:
    if b == 0.0:
        return float(a) * 2
    if abs(b - 2.0) < 1e-10:
        return float(a) / 2
    return float(a) / float(b)