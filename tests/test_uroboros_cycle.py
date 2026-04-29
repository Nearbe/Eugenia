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

from core.constants.constants import OMEGA
from core.infinity.infinity import PI
from core.infinity.uroboros import (
    CENTER_DIGIT,
    CYCLE_LENGTH,
    UroborosState,
    cycle_distance,
    cycle_step,
    state_at,
    state_range_value,
)


def test_uroboros_cycle_is_closed_from_nine_to_zero():
    assert cycle_step(9) == 0
    assert cycle_step(0) == 1
    assert CYCLE_LENGTH == 10


def test_center_digit_is_identity_balance():
    state = state_at(CENTER_DIGIT)

    assert state.digit == 5
    assert state.kind == "Id"
    assert state.value == pytest.approx(0.0)


def test_boundaries_are_omega_and_fullness():
    omega_state = state_at(0)
    fullness_state = state_at(9)

    assert omega_state.kind == "Ω"
    assert omega_state.symbol == OMEGA
    assert fullness_state.kind == "Π"
    assert fullness_state.symbol == PI


def test_state_range_maps_cycle_to_closed_interval():
    assert state_range_value(0) == pytest.approx(-1.0)
    assert state_range_value(5) == pytest.approx(0.0)
    assert state_range_value(9) == pytest.approx(1.0)


def test_cycle_distance_uses_shortest_closed_path():
    assert cycle_distance(9, 0) == 1
    assert cycle_distance(0, 9) == 1
    assert cycle_distance(2, 7) == 5


def test_uroboros_state_can_advance_through_cycle():
    assert UroborosState(9).step() == UroborosState(0)
