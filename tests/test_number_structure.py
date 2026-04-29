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
from core.states.spine import spine_level
from core.number_theory.number_structure import (
    binary_address,
    branched_spine_gcd,
    branched_spine_lcm,
    branching_preserves_congruence,
    congruent,
    is_composite_spine,
    is_system_atom,
    modulus_from_depth,
    spine_gcd,
    spine_lcm,
    system_atom,
)


def test_d_id_is_the_only_system_atom():
    assert system_atom() == spine_level(1)
    assert is_system_atom(spine_level(1))
    assert not is_system_atom(spine_level(2))
    assert is_composite_spine(spine_level(2))


def test_spine_gcd_and_lcm_are_common_ancestor_and_descendant():
    left = spine_level(3)
    right = spine_level(5)

    assert spine_gcd(left, right) == spine_level(3)
    assert spine_lcm(left, right) == spine_level(5)


def test_branching_preserves_spine_kinship():
    left = spine_level(3)
    right = spine_level(5)

    assert branched_spine_gcd(left, right) == spine_level(4)
    assert branched_spine_lcm(left, right) == spine_level(6)


def test_congruence_branching_doubles_indistinguishability_modulus():
    assert congruent(3, 7, modulus=4)
    assert branching_preserves_congruence(3, 7, modulus=4)
    assert congruent(6, 14, modulus=8)


def test_binary_address_is_residue_mod_d_power_as_word():
    assert modulus_from_depth(4) == 16
    assert binary_address(13, depth=4) == (1, 1, 0, 1)
    assert binary_address(29, depth=4) == (1, 1, 0, 1)
