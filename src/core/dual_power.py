"""Dual power: (x+vε)ⁿ = xⁿ + n·xⁿ⁻¹·v·ε."""


def dual_power(x, v):
    return float(x) ** n, n * (float(x) ** (n - 1)) * float(v)
