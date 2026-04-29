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

from core.utils.logarithmic_axis import LOG_POSITIVE_INFINITY
from core.metrics.p_adic_distance import p_adic_distance
from core.number_theory.v2_adic_valuation import v2_adic_valuation


def test_v2_zero_has_infinite_valuation():
    assert v2_adic_valuation(0) == LOG_POSITIVE_INFINITY


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1, 0.0),
        (2, 1.0),
        (4, 2.0),
        (12, 2.0),
        (24, 3.0),
        (-8, 3.0),
    ],
)
def test_v2_integer_valuation(value, expected):
    assert v2_adic_valuation(value) == pytest.approx(expected)


def test_p_adic_distance_identity_is_zero():
    assert p_adic_distance(5, 5) == 0.0
    assert p_adic_distance([1, 2, 3], [1, 2, 3]) == [0.0, 0.0, 0.0]


def test_p_adic_distance_integer_formula():
    assert p_adic_distance(3, 7) == pytest.approx(0.25)  # difference 4
    assert p_adic_distance(1, 3) == pytest.approx(0.5)   # difference 2
    assert p_adic_distance(2, 5) == pytest.approx(1.0)   # difference 3


def test_p_adic_integer_ultrametric_inequality():
    triples = [(0, 2, 6), (1, 5, 9), (3, 7, 11), (4, 12, 20)]
    for x, y, z in triples:
        d_xz = p_adic_distance(x, z)
        d_xy = p_adic_distance(x, y)
        d_yz = p_adic_distance(y, z)
        assert d_xz <= max(d_xy, d_yz)


def test_p_adic_vector_length_mismatch_raises():
    with pytest.raises(ValueError):
        p_adic_distance([1, 2], [1])
