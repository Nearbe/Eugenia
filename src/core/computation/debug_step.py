from __future__ import annotations

from .evolution_cycle import EvolutionCycle
from .evolution_step import evolution_step
from .balance_score import PERFECT_RESONANCE
from ..algebra import branch, compress


def debug_step(state: object) -> EvolutionCycle:
    """Canonical debug tick: branch, keep stable branch, compress back to meaning."""
    return evolution_step(
        state,
        generate=lambda value: (branch(value),),
        stability=lambda _value: PERFECT_RESONANCE,
        invert=compress,
    )
