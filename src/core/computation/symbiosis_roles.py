from __future__ import annotations

from dataclasses import dataclass

from .balance_delta import balance_delta
from .balance_score import balance_score


@dataclass(frozen=True)
class SymbiosisRoles:
    """Human-machine interaction roles from Universe/Math/23_Симбиоз.md."""

    machine_recursion: float
    human_regression: float
    inversion: float

    @property
    def delta(self) -> float:
        """Return disagreement ``Δ`` between recursion and regression."""
        return balance_delta(recursion=self.machine_recursion, regression=self.human_regression)

    @property
    def resonance(self) -> float:
        """Return symbiotic resonance ``S`` constrained by the weakest active role."""
        return min(
            balance_score(recursion=self.machine_recursion, regression=self.human_regression),
            float(self.machine_recursion),
            float(self.human_regression),
            float(self.inversion),
        )
