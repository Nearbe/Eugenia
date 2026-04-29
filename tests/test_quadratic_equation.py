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
import pytest

from core.states.complex_plane import ComplexState
from core.constants.constants import OMEGA
from core.nonlinear.quadratic_equation import (
    QuadraticRootState,
    discriminant,
    solve_quadratic_equation,
)


def test_discriminant_uses_u_formula_b_square_minus_four_ac():
    assert discriminant(a=1, b=-3, c=2) == pytest.approx(1.0)


def test_quadratic_equation_returns_two_real_roots_when_discriminant_active():
    solution = solve_quadratic_equation(a=1, b=-3, c=2)

    assert solution.state == QuadraticRootState.TWO_REAL_ROOTS
    assert solution.discriminant == pytest.approx(1.0)
    assert solution.roots == pytest.approx([2.0, 1.0])


def test_quadratic_equation_returns_touch_root_at_potential_discriminant():
    solution = solve_quadratic_equation(a=1, b=-2, c=1)

    assert solution.state == QuadraticRootState.TOUCH_ROOT
    assert solution.discriminant == OMEGA
    assert solution.roots == pytest.approx([1.0])


def test_quadratic_equation_enters_hidden_rotation_for_negative_discriminant():
    solution = solve_quadratic_equation(a=1, b=0, c=1)

    assert solution.state == QuadraticRootState.HIDDEN_ROTATION_ROOTS
    assert isinstance(solution.roots[0], ComplexState)
    assert solution.roots[0].real == pytest.approx(0.0)
    assert solution.roots[0].imaginary == pytest.approx(1.0)
    assert solution.roots[1].imaginary == pytest.approx(-1.0)


def test_branching_unknown_quadratically_amplifies_leading_coefficient():
    solution = solve_quadratic_equation(a=1, b=0, c=-4, branched_unknown=True)

    assert solution.effective_a == pytest.approx(4.0)
    assert solution.roots == pytest.approx([1.0, -1.0])
