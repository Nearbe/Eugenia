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

from core.foundations.constants import D_ID, OMEGA
from core.foundations.rational import ParticipationRatio, participation_ratio
from core.foundations.u_algebra import divide, multiply


def test_participation_ratio_rejects_omega_denominator():
    with pytest.raises(ValueError, match="denominator must not be Ω"):
        participation_ratio(1, OMEGA)


def test_participation_ratio_collapses_through_u_division():
    ratio = participation_ratio(3, 4)

    assert ratio.value() == pytest.approx(0.75)
    assert float(ratio) == pytest.approx(0.75)


def test_branching_preserves_participation_relation():
    ratio = participation_ratio(3, 4)
    branched = ratio.branch()

    assert branched == ParticipationRatio(6.0, 8.0)
    assert branched.value() == pytest.approx(ratio.value())
    assert divide(ratio, OMEGA) == branched


def test_compression_preserves_participation_relation():
    ratio = participation_ratio(6, 8)
    compressed = ratio.compress()

    assert compressed == ParticipationRatio(3.0, 4.0)
    assert compressed.value() == pytest.approx(ratio.value())
    assert divide(ratio, D_ID) == compressed


def test_same_denominator_addition_keeps_shared_whole():
    left = participation_ratio(1, 4)
    right = participation_ratio(2, 4)

    assert left.add(right) == ParticipationRatio(3.0, 4)


def test_ratio_multiplication_multiplies_both_parts():
    left = participation_ratio(1, 2)
    right = participation_ratio(3, 5)

    assert multiply(left, right) == ParticipationRatio(3.0, 10.0)
