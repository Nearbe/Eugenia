from __future__ import annotations

from ..algebra import branch


def recursive_step(state: object) -> object:
    """Universe recursion: ``Ψₙ₊₁ = D(Ψₙ)``."""
    return branch(state)
