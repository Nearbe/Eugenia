"""Dual addition: (x₁+v₁ε) ⊕ (x₂+v₂ε) = (x₁+x₂) + (v₁+v₂)ε."""


def dual_add(x1, v1, x2, v2):
    return float(x1) + float(x2), float(v1) + float(v2)
