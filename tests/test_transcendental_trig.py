#  Copyright (c) 2026.
#  ╔═════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═════════════════════════════════╝
"""Tests for transcendental trigonometric functions."""

import pytest

from core.transcendental import arctan, arctan2, cot, pi, sin, tan


def test_tan_pi_over_4_is_1():
    """tan(π/4) should be 1."""
    assert tan(float(pi() / 4)) == pytest.approx(1.0, rel=1e-3)


def test_cot_pi_over_4_is_1():
    """cot(π/4) should be 1."""
    assert cot(float(pi() / 4)) == pytest.approx(1.0, rel=1e-3)


def test_tan_0_is_0():
    """tan(0) should be 0."""
    assert tan(0.0) == pytest.approx(0.0)


def test_cot_pi_over_2_is_0():
    """cot(π/2) should be 0."""
    assert cot(float(pi() / 2)) == pytest.approx(0.0, abs=1e-3)


def test_arctan_1_is_pi_over_4():
    """arctan(1) should be π/4."""
    assert arctan(1.0) == pytest.approx(float(pi() / 4), rel=1e-2)


def test_arctan_0_is_0():
    """arctan(0) should be 0."""
    assert arctan(0.0) == pytest.approx(0.0)


def test_arctan2_1_1_is_pi_over_4():
    """arctan2(1, 1) should be π/4."""
    assert arctan2(1.0, 1.0) == pytest.approx(float(pi() / 4), rel=1e-2)


def test_arctan2_0_1_is_0():
    """arctan2(0, 1) should be 0."""
    assert arctan2(0.0, 1.0) == pytest.approx(0.0)


def test_arctan2_1_0_is_pi_over_2():
    """arctan2(1, 0) should be π/2."""
    assert arctan2(1.0, 0.0) == pytest.approx(float(pi() / 2), rel=1e-2)


def test_tan_and_cot_are_reciprocals():
    """tan(x) * cot(x) should be 1 for valid x."""
    x = float(pi() / 6)
    assert tan(x) * cot(x) == pytest.approx(1.0, rel=1e-3)
