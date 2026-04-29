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
from core.foundations.lo_shu import LoShuOperation, digit_address, operation_address
from core.fractal.solenoid_point import solenoid_seed_from_lo_shu
from nucleus.nucleus_seed_system import deterministic_vector, lo_shu_seed_from_tokens


def test_digit_address_unfolds_directly_into_solenoid_seed():
    address = digit_address(9)

    seed = solenoid_seed_from_lo_shu(address)

    assert seed.phase == 0.9
    assert seed.history == (1, 0, 0, 1)


def test_operation_address_is_also_lo_shu_addressed():
    address = operation_address(LoShuOperation.BRANCH)

    seed = solenoid_seed_from_lo_shu(address)

    assert address.digit == 9
    assert seed.history == (1, 0, 0, 1, 1, 0, 0, 1)


def test_nucleus_seed_uses_lo_shu_path_not_hash_normalization():
    seed = lo_shu_seed_from_tokens(("D", "9", "H"))

    assert seed.solenoid.history == (
        1, 0, 0, 1, 1, 0, 0, 1,
        1, 0, 0, 1,
        0, 0, 0, 1, 0, 0, 0, 1,
    )
    assert list(seed.vector) == [float(bit) for bit in seed.solenoid.history]


def test_compatibility_vector_repeats_lo_shu_bits_without_normalizing_weights():
    vector = deterministic_vector(("D", "9"), size=8)

    assert list(vector) == [1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0]
