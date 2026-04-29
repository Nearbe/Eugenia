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
from core.states.fullness_share import FullnessShare, fullness_share
from core.infinity.infinity import PI
from core.algebra import IDENTITY, add, branch, compress, divide, multiply


def test_absolute_fullness_stays_full_under_direct_compression():
    assert divide(PI, D_ID) == PI


def test_fullness_share_compression_changes_participation_intensity():
    share = fullness_share(PI)

    assert compress(share) == FullnessShare(PI)
    assert compress(fullness_share(8)) == FullnessShare(4.0)
    assert divide(fullness_share(8), D_ID) == FullnessShare(4.0)


def test_equal_fullness_shares_birth_identity():
    half = fullness_share(4)

    assert divide(half, half) == IDENTITY


def test_share_operations_follow_percentage_algebra():
    left = fullness_share(2)
    right = fullness_share(3)

    assert add(left, right) == FullnessShare(5.0)
    assert multiply(left, right) == FullnessShare(6.0)
    assert divide(left, right) == pytest.approx(2 / 3)


def test_share_branching_doubles_participation():
    assert branch(fullness_share(7)) == FullnessShare(14.0)
    assert divide(fullness_share(7), OMEGA) == FullnessShare(14.0)
