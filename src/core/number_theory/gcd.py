"""GCD for powers of two: GCD(2^n, 2^m) = 2^min(n,m)."""


def gcd(a: int, b: int) -> int:
    return 2 ** (min(a.bit_length(), b.bit_length()) - 1) if a > 0 and b > 0 else 1