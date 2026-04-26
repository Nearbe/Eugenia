#!/usr/bin/env python3
"""Radical fractal compressor implemented on Eugenia core math."""

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

from core.linear_algebra import CoreMatrix, euclidean_distance, subtract, to_matrix
from nucleus.correlation_compressor import _compose, _core_decompose

DEFAULT_RANDOM_SEED = 42


class RadicalCompressor:
    """Многоуровневый детерминированный low-rank компрессор."""

    def __init__(self, levels=4, base_k=4):
        self.levels = levels
        self.base_k = base_k
        self.components = []

    def compress(self, W):
        self.components = []
        original = to_matrix(W)
        residual = original.copy()
        first_error = 0.0

        for level in range(self.levels):
            rows, cols = residual.shape
            k = self.base_k * (2 ** (self.levels - level - 1))
            k = min(k, rows, cols)
            if k <= 0:
                break

            component = _core_decompose(residual, k)
            component["shape"] = residual.shape
            self.components.append(component)

            reconstructed = _compose(component)
            residual = subtract(residual, reconstructed)
            if level == 0:
                first_error = euclidean_distance(original, reconstructed) / (euclidean_distance(original, []) + 1.0e-10)

        return self.components, float(first_error)

    def decompress(self):
        if not self.components:
            return CoreMatrix()
        rows, cols = self.components[0]["shape"]
        result = CoreMatrix([[0.0 for _ in range(cols)] for _ in range(rows)])
        for component in self.components:
            restored = _compose(component)
            result = CoreMatrix(
                [[left + right for left, right in zip(row_a, row_b)] for row_a, row_b in zip(result, restored)]
            )
        return result


def test_radical():
    rng = random.Random(DEFAULT_RANDOM_SEED)
    matrix = CoreMatrix([[rng.gauss(0.0, 1.0) for _ in range(32)] for _ in range(32)])
    compressor = RadicalCompressor(levels=3, base_k=2)
    compressor.compress(matrix)
    print(compressor.decompress().shape)


def realistic_llm_weights():
    print("Realistic weights are represented through deterministic fractal components.")


def final_analysis():
    print("Compression is delegated to the repository core math layer.")


if __name__ == "__main__":
    test_radical()
    realistic_llm_weights()
    final_analysis()
