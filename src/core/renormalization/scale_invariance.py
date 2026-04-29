"""Scale invariance from Universe/Math/28_Масштабная_инвариантность.md."""

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

from ..foundations.u_algebra import branch, compress, power
from ..linear.linear_system import LinearSystemState, solve_linear_system

MIN_STEPS = 0


@dataclass(frozen=True)
class RenormalizationFlow:
    """Discrete RG trajectory ``gₙ₊₁ = D(gₙ)``."""

    seed: object
    states: tuple[object, ...]

    @property
    def depth(self) -> int:
        """Return number of RG steps in the trajectory."""
        return max(MIN_STEPS, len(self.states) - 1)


def rg_step(value: object) -> object:
    """Return ``R_D(x)=x:Ω=D(x)``."""
    return branch(value)


def inverse_rg_step(value: object) -> object:
    """Return ``R_D⁻¹(x)=x:D(Id)=H(x)``."""
    return compress(value)


def beta_function(coupling: object) -> object:
    """Return ``β(g)=D(g)⊖g``."""
    return float(rg_step(coupling)) - float(coupling)


def rg_flow(seed: object, *, steps: int) -> RenormalizationFlow:
    """Return finite RG flow ``g₀,g₁,...,gₙ``."""
    if steps < MIN_STEPS:
        raise ValueError("RG steps must be non-negative")
    states: list[object] = [seed]
    current = seed
    for _ in range(steps):
        current = rg_step(current)
        states.append(current)
    return RenormalizationFlow(seed=seed, states=tuple(states))


def covariant_power_law(value: object, *, exponent: object) -> object:
    """Return ``f(x:Ω)`` for ``f(x)=x^b`` under one RG step.

    In U this equals the branched power class, written as ``D(x^b)`` in the
    specification.
    """
    return branch(power(value, exponent))


def branched_matrix(matrix: object) -> tuple[tuple[object, ...], ...]:
    """Return ``D(M)`` component-wise."""
    return tuple(tuple(branch(component) for component in row) for row in matrix)  # type: ignore[union-attr]


def branched_vector(vector: object) -> tuple[object, ...]:
    """Return ``D(b)`` component-wise."""
    return tuple(branch(component) for component in vector)  # type: ignore[union-attr]


def is_scale_invariant_solution(matrix: object, target: object) -> bool:
    """Return true when ``M⁻¹b`` equals ``D(M)⁻¹D(b)``."""
    solution = solve_linear_system(matrix, target)
    branched_solution = solve_linear_system(branched_matrix(matrix), branched_vector(target))
    if solution.state != LinearSystemState.UNIQUE or branched_solution.state != LinearSystemState.UNIQUE:
        return False
    return tuple(solution.values or ()) == tuple(branched_solution.values or ())
