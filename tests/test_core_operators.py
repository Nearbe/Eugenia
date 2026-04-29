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

from core.foundations.logarithmic_axis import LOG_NEGATIVE_INFINITY
from core.foundations.safe_divide import safe_divide
from core.operators.D import D
from core.operators.H import H
from core.operators.L import L


def test_d_h_are_inverse_on_scalars():
    for value in [-3.5, 0.0, 2.0, 10]:
        assert H(D(value)) == pytest.approx(float(value))
        assert D(H(value)) == pytest.approx(float(value))


def test_d_h_are_inverse_on_lists():
    values = [1, -2.5, 0.0, 8]
    assert H(D(values)) == pytest.approx([float(value) for value in values])
    assert D(H(values)) == pytest.approx([float(value) for value in values])


def test_l_binary_depth_and_zero_sentinel():
    assert L(1) == pytest.approx(0.0)
    assert L(2) == pytest.approx(1.0)
    assert L(8) == pytest.approx(3.0)
    assert L(-4) == pytest.approx(2.0)
    assert L(0) == LOG_NEGATIVE_INFINITY
    assert L([1, 2, 4]) == pytest.approx([0.0, 1.0, 2.0])


def test_safe_divide_pins_u_system_zero_contract():
    assert safe_divide(7, 0) == pytest.approx(14.0)
    assert safe_divide(7, 2) == pytest.approx(3.5)
    assert safe_divide(9, 3) == pytest.approx(3.0)
