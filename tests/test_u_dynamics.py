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
from pytest import approx

from core.dynamics import (
    DynamicStep,
    invariant_measure_holds,
    lyapunov_exponent,
    orbit,
    oscillation,
    period_cycle,
)
from core.states.spine import spine_level


def test_orbit_applies_d_and_h_word_in_order():
    trajectory = orbit(3.0, (DynamicStep.BRANCH, DynamicStep.COMPRESS, DynamicStep.BRANCH))

    assert trajectory.seed == approx(3.0)
    assert trajectory.states == approx((3.0, 6.0, 3.0, 6.0))
    assert trajectory.final == approx(6.0)


def test_oscillation_returns_to_initial_state():
    assert oscillation(5.0).states == approx((5.0, 10.0, 5.0))


def test_period_cycle_repeats_growth_and_return():
    cycle = period_cycle(2.0, periods=3)

    assert cycle.states == approx((2.0, 4.0, 2.0, 4.0, 2.0, 4.0, 2.0))


def test_lyapunov_exponent_is_log_depth_of_branch_class():
    assert lyapunov_exponent() == approx(1.0)


def test_invariant_measure_holds_for_doubling_preimage():
    measure = {0: 0.5, 1: 0.5}
    preimage = {0: (0, 1)}

    assert invariant_measure_holds(measure, preimage, 0)


def test_orbit_works_on_spine_levels():
    trajectory = orbit(spine_level(2), (DynamicStep.BRANCH, DynamicStep.COMPRESS))

    assert trajectory.final == spine_level(2)
