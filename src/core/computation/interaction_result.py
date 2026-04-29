from __future__ import annotations

from dataclasses import dataclass

from .computability_state import ComputabilityState


@dataclass(frozen=True)
class InteractionResult:
    """Result of reverse connectivity analysis from STOP to START."""

    state: ComputabilityState
    regression_frontier: tuple[object, ...]
    path: tuple[object, ...]

    @property
    def halts(self) -> bool:
        """Return true when START is connected to STOP."""
        return self.state == ComputabilityState.HALTS
