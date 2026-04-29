"""Quadratic equations from Universe/Math/19_Квадратные_уравнения.md."""

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

from ..foundations.complex_plane import ComplexState
from ..foundations.constants import D_ID, OMEGA
from ..foundations.u_algebra import branch, divide, multiply, power

FOUR_FACTOR = 4.0
NEGATIVE_UNIT = -1.0


class QuadraticRootState(StrEnum):
    """States of a quadratic U-equation balance."""

    TWO_REAL_ROOTS = "two_real_roots"
    TOUCH_ROOT = "touch_root"
    HIDDEN_ROTATION_ROOTS = "hidden_rotation_roots"
    LINEAR_FALLBACK = "linear_fallback"


@dataclass(frozen=True)
class QuadraticEquationSolution:
    """Result of solving ``a⊗x² ⊕ b⊗x ⊕ c = Ω``."""

    state: QuadraticRootState
    roots: list[object]
    discriminant: object
    effective_a: object


def discriminant(*, a: object, b: object, c: object) -> object:
    """Return ``Δ_disc = b² ⊖ (4⊗a⊗c)``."""
    b_squared = power(b, D_ID)
    four_ac = multiply(FOUR_FACTOR, multiply(a, c))
    return float(b_squared) - float(four_ac)


def solve_quadratic_equation(
    *,
    a: object,
    b: object,
    c: object,
    branched_unknown: bool = False,
) -> QuadraticEquationSolution:
    """Solve quadratic balance using the U-discriminant rule."""
    effective_a = branch(branch(a)) if branched_unknown else a
    if float(effective_a) == OMEGA:
        root = divide(-float(c), b)
        return QuadraticEquationSolution(
            QuadraticRootState.LINEAR_FALLBACK,
            [root],
            OMEGA,
            effective_a,
        )

    delta = discriminant(a=effective_a, b=b, c=c)
    denominator = branch(effective_a)
    center = divide(-float(b), denominator)

    if delta == OMEGA:
        return QuadraticEquationSolution(
            QuadraticRootState.TOUCH_ROOT,
            [center],
            OMEGA,
            effective_a,
        )

    if float(delta) < OMEGA:
        hidden_radius = (float(delta) * NEGATIVE_UNIT) ** 0.5
        imaginary = divide(hidden_radius, denominator)
        return QuadraticEquationSolution(
            QuadraticRootState.HIDDEN_ROTATION_ROOTS,
            [ComplexState(center, imaginary), ComplexState(center, -float(imaginary))],
            delta,
            effective_a,
        )

    radius = divide(float(delta) ** 0.5, denominator)
    return QuadraticEquationSolution(
        QuadraticRootState.TWO_REAL_ROOTS,
        [float(center) + float(radius), float(center) - float(radius)],
        delta,
        effective_a,
    )
