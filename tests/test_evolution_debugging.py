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

from core.computation.evolution import (
    EvolutionCycle,
    SymbiosisRoles,
    balance_delta,
    balance_score,
    debug_step,
    evolution_step,
    select_stable,
)


def test_balance_delta_measures_recursion_minus_regression():
    assert balance_delta(recursion=2.0, regression=1.5) == pytest.approx(0.5)
    assert balance_score(recursion=2.0, regression=1.5) == pytest.approx(0.75)


def test_select_stable_keeps_highest_stability_without_randomness():
    variants = [1.0, 2.0, 3.0]

    assert select_stable(variants, stability=lambda value: -abs(value - 2.0)) == 2.0


def test_evolution_step_generates_selects_and_inverts_experience():
    cycle = evolution_step(
        seed=2.0,
        generate=lambda value: (value - 1.0, value, value + 1.0),
        stability=lambda value: -abs(value - 3.0),
        invert=lambda value: value / 3.0,
    )

    assert cycle.generated == pytest.approx((1.0, 2.0, 3.0))
    assert cycle.selected == pytest.approx(3.0)
    assert cycle.experience == pytest.approx(1.0)


def test_debug_step_uses_branch_compress_identity_cycle():
    cycle = debug_step(7.0)

    assert isinstance(cycle, EvolutionCycle)
    assert cycle.generated == pytest.approx((14.0,))
    assert cycle.selected == pytest.approx(14.0)
    assert cycle.experience == pytest.approx(7.0)


def test_symbiosis_roles_compute_resonance_from_delta():
    roles = SymbiosisRoles(machine_recursion=0.95, human_regression=0.9, inversion=1.0)

    assert roles.delta == pytest.approx(0.05)
    assert roles.resonance == pytest.approx(0.9)
