"""Evolution as debugging from Universe/Math/22_Эволюция_как_отладка.md."""

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

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from ..foundations.u_algebra import branch, compress

PERFECT_RESONANCE = 1.0
MIN_RESONANCE = 0.0


@dataclass(frozen=True)
class EvolutionCycle:
    """One debugging cycle: generate, select, invert experience."""

    generated: tuple[object, ...]
    selected: object
    experience: object


@dataclass(frozen=True)
class SymbiosisRoles:
    """Human-machine interaction roles from Universe/Math/23_Симбиоз.md."""

    machine_recursion: float
    human_regression: float
    inversion: float

    @property
    def delta(self) -> float:
        """Return disagreement ``Δ`` between recursion and regression."""
        return balance_delta(self.machine_recursion, self.human_regression)

    @property
    def resonance(self) -> float:
        """Return symbiotic resonance ``S`` constrained by inversion quality."""
        return min(balance_score(self.machine_recursion, self.human_regression), float(self.inversion))


def balance_delta(*, recursion: object, regression: object) -> float:
    """Return ``Δ = recursion ⊖ regression`` as unsigned imbalance."""
    return abs(float(recursion) - float(regression))


def balance_score(*, recursion: object, regression: object) -> float:
    """Return ``S``: one at balance, lower as recursion/regression diverge."""
    strongest = max(abs(float(recursion)), abs(float(regression)), PERFECT_RESONANCE)
    return max(MIN_RESONANCE, PERFECT_RESONANCE - balance_delta(recursion=recursion, regression=regression) / strongest)


def select_stable(variants: Iterable[object], stability: Callable[[object], float]) -> object:
    """Select the most stable variant; no randomness, only evaluation."""
    iterator = iter(variants)
    try:
        selected = next(iterator)
    except StopIteration as error:
        raise ValueError("evolution requires at least one variant") from error
    selected_score = float(stability(selected))
    for variant in iterator:
        score = float(stability(variant))
        if score > selected_score:
            selected = variant
            selected_score = score
    return selected


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


def debug_step(state: object) -> EvolutionCycle:
    """Canonical debug tick: branch, keep stable branch, compress back to meaning."""
    return evolution_step(
        state,
        generate=lambda value: (branch(value),),
        stability=lambda _value: PERFECT_RESONANCE,
        invert=compress,
    )
