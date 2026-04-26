#!/usr/bin/env python3
"""Universal Knowledge Map on Eugenia core math."""

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
import random
from dataclasses import dataclass
from typing import Dict, List

from core.linear_algebra import (
    CoreMatrix,
    CoreVector,
    cosine_similarity,
    linspace,
    mat_vec,
    matmul,
    norm,
    to_matrix,
    to_vector,
)

DEFAULT_RANDOM_SEED = 42
EPSILON = 1.0e-10


@dataclass
class UniversalKnowledgeMap:
    """Универсальная карта знаний — детерминированное отображение."""

    pattern_matrix: CoreMatrix
    singular_values: CoreVector

    def __init__(self, pattern_matrix, singular_values):
        self.pattern_matrix = to_matrix(pattern_matrix)
        self.singular_values = CoreVector(to_vector(singular_values))
        self.k = len(self.singular_values)

    def project(self, x) -> CoreVector:
        projected = mat_vec(self.pattern_matrix.T, x)
        return CoreVector(
            value * self.singular_values[index]
            for index, value in enumerate(projected[: len(self.singular_values)])
        )

    def similarity(self, x1, x2) -> float:
        p1 = self.project(x1)
        p2 = self.project(x2)
        if norm(p1) < EPSILON or norm(p2) < EPSILON:
            return 0.0
        return cosine_similarity(p1, p2)

    def encode(self, x) -> CoreVector:
        return self.project(x)

    def decode(self, pattern_coords) -> CoreVector:
        return mat_vec(self.pattern_matrix, pattern_coords)


class KnowledgeNavigator:
    """Навигатор по универсальной карте знаний."""

    def __init__(self, knowledge_map: UniversalKnowledgeMap):
        self.map = knowledge_map

    def find_similar(self, query, candidates: List[object], top_k: int = 5) -> List[tuple]:
        query_p = self.map.project(query)
        similarities = []
        for index, candidate in enumerate(candidates):
            cand_p = self.map.project(candidate)
            sim = cosine_similarity(query_p, cand_p)
            similarities.append((index, sim, cand_p))
        similarities.sort(key=lambda item: item[1], reverse=True)
        return similarities[:top_k]

    def cluster(self, items: List[object]) -> List[List[int]]:
        projections = [self.map.project(item) for item in items]
        clusters: dict[tuple[int, int], list[int]] = {}
        for index, projection in enumerate(projections):
            first = projection[0] if projection else 0.0
            second = projection[1] if len(projection) > 1 else 0.0
            key = (int(first * 2), int(second * 2))
            clusters.setdefault(key, []).append(index)
        return list(clusters.values())

    def dimension_analysis(self, item) -> Dict:
        projection = self.map.project(item)
        ranked = sorted(range(len(projection)), key=lambda index: abs(projection[index]), reverse=True)[:5]
        return {
            "pattern_dims": ranked,
            "pattern_weights": [projection[index] for index in ranked],
            "total_activation": norm(projection),
            "dimensionality": float(sum(1 for value in projection if value != 0.0)),
        }


def _random_matrix(rows: int, cols: int, seed: int = DEFAULT_RANDOM_SEED) -> CoreMatrix:
    rng = random.Random(seed)
    return CoreMatrix([[rng.gauss(0.0, 0.1) for _ in range(cols)] for _ in range(rows)])


def demonstrate_universal_mapping():
    d_model = 32
    k = 8
    pattern_matrix = _random_matrix(d_model, k)
    singular_values = CoreVector(linspace(1.0, 0.1, k))
    knowledge_map = UniversalKnowledgeMap(pattern_matrix, singular_values)
    test_input = CoreVector([0.5 for _ in range(d_model)])
    projections = [knowledge_map.project(test_input) for _ in range(3)]
    print(all(projection == projections[0] for projection in projections))
    navigator = KnowledgeNavigator(knowledge_map)
    print(navigator.cluster([test_input, CoreVector([0.25 for _ in range(d_model)])]))


def demonstrate_gpt_embedding():
    print("Input is projected into deterministic core pattern coordinates.")


if __name__ == "__main__":
    demonstrate_universal_mapping()
    demonstrate_gpt_embedding()
