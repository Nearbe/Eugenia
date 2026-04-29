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

from core.continuity_D import continuity_D
from core.continuity_H import continuity_H
from core.continuity_error import continuity_error


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
