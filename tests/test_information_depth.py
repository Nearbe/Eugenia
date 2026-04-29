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

from core.combinatorics.branching import BranchingLevel
from core.foundations.constants import OMEGA
from core.foundations.infinity import PI
from core.foundations.logarithmic_axis import LOG_POSITIVE_INFINITY
from core.foundations.spine import spine_level
from core.information.information_depth import (
    address_cost,
    address_state,
    branch_information,
    branching_level_information,
    choice_capacity,
    compress_information,
    information,
    mass_from_information,
)


def test_information_is_log_depth_of_mass():
    assert information(spine_level(0)) == OMEGA
    assert information(spine_level(1)) == 1.0
    assert information(spine_level(5)) == 5.0
    assert information(PI) == LOG_POSITIVE_INFINITY


def test_mass_from_information_returns_spine_depth_or_fullness():
    assert mass_from_information(OMEGA) == spine_level(0)
    assert mass_from_information(4) == spine_level(4)
    assert mass_from_information(LOG_POSITIVE_INFINITY) == PI


def test_branching_and_compression_change_information_by_one_choice():
    mass = spine_level(4)

    assert branch_information(mass) == 5.0
    assert compress_information(mass) == 3.0


def test_addressed_state_cost_matches_information_depth():
    state = address_state(5, depth=3)

    assert state.address == (1, 0, 1)
    assert address_cost(state.address) == 3
    assert state.information == 3.0


def test_branching_level_information_and_capacity_match():
    level = BranchingLevel(6)

    assert branching_level_information(level) == 6.0
    assert choice_capacity(6) == 64
