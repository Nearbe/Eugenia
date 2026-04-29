"""Pattern similarity using complex delta coordinates via Eugenia core math."""

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
from core.linear.linear_algebra import cosine_similarity
from core.operators.complex_delta_field import complex_delta_field


def pattern_similarity_from_complex(values_a, values_b) -> float:
    complex_a = [abs(value) for value in complex_delta_field(values_a)]
    complex_b = [abs(value) for value in complex_delta_field(values_b)]
    return float(cosine_similarity(complex_a, complex_b))
