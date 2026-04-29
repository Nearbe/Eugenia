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

from core.states.fullness_share import FullnessShare
from core.probability.binomial_probability import binomial_probability as legacy_binomial_probability
from core.probability.branch_probability import (
    branch_probability,
    binomial_probability,
    conditional_probability,
    total_probability,
    universe_probability,
)


def test_branch_probability_is_share_of_matching_branches():
    probability = branch_probability(3, 8)

    assert probability.value == pytest.approx(0.375)
    assert probability.to_fullness_share() == FullnessShare(0.375)


def test_binomial_probability_is_combinatoric_branch_share():
    probability = binomial_probability(successes=2, acts=4)

    assert probability.matching_branches == 6
    assert probability.total_branches == 16
    assert probability.value == pytest.approx(0.375)
    assert legacy_binomial_probability(2, 4) == pytest.approx(0.375)


def test_conditional_probability_restricts_to_known_subtree():
    intersection = branch_probability(2, 8)
    condition = branch_probability(4, 8)

    assert conditional_probability(intersection, condition) == pytest.approx(0.5)


def test_total_probability_over_common_depth_sums_to_identity():
    parts = tuple(branch_probability(count, 16) for count in (1, 4, 6, 4, 1))

    assert total_probability(parts) == pytest.approx(1.0)


def test_universe_probability_is_identity_certainty():
    assert universe_probability() == pytest.approx(1.0)
