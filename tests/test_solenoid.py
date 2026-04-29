import pytest

from core import encode_solenoid_trajectory, solenoid_distance, solenoid_similarity


def test_binary_fraction_encoding_extracts_fractional_bits():
    assert encode_solenoid_trajectory(0.625, depth=4) == [1, 0, 1, 0]
    assert encode_solenoid_trajectory(0.25, depth=4) == [0, 1, 0, 0]
    assert encode_solenoid_trajectory(1.625, depth=4) == [1, 0, 1, 0]


def test_solenoid_distance_exact_equality():
    trajectory = [1, 0, 1, 1]
    assert solenoid_distance(trajectory, trajectory.copy()) == 0.0
    assert solenoid_similarity(trajectory, trajectory.copy()) == 1.0


def test_solenoid_distance_first_bit_mismatch():
    assert solenoid_distance([0, 1, 1], [1, 1, 1]) == pytest.approx(1.0)
    assert solenoid_similarity([0, 1, 1], [1, 1, 1]) == pytest.approx(0.0)


def test_solenoid_distance_partial_common_prefix():
    assert solenoid_distance([1, 0, 0], [1, 0, 1]) == pytest.approx(0.25)
    assert solenoid_similarity([1, 0, 0], [1, 0, 1]) == pytest.approx(0.75)


def test_solenoid_distance_strict_prefix_is_positive():
    assert solenoid_distance([1, 0], [1, 0, 1]) == pytest.approx(0.25)


def test_solenoid_rejects_non_binary_trajectories():
    with pytest.raises(ValueError):
        solenoid_distance([0, 2], [0, 1])
