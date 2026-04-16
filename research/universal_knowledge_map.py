#!/usr/bin/env python3
"""
Universal Knowledge Map
=====================

ЭТО КЛЮЧЕВОЕ:
- Паттерны = универсальная карта знаний
- Relationship matrix = универсальные правила
- ANY input → SAME output (deterministic mapping)

Это как:
- GPS координаты — одинаковы для всех
- Математика — 2+2=4 для всех
- Это БАЗА ЗНАНИЙ в чистом виде!
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Callable, Optional


@dataclass
class UniversalKnowledgeMap:
    """
    Универсальная карта знаний

    Принцип:
    - ANY input → deterministic pattern projection
    - ANY two inputs can be compared by their pattern projections
    - This is the SAME mapping that the model learned!
    """

    # Pattern matrix (learned from ANY data)
    pattern_matrix: np.ndarray  # (d_model, k) — universal for all inputs

    # Singular values (importance weights)
    singular_values: np.ndarray  # (k,) — also universal

    def __init__(self, pattern_matrix: np.ndarray, singular_values: np.ndarray):
        self.pattern_matrix = pattern_matrix
        self.singular_values = singular_values
        self.k = len(singular_values)

    def project(self, x: np.ndarray) -> np.ndarray:
        """
        PROJECT input to pattern space

        This is DETERMINISTIC — always the same for same input!
        x → pattern projection → deterministic vector
        """
        # Project through learned patterns
        projected = self.pattern_matrix.T @ x  # (k,)

        # Scale by learned importance
        scaled = projected * self.singular_values

        return scaled

    def similarity(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """
        Compare ANY two inputs by their PATTERNS

        x1 → project → p1
        x2 → project → p2
        compare(p1, p2) → semantic similarity

        NO decoding needed! Just projections!
        """
        p1 = self.project(x1)
        p2 = self.project(x2)

        # Cosine similarity in pattern space
        norm1 = np.linalg.norm(p1)
        norm2 = np.linalg.norm(p2)

        if norm1 < 1e-10 or norm2 < 1e-10:
            return 0.0

        return np.dot(p1, p2) / (norm1 * norm2)

    def encode(self, x: np.ndarray) -> np.ndarray:
        """Universal encoding of ANY input"""
        return self.project(x)

    def decode(self, pattern_coords: np.ndarray) -> np.ndarray:
        """Universal decoding from pattern space"""
        return self.pattern_matrix @ pattern_coords


class KnowledgeNavigator:
    """
    Навигатор по универсальной карте знаний

    Вместо "дай мне факт X"
    Теперь: "найди паттерн, близкий к Y"
    """

    def __init__(self, knowledge_map: UniversalKnowledgeMap):
        self.map = knowledge_map

    def find_similar(
        self, query: np.ndarray, candidates: List[np.ndarray], top_k: int = 5
    ) -> List[tuple]:
        """
        Find most similar to query WITHOUT model inference!

        Just pattern projections!
        """
        query_p = self.map.project(query)

        similarities = []
        for i, candidate in enumerate(candidates):
            cand_p = self.map.project(candidate)
            sim = np.dot(query_p, cand_p) / (
                np.linalg.norm(query_p) * np.linalg.norm(cand_p) + 1e-10
            )
            similarities.append((i, sim, cand_p))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def cluster(self, items: List[np.ndarray]) -> List[List[int]]:
        """
        Cluster items by pattern similarity

        Items with similar patterns → same cluster
        """
        projections = [self.map.project(x) for x in items]

        # Simple clustering by angle in pattern space
        clusters = {}

        for i, p in enumerate(projections):
            # Use first two dimensions for clustering (simplified)
            key = (int(p[0] * 2), int(p[1] * 2))

            if key not in clusters:
                clusters[key] = []
            clusters[key].append(i)

        return list(clusters.values())

    def dimension_analysis(self, item: np.ndarray) -> Dict:
        """
        Analyze which "dimensions of knowledge" this item activates

        Returns which pattern combinations are active
        """
        projection = self.project(item)

        # Top pattern dimensions
        top_indices = np.argsort(np.abs(projection))[-5:][::-1]

        return {
            "pattern_dims": top_indices.tolist(),
            "pattern_weights": projection[top_indices].tolist(),
            "total_activation": float(np.linalg.norm(projection)),
            "dimensionality": float(np.sum(projection != 0)),
        }


def demonstrate_universal_mapping():
    """Демонстрация универсальной карты"""
    print("=" * 60)
    print("UNIVERSAL KNOWLEDGE MAP")
    print("=" * 60)

    np.random.seed(42)

    # Create a "model" — learned patterns from training
    d_model = 512
    k = 32

    # These could come from ANY trained model
    # They represent the universal "knowledge structure"
    pattern_matrix = np.random.randn(d_model, k) * 0.1
    singular_values = np.random.rand(k)

    map = UniversalKnowledgeMap(pattern_matrix, singular_values)

    print("\n1. Demonstrating deterministic projection...")

    # ANY input projects to SAME pattern space
    test_input = np.random.randn(d_model)

    # Multiple projections of SAME input
    projections = []
    for _ in range(10):
        p = map.project(test_input)
        projections.append(p.copy())

    # Verify all same
    all_same = all(np.allclose(projections[i], projections[0]) for i in range(1, 10))
    print(f"   Same input, 10 projections: {'IDENTICAL' if all_same else 'DIFFERENT'}")

    print("\n2. Similarity without model inference...")

    # Create different inputs
    input_a = np.random.randn(d_model)
    input_b = np.random.randn(d_model)
    input_c = input_a * 0.9 + np.random.randn(d_model) * 0.1  # Similar to a

    # Get pattern projections
    pa = map.project(input_a)
    pb = map.project(input_b)
    pc = map.project(input_c)

    # Calculate similarities
    sim_ab = np.dot(pa, pb) / (np.linalg.norm(pa) * np.linalg.norm(pb))
    sim_ac = np.dot(pa, pc) / (np.linalg.norm(pa) * np.linalg.norm(pc))

    print(f"   A vs B (random): {sim_ab:.4f}")
    print(f"   A vs C (similar): {sim_ac:.4f} <-- should be higher!")

    print("\n3. Cluster analysis...")

    fake_knowledge = [np.random.randn(d_model) for _ in range(10)]

    navigator = KnowledgeNavigator(map)
    clusters = navigator.cluster(fake_knowledge)

    print(f"   Items grouped into {len(clusters)} clusters by pattern")

    print("\n" + "=" * 60)
    print("THE KEY INSIGHT")
    print("=" * 60)
    print("""
    What we have:
    - Universal pattern matrix (learned from model)
    - Projects ANY input → fixed-dim pattern space
    - No model inference needed for comparison!
    
    This is like:
    - GPS coordinates for knowledge
    - Universal embedding space
    - Hash table for semantic search
    
    Benefits:
    - Fast similarity search (O(1) projection vs O(n) decode)
    - Cluster analysis without model decode
    - Universal encoding for ANY input
    
    THE MAP IS THE SAME FOR EVERYTHING!
    """)


def demonstrate_gpt_embedding():
    """
    Это буквально как GPT embeddings работают!
    """
    print("\n" + "=" * 60)
    print("This is LITERALLY how GPT/transformers work!")
    print("=" * 60)
    print("""
    When GPT processes "king" vs "queen":
    - Both project through learned weight matrices
    - Land in similar region of embedding space
    - Because training taught them patterns!
    
    Our universal map does the SAME:
    - Input → pattern projection (learned during training)
    - Compare pattern vectors
    - Similar inputs → similar patterns
    
    The difference: our map is MUCH smaller:
    - GPT embedding: d_model x vocab_size floats
    - Our map: d_model x k floats (k << vocab)
    
    But the FUNCTION is the same:
    - Deterministic input → pattern mapping
    - Deterministic similarity calculation
    """)


if __name__ == "__main__":
    demonstrate_universal_mapping()
    demonstrate_gpt_embedding()
