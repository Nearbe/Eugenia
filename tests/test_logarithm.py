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

from core.foundations.constants import OMEGA
from core.foundations.infinity import PI
from core.foundations.logarithmic_axis import (
    LOG_NEGATIVE_INFINITY,
    LOG_POSITIVE_INFINITY,
    depth_add,
    depth_scale,
)
from core.foundations.spine import spine_level
from core.operators.L import L
from core.transcendental.ln import ln
from core.transcendental.log2 import log2


def test_l_maps_omega_and_fullness_to_log_axis_infinities():
    assert L(OMEGA) == LOG_NEGATIVE_INFINITY
    assert L(PI) == LOG_POSITIVE_INFINITY


def test_l_reads_spine_and_finite_depths():
    assert L(spine_level(2.5)) == pytest.approx(2.5)
    assert L(8) == pytest.approx(3.0)


def test_log2_uses_algebraic_negative_infinity_for_potential():
    assert log2(OMEGA) == LOG_NEGATIVE_INFINITY
    assert log2(PI) == LOG_POSITIVE_INFINITY


def test_ln_uses_algebraic_axis_boundaries():
    assert ln(OMEGA) == LOG_NEGATIVE_INFINITY
    assert ln(PI) == LOG_POSITIVE_INFINITY


def test_log_axis_counts_infinities():
    assert depth_add(LOG_POSITIVE_INFINITY, 3) == LOG_POSITIVE_INFINITY
    assert depth_add(LOG_NEGATIVE_INFINITY, -3) == LOG_NEGATIVE_INFINITY
    assert depth_scale(LOG_POSITIVE_INFINITY, -1) == LOG_NEGATIVE_INFINITY
