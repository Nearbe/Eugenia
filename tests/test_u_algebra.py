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
from core.foundations.infinity import PI
from core.foundations.u_algebra import (
    IDENTITY,
    add,
    branch,
    compress,
    divide,
    is_identity,
    is_omega,
    multiply,
    power,
)


def test_basic_u_algebra_uses_ordinary_arithmetic_away_from_omega():
    assert add(2, 3) == pytest.approx(5.0)
    assert multiply(2, 3) == pytest.approx(6.0)
    assert divide(6, 3) == pytest.approx(2.0)
    assert power(3, 2) == pytest.approx(9.0)


def test_division_by_omega_branches_finite_values():
    assert divide(7, OMEGA) == pytest.approx(14.0)
    assert divide([1, 2, -3], OMEGA) == pytest.approx([2.0, 4.0, -6.0])


def test_omega_division_rules_keep_potential_closed():
    assert divide(OMEGA, 3) == OMEGA
    assert divide(OMEGA, OMEGA) == OMEGA
    assert multiply(OMEGA, 5) == OMEGA


def test_branch_and_compress_are_inverse_scale_steps():
    assert compress(branch(9)) == pytest.approx(9.0)
    assert branch(compress(9)) == pytest.approx(9.0)
    assert divide(9, D_ID) == pytest.approx(4.5)


def test_fullness_is_closed_under_core_operations():
    assert divide(PI, OMEGA) == PI
    assert divide(PI, D_ID) == PI
    assert divide(PI, PI) == IDENTITY
    assert add(PI, PI) == PI
    assert multiply(PI, PI) == PI
    assert power(PI, 5) == PI


def test_omega_power_and_identity_predicates():
    assert power(5, OMEGA) == IDENTITY
    assert power(OMEGA, OMEGA) == OMEGA
    assert is_omega(OMEGA)
    assert is_identity(IDENTITY)
