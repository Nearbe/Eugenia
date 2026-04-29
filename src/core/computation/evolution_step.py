from __future__ import annotations

from collections.abc import Callable, Iterable

from .evolution_cycle import EvolutionCycle
from .select_stable import select_stable


def evolution_step(
    seed: object,
    generate: Callable[[object], Iterable[object]],
    stability: Callable[[object], float],
    invert: Callable[[object], object],
) -> EvolutionCycle:
    """Run ``D`` generation, ``H`` selection and inversion of experience."""
    generated = tuple(generate(seed))
    selected = select_stable(generated, stability)
    experience = invert(selected)
    return EvolutionCycle(generated, selected, experience)
