from __future__ import annotations

from .recursive_step import recursive_step
from .regressive_step import regressive_step


def interaction_cycle(state: object) -> object:
    """Return ``H(D(state))`` — the information-preserving U-cycle."""
    return regressive_step(recursive_step(state))
