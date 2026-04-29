from __future__ import annotations

from dataclasses import dataclass

from .dynamic_step import DynamicStep


@dataclass(frozen=True)
class Orbit:
    """Trajectory of a seed under a finite D/H word."""

    seed: object
    steps: tuple[DynamicStep, ...]
    states: tuple[object, ...]

    @property
    def final(self) -> object:
        """Return the final state of the orbit."""
        return self.states[-1]
