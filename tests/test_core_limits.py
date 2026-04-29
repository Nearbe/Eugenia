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
from core.states.dual_number import EPSILON_SQUARED
from core.infinity.infinity import PI
from core.limits.continuity_D import continuity_D
from core.limits.continuity_H import continuity_H
from core.limits.continuity_error import continuity_error
from core.limits.limit_branching import branching_term, limit_branching
from core.limits.limit_compression import compression_term, limit_compression


def test_branching_limit_is_fullness_without_numeric_threshold():
    assert branching_term(0) == pytest.approx(1.0)
    assert branching_term(3) == pytest.approx(8.0)
    assert limit_branching() == PI


def test_compression_limit_is_potential_without_numeric_threshold():
    assert compression_term(8.0, 0) == pytest.approx(8.0)
    assert compression_term(8.0, 3) == pytest.approx(1.0)
    assert limit_compression(8.0) == OMEGA


def test_continuity_error_matches_limit_contract_for_linear_operator():
    sequence = [0.5, 0.75, 0.875, 1.0]
    assert continuity_error(lambda value: value * 2.0, sequence, x_limit=1.0) == pytest.approx(0.0)


def test_continuity_d_and_h_are_zero_on_observed_limit():
    sequence = [1.0, 1.5, 1.75, 2.0]
    assert continuity_D(sequence) == pytest.approx(0.0)
    assert continuity_H(sequence) == pytest.approx(0.0)


def test_continuity_error_reports_mismatch_when_limit_disagrees_with_sequence_tail():
    sequence = [1.0, 1.5, 2.0]
    assert continuity_error(lambda value: value * 2.0, sequence, x_limit=3.0) == pytest.approx(2.0)


def test_dual_epsilon_square_is_limit_potential():
    assert EPSILON_SQUARED == OMEGA
