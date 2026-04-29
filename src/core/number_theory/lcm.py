"""LCM for powers of two: LCM(2^n, 2^m) = 2^max(n,m)."""


def lcm(a: int, b: int) -> int:
    return 2 ** max(a.bit_length() - 1, b.bit_length() - 1) if a > 0 and b > 0 else 1