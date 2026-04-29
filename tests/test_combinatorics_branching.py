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
from core.combinatorics.branching import (
    BranchingLevel,
    binomial_coefficient,
    boolean_capacity,
    branching_distribution,
    factorial,
    paths_count,
    routes,
)
from core.foundations.spine import spine_level


def test_paths_count_is_d_power_capacity():
    assert paths_count(0) == 1
    assert paths_count(1) == 2
    assert paths_count(5) == 32


def test_branching_level_tracks_spine_and_addresses():
    level = BranchingLevel(3)

    assert level.spine == spine_level(3)
    assert level.paths == 8
    assert level.branch() == BranchingLevel(4)
    assert level.address(5) == (1, 0, 1)


def test_binomial_coefficients_group_paths_by_right_choices():
    assert binomial_coefficient(5, 2) == 10
    assert branching_distribution(4) == (1, 4, 6, 4, 1)
    assert sum(branching_distribution(4)) == paths_count(4)


def test_factorial_counts_distinguishable_act_orderings():
    assert factorial(0) == 1
    assert factorial(5) == 120


def test_boolean_capacity_is_branching_tree_capacity():
    assert boolean_capacity(6) == 64


def test_routes_are_all_binary_addresses_at_depth():
    assert routes(2) == ((0, 0), (0, 1), (1, 0), (1, 1))
