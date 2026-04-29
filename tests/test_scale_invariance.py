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

from core.renormalization.scale_invariance import (
    RenormalizationFlow,
    beta_function,
    covariant_power_law,
    inverse_rg_step,
    is_scale_invariant_solution,
    rg_flow,
    rg_step,
)


def test_rg_step_is_division_by_potential_and_inverse_is_compression():
    assert rg_step(3.0) == pytest.approx(6.0)
    assert inverse_rg_step(6.0) == pytest.approx(3.0)


def test_beta_function_is_linear_flow_delta():
    assert beta_function(5.0) == pytest.approx(5.0)


def test_rg_flow_moves_along_branching_depth():
    flow = rg_flow(3.0, steps=3)

    assert flow == RenormalizationFlow(seed=3.0, states=(3.0, 6.0, 12.0, 24.0))
    assert flow.depth == 3


def test_power_law_covariance_keeps_branch_class():
    assert covariant_power_law(3.0, exponent=2.0) == pytest.approx(18.0)


def test_linear_solution_is_invariant_under_common_rg_step():
    assert is_scale_invariant_solution(matrix=((2.0, 0.0), (0.0, 4.0)), target=(6.0, 8.0))
