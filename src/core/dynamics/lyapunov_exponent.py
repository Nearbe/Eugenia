from __future__ import annotations

from ..constants.constants import D_ID
from ..operators.L import L


def lyapunov_exponent() -> object:
    """Return ``λ = L(D'(x)) = L(D(Id))``."""
    return L(D_ID)
