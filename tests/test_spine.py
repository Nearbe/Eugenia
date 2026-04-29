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
from core.foundations.spine import SpineLevel, spine_level
from core.foundations.u_algebra import branch, compress, divide
from core.operators.L import L


def test_spine_level_represents_d_power_of_identity():
    assert spine_level(0).value() == pytest.approx(1.0)
    assert spine_level(1).value() == pytest.approx(2.0)
    assert spine_level(4).value() == pytest.approx(16.0)


def test_spine_branching_moves_one_level_up():
    level = spine_level(2)

    assert branch(level) == SpineLevel(3)
    assert divide(level, OMEGA) == SpineLevel(3)


def test_spine_compression_moves_one_level_down_with_identity_fixed():
    assert compress(spine_level(3)) == SpineLevel(2)
    assert divide(spine_level(3), D_ID) == SpineLevel(2)
    assert compress(spine_level(0)) == SpineLevel(0)


def test_l_reads_spine_depth_directly():
    assert L(spine_level(0)) == 0
    assert L(spine_level(5)) == 5
