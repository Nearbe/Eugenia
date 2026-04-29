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
from core.foundations.spine import SpineLevel, root, spine_level
from core.foundations.u_algebra import IDENTITY, branch, compress, divide, power
from core.operators.L import L


def test_spine_level_represents_d_power_of_identity():
    assert spine_level(0).value() == pytest.approx(1.0)
    assert spine_level(1).value() == pytest.approx(2.0)
    assert spine_level(4).value() == pytest.approx(16.0)


def test_spine_branching_moves_one_level_up():
    level = spine_level(2)

    assert branch(level) == SpineLevel(3.0)
    assert divide(level, OMEGA) == SpineLevel(3.0)


def test_spine_compression_moves_one_level_down_with_identity_fixed():
    assert compress(spine_level(3)) == SpineLevel(2.0)
    assert divide(spine_level(3), D_ID) == SpineLevel(2.0)
    assert compress(spine_level(0)) == SpineLevel(0.0)


def test_l_reads_spine_depth_directly():
    assert L(spine_level(0)) == 0
    assert L(spine_level(5)) == 5


def test_spine_power_scales_depth():
    assert power(spine_level(3), 2) == SpineLevel(6.0)
    assert power(spine_level(3), OMEGA) == IDENTITY


def test_spine_root_creates_fractional_step():
    rooted = root(spine_level(3), 2)

    assert rooted == SpineLevel(1.5)
    assert rooted.value() == D_ID**1.5
    assert L(rooted) == 1.5
