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
from core.foundations.lo_shu import active_principles, compute_invariants, is_magic_square, magic_sum, residual_sum


def test_lo_shu_magic_square_axiom():
    assert magic_sum() == 15
    assert is_magic_square()


def test_lo_shu_active_principles_exclude_duality():
    assert active_principles() == 22


def test_lo_shu_operational_invariants_are_computed_from_specification():
    invariants = compute_invariants()

    assert invariants.context == 1_048_576
    assert invariants.rope_scale == 198
    assert invariants.rope_base == 891
    assert invariants.layers == 88
    assert invariants.gpu_layers == 66
    assert invariants.cpu_layers == 22
    assert invariants.load_threads == 1
    assert invariants.inference_threads == 3
    assert invariants.kv_bits == 16
    assert residual_sum(invariants) == 0
