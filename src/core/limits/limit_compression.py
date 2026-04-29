"""Limit of compression: H^n(a) = a / 2^n → Ω."""


def limit_compression(a: float, n: int) -> float:
    return 0.0 if n >= 1000 else a / (2.0 ** n)