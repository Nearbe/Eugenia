"""Dynamic systems from Universe/Math/29_Динамические_системы.md."""

#  Copyright (c) 2026.
#  ╔═══════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═══════════════════════════════════╝
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping

from ..foundations.constants import D_ID
from ..foundations.u_algebra import branch, compress
from ..operators.L import L

DEFAULT_PERIODS = 1
POTENTIAL_PREIMAGE_WEIGHT = 0.0


class DynamicStep(StrEnum):
    """Elementary U-dynamic operators."""

    BRANCH = "D"
    COMPRESS = "H"


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


def apply_step(value: object, step: DynamicStep | str) -> object:
    """Apply one dynamic operator."""
    dynamic_step = DynamicStep(step)
    if dynamic_step == DynamicStep.BRANCH:
        return branch(value)
    return compress(value)


def orbit(seed: object, steps: tuple[DynamicStep | str, ...]) -> Orbit:
    """Return trajectory under a finite word of ``D`` and ``H``."""
    normalized_steps = tuple(DynamicStep(step) for step in steps)
    states: list[object] = [seed]
    current = seed
    for step in normalized_steps:
        current = apply_step(current, step)
        states.append(current)
    return Orbit(seed=seed, steps=normalized_steps, states=tuple(states))


def oscillation(seed: object) -> Orbit:
    """Return elementary cycle ``D → H``."""
    return orbit(seed, (DynamicStep.BRANCH, DynamicStep.COMPRESS))


def period_cycle(seed: object, *, periods: int = DEFAULT_PERIODS) -> Orbit:
    """Return repeated ``D → H`` periods."""
    if periods < 0:
        raise ValueError("periods must be non-negative")
    return orbit(seed, (DynamicStep.BRANCH, DynamicStep.COMPRESS) * periods)


def lyapunov_exponent() -> object:
    """Return ``λ = L(D'(x)) = L(D(Id))``."""
    return L(D_ID)


def invariant_measure_holds(
    measure: Mapping[object, float],
    preimage: Mapping[object, tuple[object, ...]],
    event: object,
) -> bool:
    """Return true when ``μ(D⁻¹(A)) = μ(A)`` for a finite partition.

    ``D`` doubles states, so each point of the inverse image contributes through
    the inverse branch ``H``. The preimage mass is therefore compressed once.
    """
    event_measure = float(measure.get(event, 0.0))
    preimage_mass = sum(float(measure.get(state, 0.0)) for state in preimage.get(event, ()))
    if preimage_mass == POTENTIAL_PREIMAGE_WEIGHT:
        return event_measure == POTENTIAL_PREIMAGE_WEIGHT
    preimage_measure = float(compress(preimage_mass))
    return preimage_measure == event_measure
