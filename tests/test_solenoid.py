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

from core.fractal.encode_solenoid_trajectory import encode_solenoid_trajectory
from core.fractal.solenoid_distance import solenoid_distance
from core.fractal.solenoid_point import SolenoidPoint, d_adic_norm_from_depth
from core.fractal.solenoid_similarity import solenoid_similarity


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


def test_solenoid_point_keeps_phase_and_history_together():
    point = SolenoidPoint.from_value(1.625, depth=4)

    assert point.phase == pytest.approx(0.625)
    assert point.history == (1, 0, 1, 0)
    assert point.shift() == SolenoidPoint(0.25, (0, 1, 0))


def test_solenoid_point_d_adic_norm_is_shared_prefix_depth():
    left = SolenoidPoint(0.625, (1, 0, 0))
    right = SolenoidPoint(0.875, (1, 0, 1))

    assert left.shared_depth(right) == 2
    assert left.d_adic_norm(right) == pytest.approx(d_adic_norm_from_depth(2))
