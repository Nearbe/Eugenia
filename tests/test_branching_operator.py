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

from core.algebra.branching_operator import branching_operator
from core.constants.constants import D_ID, OMEGA
from core.algebra import add, branch, compress


def test_branching_operator_is_linear():
    operator = branching_operator()

    assert operator.apply(add(3, 5)) == pytest.approx(add(operator.apply(3), operator.apply(5)))
    assert operator.is_linear_on_pair(3, 5)


def test_branching_kernel_image_and_eigen_class_are_explicit():
    operator = branching_operator()

    assert operator.kernel() == frozenset({OMEGA})
    assert operator.image_is_carrier()
    assert operator.eigen_class() == D_ID


def test_branching_matrices_match_specification():
    operator = branching_operator()

    assert operator.scalar_matrix() == ((D_ID,),)
    assert operator.dual_matrix() == ((D_ID, OMEGA), (OMEGA, D_ID))


def test_branching_and_compression_are_inverse_operator_steps():
    operator = branching_operator()

    assert operator.inverse(operator.apply(9)) == pytest.approx(9.0)
    assert branch(compress(9)) == pytest.approx(9.0)
