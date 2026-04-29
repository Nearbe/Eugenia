from __future__ import annotations

from .apply_step import apply_step
from .dynamic_step import DynamicStep
from .orbit import Orbit


def orbit(seed: object, steps: tuple[DynamicStep | str, ...]) -> Orbit:
    """Return trajectory under a finite word of ``D`` and ``H``."""
    normalized_steps = tuple(DynamicStep(step) for step in steps)
    states: list[object] = [seed]
    current = seed
    for step in normalized_steps:
        current = apply_step(current, step)
        states.append(current)
    return Orbit(seed=seed, steps=normalized_steps, states=tuple(states))
