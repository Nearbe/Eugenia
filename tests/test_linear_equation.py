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

from core.foundations.constants import OMEGA
from core.linear.linear_equation import (
    LinearEquation,
    LinearEquationState,
    linear_coefficient,
    solve_linear_equation,
)


def test_linear_coefficient_combines_id_branch_and_compress_parts():
    assert linear_coefficient(c_id=1, c_branch=3, c_compress=8) == pytest.approx(11.0)


def test_solve_linear_equation_uses_u_division_by_coefficient():
    equation = LinearEquation(c_id=1, c_branch=3, c_compress=8, target=22)
    solution = equation.solve()

    assert solution.state == LinearEquationState.UNIQUE
    assert solution.value == pytest.approx(2.0)
    assert equation.evaluate(solution.value) == pytest.approx(22.0)


def test_potential_coefficient_and_potential_target_is_life_perspective():
    solution = solve_linear_equation(c_id=0, c_branch=0, c_compress=0, target=OMEGA)

    assert solution.state == LinearEquationState.LIFE_PERSPECTIVE
    assert solution.value is None


def test_potential_coefficient_and_fixed_target_is_impossible_realization():
    solution = solve_linear_equation(c_id=0, c_branch=0, c_compress=0, target=5)

    assert solution.state == LinearEquationState.IMPOSSIBLE_REALIZATION
    assert solution.value is None
