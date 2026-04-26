#!/usr/bin/env python3
"""Deterministic semantic engine on Eugenia core math."""

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
from dataclasses import dataclass
from typing import List, Tuple

from core.linear_algebra import (
    CoreMatrix,
    CoreVector,
    dot,
    mat_vec,
    mean,
    scalar_multiply,
    to_matrix,
    to_vector,
)
from nucleus.cross_layer_compressor import compress_layer, cross_layer_pattern


@dataclass
class DeterministicPattern:
    """Детерминированный паттерн."""

    vector: CoreMatrix
    singular: CoreVector
    phase: float


class DeterministicKnowledgeCore:
    """Ядро детерминированных знаний."""

    def __init__(self, d_model: int, k: int = 32):
        self.d_model = d_model
        self.k = k
        self.patterns: List[DeterministicPattern] = []
        self.relationships: list[CoreMatrix] | None = None
        self._initialized = False

    def learn(self, weight_matrices: dict) -> "DeterministicKnowledgeCore":
        all_patterns: list[DeterministicPattern] = []
        all_rels: list[CoreMatrix] = []
        for _, matrix in weight_matrices.items():
            layer = compress_layer(matrix, self.k)
            vector = layer["U"]
            singular = layer["S"]
            first_col = [row[0] for row in vector if row]
            phase = mean(first_col)
            pattern = DeterministicPattern(vector=vector, singular=singular, phase=phase)
            all_patterns.append(pattern)
            if len(all_patterns) > 1:
                all_rels.append(self._compute_relationship(all_patterns[-2], pattern))
        self.patterns = all_patterns
        self.relationships = all_rels or None
        self._initialized = True
        return self

    def _compute_relationship(self, p1: DeterministicPattern, p2: DeterministicPattern) -> CoreMatrix:
        return cross_layer_pattern({"U": p1.vector, "S": p1.singular}, {"U": p2.vector, "S": p2.singular}, self.k)

    def forward(self, x):
        if not self._initialized:
            raise ValueError("Core not initialized. Call learn() first.")
        current = CoreVector(to_vector(x))
        for pattern in self.patterns:
            projected = mat_vec(pattern.vector.T, current)
            scaled = CoreVector(value * pattern.singular[index] for index, value in enumerate(projected))
            current = mat_vec(pattern.vector, scaled)
        return current

    def apply_deterministic(self, x, layer_idx: int):
        if layer_idx >= len(self.patterns):
            return x
        pattern = self.patterns[layer_idx]
        projected = mat_vec(pattern.vector.T, x)
        scaled = CoreVector(value * pattern.singular[index] for index, value in enumerate(projected))
        return mat_vec(pattern.vector, scaled)

    def get_deterministic_signature(self) -> str:
        if not self.patterns:
            return "NOT_INITIALIZED"
        total_singular = sum(sum(pattern.singular) for pattern in self.patterns)
        phase = self.patterns[0].phase if self.patterns else 0.0
        return f"d{self.d_model}_k{self.k}_sig{total_singular:.6f}_ph{phase:.4f}"

    def verify_determinism(self, x, n_tests: int = 10) -> Tuple[bool, float]:
        first = self.forward(x)
        max_diff = 0.0
        for _ in range(max(n_tests - 1, 0)):
            current = self.forward(x)
            diffs = [abs(a - b) for a, b in zip(first, current)]
            max_diff = max(max_diff, max(diffs) if diffs else 0.0)
        return max_diff < 1.0e-10, max_diff


class DeterministicFunction:
    """Детерминированная функция модели."""

    def __init__(self, k: int = 32):
        self.k = k
        self.core = DeterministicKnowledgeCore(k=k, d_model=4096)
        self.signature = None

    def fit(self, weights: dict) -> "DeterministicFunction":
        self.core = DeterministicKnowledgeCore(d_model=4096, k=self.k)
        self.core.learn(weights)
        self.signature = self.core.get_deterministic_signature()
        return self

    def __call__(self, x):
        return self.core.forward(x)

    def apply(self, x, layer: int):
        return self.core.apply_deterministic(x, layer)

    def verify(self, test_input, n: int = 100) -> dict:
        is_det, max_diff = self.core.verify_determinism(test_input, n)
        return {"is_deterministic": is_det, "max_variation": max_diff, "signature": self.signature}


def demonstrate_determinism():
    weights = {"q": CoreMatrix([[0.1 for _ in range(16)] for _ in range(16)])}
    dfa = DeterministicFunction(k=4).fit(weights)
    print(dfa.verify(CoreVector([1.0] * 16), n=5))


def test_compression_ratio():
    print("Compression ratio depends on selected core rank k.")


if __name__ == "__main__":
    demonstrate_determinism()
    test_compression_ratio()
