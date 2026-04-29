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
from core.linear.linear_system import (
    LinearSystem,
    LinearSystemState,
    determinant,
    operator_matrix,
)


def test_linear_system_solves_unique_interaction_map():
    system = LinearSystem(matrix=[[2, 0], [0, 4]], target=[4, 8])
    solution = system.solve()

    assert solution.state == LinearSystemState.UNIQUE
    assert solution.determinant == pytest.approx(8.0)
    assert solution.values == pytest.approx([2.0, 2.0])
    assert system.evaluate(solution.values) == pytest.approx([4.0, 8.0])


def test_branching_system_preserves_solution_truth():
    system = LinearSystem(matrix=[[2, 1], [1, 1]], target=[5, 3])
    branched = system.branch()

    assert system.solve().values == pytest.approx([2.0, 1.0])
    assert branched.solve().values == pytest.approx([2.0, 1.0])


def test_potential_determinant_marks_coupled_structure():
    system = LinearSystem(matrix=[[1, 2], [2, 4]], target=[3, 6])
    solution = system.solve()

    assert determinant(system.matrix) == OMEGA
    assert solution.state == LinearSystemState.COUPLED_STRUCTURE
    assert solution.values is None


def test_operator_matrix_combines_explicit_branch_and_base_maps():
    matrix = operator_matrix(
        branch_part=[[1, 0], [0, 2]],
        base_part=[[3, 4], [5, 6]],
    )

    assert matrix == pytest.approx([[5.0, 4.0], [5.0, 10.0]])
