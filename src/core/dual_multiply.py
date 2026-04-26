"""Dual multiplication: (x₁+v₁ε) ⊗ (x₂+v₂ε) = (x₁x₂) + (x₁v₂+x₂v₁)ε."""


def dual_multiply(x1, v1, x2, v2):
    return float(x1) * float(x2), float(x1) * float(v2) + float(x2) * float(v1)
