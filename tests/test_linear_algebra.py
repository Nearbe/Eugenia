import math

import pytest

from core.linear_algebra import CoreMatrix, dot, mat_vec, matmul, matrix_shape, norm, to_matrix


def test_vector_norm_and_dot():
    assert norm([3, 4]) == pytest.approx(5.0)
    assert dot([1, 2, 3], [4, 5, 6]) == pytest.approx(32.0)


def test_dot_shape_mismatch_raises():
    with pytest.raises(ValueError):
        dot([1, 2], [1])


def test_rectangular_matrix_shape_and_matmul():
    left = CoreMatrix([[1, 2, 3], [4, 5, 6]])
    right = CoreMatrix([[7, 8], [9, 10], [11, 12]])
    assert matrix_shape(left) == (2, 3)
    assert matrix_shape(right) == (3, 2)
    assert matmul(left, right) == [[58, 64], [139, 154]]


def test_ragged_matrix_validation():
    with pytest.raises(ValueError):
        CoreMatrix([[1, 2], [3]])
    with pytest.raises(ValueError):
        to_matrix([[1, 2], [3]])


def test_matmul_shape_mismatch_raises():
    with pytest.raises(ValueError):
        matmul([[1, 2]], [[1, 2]])


def test_mat_vec_shape_mismatch_raises():
    with pytest.raises(ValueError):
        mat_vec([[1, 2, 3]], [1, 2])
