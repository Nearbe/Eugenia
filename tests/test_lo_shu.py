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
from core.foundations.lo_shu import (
    Direction,
    active_principles,
    compute_equations,
    corners,
    is_magic_square,
    key_numbers,
    magic_sum,
    position,
    residual_sum,
    value,
)


def test_lo_shu_positions_are_fixed_to_directions():
    assert value(Direction.NORTH_WEST) == 4
    assert value(Direction.NORTH) == 9
    assert value(Direction.NORTH_EAST) == 2
    assert value(Direction.WEST) == 3
    assert value(Direction.CENTER) == 5
    assert value(Direction.SOUTH) == 1
    assert position(Direction.CENTER).row == 1
    assert position(Direction.CENTER).column == 1


def test_lo_shu_magic_square_axiom():
    assert magic_sum() == 15
    assert is_magic_square()


def test_lo_shu_key_numbers_and_corners_keep_positional_meaning():
    assert key_numbers() == (1, 2, 3, 4, 5, 9)
    assert corners() == (4, 2, 8, 6)
    assert active_principles() == 22


def test_lo_shu_equations_are_derived_from_fixed_positions():
    equations = compute_equations()

    assert equations.context == 1_048_576
    assert equations.rope_scale == 198
    assert equations.rope_base == 891
    assert equations.layers == 88
    assert equations.gpu_layers == 66
    assert equations.cpu_layers == 22
    assert equations.load_threads == 1
    assert equations.inference_threads == 3
    assert equations.kv_bits == 16
    assert residual_sum(equations) == 0
