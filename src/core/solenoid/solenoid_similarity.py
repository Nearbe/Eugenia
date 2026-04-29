"""Similarity score derived from the solenoid prefix metric."""

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
from .solenoid_distance import solenoid_distance


def solenoid_similarity(traj_a: list[int], traj_b: list[int]) -> float:
    """Map solenoid distance to a stable score in ``[0, 1]``.

    Equal trajectories have similarity ``1``; a first-bit mismatch has
    similarity ``0``; longer shared prefixes approach ``1``.
    """
    return max(0.0, min(1.0, 1.0 - solenoid_distance(traj_a, traj_b)))
