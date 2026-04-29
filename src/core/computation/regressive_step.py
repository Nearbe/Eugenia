from __future__ import annotations

from ..algebra import compress


def regressive_step(state: object) -> object:
    """Mind regression: ``Ψₙ₋₁ = H(Ψₙ)``."""
    return compress(state)
