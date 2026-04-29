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
from core.algebra import branch
from core import (
    branching_function,
    compose,
    logarithmic_function,
    periodic_function,
    power_function,
)


def test_power_function_reacts_to_branching_by_power_of_branch():
    square = power_function(2)

    assert square(3) == pytest.approx(9.0)
    assert square.on_branch(3) == pytest.approx(36.0)
    assert square.on_branch(3) == square(branch(3))


def test_branching_function_turns_act_into_repeated_branching():
    fn = branching_function()

    assert fn(3) == pytest.approx(6.0)
    assert fn.on_branch(3) == pytest.approx(12.0)


def test_logarithmic_function_turns_branching_into_depth_shift():
    fn = logarithmic_function()

    assert fn(8) == pytest.approx(3.0)
    assert fn.on_branch(8) == pytest.approx(4.0)
    assert fn.on_compress(8) == pytest.approx(2.0)


def test_periodic_function_returns_flow_plane_state_and_scales_phase():
    wave = periodic_function(1)

    assert wave(0) == ComplexState(1.0045248555348174, 0.0)
    assert wave.on_branch(1) == wave(branch(1))


def test_function_composition_passes_branching_through_inner_law():
    composed = compose(logarithmic_function(), branching_function())

    assert composed(8) == pytest.approx(4.0)
    assert composed.on_branch(8) == pytest.approx(5.0)
