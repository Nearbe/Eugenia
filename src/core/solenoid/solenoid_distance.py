"""Prefix metric on solenoid binary histories."""


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
def _validate_bits(trajectory: list[int]) -> list[int]:
    bits = [int(bit) for bit in trajectory]
    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("solenoid trajectories must contain only 0/1 bits")
    return bits


def solenoid_distance(traj_a: list[int], traj_b: list[int]) -> float:
    """Return ``0`` for equal histories, otherwise ``2**(-common_prefix_len)``.

    Strict prefixes are not identical: if one finite trajectory is a prefix of
    the other, the distance is positive and depends on the shared prefix length.
    """
    bits_a = _validate_bits(traj_a)
    bits_b = _validate_bits(traj_b)
    common = 0
    for left, right in zip(bits_a, bits_b):
        if left != right:
            return 2.0 ** (-common)
        common += 1
    if len(bits_a) == len(bits_b):
        return 0.0
    return 2.0 ** (-common)
