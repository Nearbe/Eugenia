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
from core.computation.interaction import (
    ComputabilityState,
    analyze_halting_by_regression,
    interaction_cycle,
    recursive_step,
    regressive_step,
)


def test_recursion_and_regression_form_information_preserving_cycle():
    assert recursive_step(3) == 6.0
    assert regressive_step(6) == 3.0
    assert interaction_cycle(3) == 3.0


def test_halting_is_detected_by_reverse_connectivity_from_stop():
    previous = {
        "STOP": ["B"],
        "B": ["A"],
        "A": ["START"],
        "START": [],
    }

    result = analyze_halting_by_regression(
        "START",
        "STOP",
        lambda state: previous[state],
        max_depth=3,
    )

    assert result.state == ComputabilityState.HALTS
    assert result.halts
    assert result.path == ("STOP", "B", "A", "START")
    assert set(result.regression_frontier) == {"STOP", "B", "A", "START"}


def test_missing_start_in_regression_frontier_marks_cycle():
    previous = {
        "STOP": ["B"],
        "B": ["A"],
        "A": [],
        "START": [],
    }

    result = analyze_halting_by_regression(
        "START",
        "STOP",
        lambda state: previous[state],
        max_depth=3,
    )

    assert result.state == ComputabilityState.CYCLES
    assert not result.halts
    assert result.path == ()
