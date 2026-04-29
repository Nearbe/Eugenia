from __future__ import annotations


def balance_delta(*, recursion: object, regression: object) -> float:
    """Return ``Δ = recursion ⊖ regression`` as unsigned imbalance."""
    return abs(float(recursion) - float(regression))
