"""v₂(x) = max n such that 2^n divides x."""


def v2_adic_valuation(val: float | int) -> float:
    if val == 0.0:
        return float("-inf")
    v = abs(float(val))
    n = 0
    while v > 1e-15 and v % 2.0 == 0:
        v /= 2.0
        n += 1
    return float(n)