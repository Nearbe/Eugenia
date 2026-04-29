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

from core.states.complex_plane import I, PI_Z, ComplexState, conjugate, norm_squared
from core.constants.constants import D_ID, OMEGA
from core.algebra import add, branch, compress, divide, multiply


def test_imaginary_unit_squares_to_negative_identity():
    assert multiply(I, I) == ComplexState(-1.0, 0.0)


def test_complex_branching_and_compression_scale_both_flows():
    state = ComplexState(3.0, -4.0)

    assert branch(state) == ComplexState(6.0, -8.0)
    assert divide(state, OMEGA) == ComplexState(6.0, -8.0)
    assert compress(state) == ComplexState(1.5, -2.0)
    assert divide(state, D_ID) == ComplexState(1.5, -2.0)


def test_complex_add_multiply_conjugate_and_norm():
    left = ComplexState(2.0, 3.0)
    right = ComplexState(4.0, -1.0)

    assert add(left, right) == ComplexState(6.0, 2.0)
    assert multiply(left, right) == ComplexState(11.0, 10.0)
    assert conjugate(left) == ComplexState(2.0, -3.0)
    assert norm_squared(left) == pytest.approx(13.0)


def test_complex_fullness_is_stable_under_branching():
    assert branch(PI_Z) == PI_Z
    assert compress(PI_Z) == PI_Z
    assert divide(PI_Z, OMEGA) == PI_Z
