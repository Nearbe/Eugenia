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

from core.constants.constants import D_ID, OMEGA
from core.states.dual_number import DualNumber, EPSILON_SQUARED, dual_number, natural_velocity
from core.algebra import add, branch, compress, divide, multiply, power


def test_dual_epsilon_square_is_potential():
    assert EPSILON_SQUARED == OMEGA
    assert multiply(dual_number(0, 1), dual_number(0, 1)) == DualNumber(0.0, 0.0)


def test_dual_addition_and_multiplication_follow_first_order_rule():
    left = dual_number(2, 3)
    right = dual_number(5, 7)

    assert add(left, right) == DualNumber(7.0, 10.0)
    assert multiply(left, right) == DualNumber(10.0, 29.0)


def test_dual_branching_and_compression_scale_form_and_velocity():
    state = dual_number(3, 4)

    assert branch(state) == DualNumber(6.0, 8.0)
    assert divide(state, OMEGA) == DualNumber(6.0, 8.0)
    assert compress(state) == DualNumber(1.5, 2.0)
    assert divide(state, D_ID) == DualNumber(1.5, 2.0)


def test_dual_power_and_function_application_encode_derivative():
    state = dual_number(3, 4)

    assert power(state, 3) == DualNumber(27.0, 108.0)
    assert state.apply(lambda x: x * x, lambda x: 2 * x) == DualNumber(9.0, 24.0)


def test_natural_velocity_for_d_growth_matches_form():
    assert natural_velocity(9) == pytest.approx(9.0)
