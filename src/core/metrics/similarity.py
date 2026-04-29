"""Cosine similarity between vectors."""
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
from ..linear.vec_norm import vec_norm
from ..utils.vectorization import to_vector, zip_vectors


def similarity(a: list[float], b: list[float]) -> float:
    values_a = to_vector(a, name="similarity left")
    values_b = to_vector(b, name="similarity right")
    dot = sum(left * right for left, right in zip_vectors(values_a, values_b, name="similarity"))
    norm_a = vec_norm(values_a)
    norm_b = vec_norm(values_b)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)
