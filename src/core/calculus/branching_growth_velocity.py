from __future__ import annotations

from ..constants.constants import D_ID
from ..algebra import multiply
from ..operators.L import L


def branching_growth_velocity(value: object) -> object:
    """Return ``dx/dt = L(D(Id))·x`` for ``x(t)=Dᵗ(Id)``."""
    return multiply(L(D_ID), value)
