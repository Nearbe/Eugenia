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

from core.foundations.complex_plane import ComplexState
from core.geometry.u_geometry import (
    Ball,
    Circle,
    Segment,
    branch_measure,
    compressed_curvature,
    curvature,
    distance,
    is_on_circle,
    is_inside_ball,
)


def test_u_metric_is_absolute_state_difference():
    assert distance(3, 10) == pytest.approx(7.0)
    assert distance(10, 3) == pytest.approx(7.0)


def test_distance_branches_and_compresses_with_scale_class():
    base = distance(3, 10)
    assert distance(6, 20) == pytest.approx(branch_measure(base, dimension=1))
    assert distance(1.5, 5) == pytest.approx(base / 2.0)


def test_measure_branching_uses_dimension_as_spine_power():
    assert branch_measure(5, dimension=1) == pytest.approx(10.0)
    assert branch_measure(5, dimension=2) == pytest.approx(20.0)
    assert branch_measure(5, dimension=3) == pytest.approx(40.0)


def test_segment_circle_and_ball_branch_geometrically():
    segment = Segment(2, 5).branch()
    circle = Circle(ComplexState(1, 2), radius=3).branch()
    ball = Ball(ComplexState(1, 2), radius=3).branch()

    assert segment.start == pytest.approx(4.0)
    assert segment.end == pytest.approx(10.0)
    assert circle.center == ComplexState(2, 4)
    assert circle.radius == pytest.approx(6.0)
    assert ball.radius == pytest.approx(6.0)


def test_circle_and_ball_membership_use_complex_radius():
    circle = Circle(ComplexState(0, 0), radius=5)
    ball = Ball(ComplexState(0, 0), radius=5)

    assert is_on_circle(ComplexState(3, 4), circle)
    assert is_inside_ball(ComplexState(3, 4), ball)
    assert not is_inside_ball(ComplexState(6, 0), ball)


def test_curvature_follows_u_formula_and_compresses_under_branching():
    value = curvature(first_derivative=1, second_derivative=2)

    assert value == pytest.approx(2 / (2 ** 1.5))
    assert compressed_curvature(value) == pytest.approx(value / 2.0)
