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

from core.utils.vectorization import (
    is_scalar,
    is_vector,
    map_scalar_or_vector,
    vector_delta,
    zip_vectors,
)
from core.metrics.delta_distance import delta_distance
from core.metrics.euclidean_distance import euclidean_distance
from core.operators.D import D


def test_scalar_and_vector_contracts_are_explicit():
    assert is_scalar(1.0)
    assert not is_scalar(True)
    assert is_vector([1, 2, 3])
    assert not is_vector("123")


def test_map_scalar_or_vector_lifts_scalar_operator_componentwise():
    assert map_scalar_or_vector(2, lambda value: value + 1.0) == pytest.approx(3.0)
    assert map_scalar_or_vector([1, 2], lambda value: value + 1.0) == pytest.approx([2.0, 3.0])


def test_vector_delta_uses_spec_order_vb_minus_va():
    assert vector_delta([1, 2, 3], [3, 1, 5]) == pytest.approx([2.0, -1.0, 2.0])


def test_pairwise_vector_operations_reject_shape_mismatch():
    with pytest.raises(ValueError):
        zip_vectors([1, 2], [1], name="test")
    with pytest.raises(ValueError):
        euclidean_distance([1, 2], [1])
    with pytest.raises(ValueError):
        delta_distance([1, 2], [1])


def test_core_operators_still_lift_through_shared_vectorization():
    assert D([1, 2, 3]) == pytest.approx([2.0, 4.0, 6.0])
