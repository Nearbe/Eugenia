from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionCycle:
    """One debugging cycle: generate, select, invert experience."""

    generated: tuple[object, ...]
    selected: object
    experience: object
