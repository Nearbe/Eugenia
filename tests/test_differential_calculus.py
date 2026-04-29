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

from core.calculus import (
    branched_derivative,
    branching_growth_velocity,
    chain_derivative,
    compressed_derivative,
    derivative,
    differential_state,
    power_derivative,
    second_derivative,
)
from core.states.dual_number import DualNumber
from core.algebra import branch, compress, power


def square(value: object) -> object:
    return power(value, 2)


def square_derivative(value: object) -> object:
    return power_derivative(2, value)


def test_derivative_is_extracted_from_dual_hidden_component():
    state = differential_state(square, square_derivative, 3, velocity=4)

    assert state == DualNumber(9.0, 24.0)
    assert derivative(square, square_derivative, 3) == pytest.approx(6.0)


def test_branching_derivative_scales_by_branch_class():
    assert branched_derivative(square_derivative, 3) == pytest.approx(24.0)
    assert branched_derivative(square_derivative, 3) == pytest.approx(
        2.0 * square_derivative(branch(3))
    )


def test_compressed_derivative_scales_by_inverse_branch_class():
    assert compressed_derivative(square_derivative, 8) == pytest.approx(4.0)
    assert compressed_derivative(square_derivative, 8) == pytest.approx(
        square_derivative(compress(8)) / 2.0
    )


def test_chain_rule_multiplies_outer_and_inner_speeds():
    cube_via_chain = chain_derivative(
        outer_derivative=square_derivative,
        inner_fn=lambda value: power(value, 3),
        inner_derivative=lambda value: power_derivative(3, value),
        point=2,
    )

    assert cube_via_chain == pytest.approx(192.0)


def test_branching_growth_velocity_is_proportional_to_state():
    assert branching_growth_velocity(11) == pytest.approx(11.0)


def test_second_derivative_extracts_acceleration():
    assert second_derivative(square_derivative, lambda _value: 2.0, 5) == pytest.approx(2.0)
