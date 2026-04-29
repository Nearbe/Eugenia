"""Distance between solenoid-like pattern trajectories."""


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
from core.linear.linear_algebra import to_vector


def solenoid_pattern_distance(pattern_a, pattern_b) -> float:
    values_a = to_vector(pattern_a)
    values_b = to_vector(pattern_b)

    if not values_a and not values_b:
        return 0.0
    if not values_a or not values_b:
        return 1.0

    length = min(len(values_a), len(values_b))
    mismatches = sum(1 for left, right in zip(values_a[:length], values_b[:length]) if left != right)
    length_penalty = abs(len(values_a) - len(values_b))
    return (mismatches + length_penalty) / max(len(values_a), len(values_b))
