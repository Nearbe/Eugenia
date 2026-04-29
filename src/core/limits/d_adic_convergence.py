"""D-adic convergence: v₂(a-b)."""
from .v2_adic_valuation import v2_adic_valuation

def d_adic_convergence(a, b):
    return v2_adic_valuation(abs(float(a) - float(b)))
