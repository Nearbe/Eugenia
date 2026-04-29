"""Linear equations from Universe/Math/17_Линейные_уравнения.md."""

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

from ..constants.constants import OMEGA
from ..algebra import add, branch, compress, divide, is_omega, multiply


class LinearEquationState(StrEnum):
    """Possible states of a U-linear equation realization."""

    UNIQUE = "unique"
    LIFE_PERSPECTIVE = "life_perspective"
    IMPOSSIBLE_REALIZATION = "impossible_realization"


@dataclass(frozen=True)
class LinearEquationSolution:
    """Result of solving a linear U-equation."""

    state: LinearEquationState
    value: object | None = None


@dataclass(frozen=True)
class LinearEquation:
    """Equation ``(c₀·Id ⊕ c₁·D ⊕ c₂·H)(x) = target``."""

    c_id: object
    c_branch: object
    c_compress: object
    target: object

    def coefficient(self) -> object:
        """Return ``K = c₀ ⊕ D(c₁) ⊕ H(c₂)``."""
        return linear_coefficient(self.c_id, self.c_branch, self.c_compress)

    def evaluate(self, value: object) -> object:
        """Evaluate the linear combination on ``value``."""
        id_part = multiply(self.c_id, value)
        branch_part = multiply(self.c_branch, branch(value))
        compress_part = multiply(self.c_compress, compress(value))
        return add(add(id_part, branch_part), compress_part)

    def solve(self) -> LinearEquationSolution:
        """Solve the equation according to potential/realization alignment."""
        return solve_linear_equation(
            c_id=self.c_id,
            c_branch=self.c_branch,
            c_compress=self.c_compress,
            target=self.target,
        )


def linear_coefficient(c_id: object, c_branch: object, c_compress: object) -> object:
    """Return ``K = c₀ ⊕ D(c₁) ⊕ H(c₂)``."""
    return add(add(c_id, branch(c_branch)), compress(c_compress))


def solve_linear_equation(
    *,
    c_id: object,
    c_branch: object,
    c_compress: object,
    target: object,
) -> LinearEquationSolution:
    """Solve ``K ⊗ x = target`` where ``K`` is the U-linear coefficient."""
    coefficient = linear_coefficient(c_id, c_branch, c_compress)
    if is_omega(coefficient):
        if is_omega(target):
            return LinearEquationSolution(LinearEquationState.LIFE_PERSPECTIVE)
        return LinearEquationSolution(LinearEquationState.IMPOSSIBLE_REALIZATION)
    return LinearEquationSolution(LinearEquationState.UNIQUE, divide(target, coefficient))
