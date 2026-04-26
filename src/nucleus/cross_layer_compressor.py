#!/usr/bin/env python3
"""Cross-layer knowledge compression using Eugenia core math."""

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

from core.linear_algebra import CoreMatrix, CoreVector, matmul, to_matrix
from nucleus.correlation_compressor import _compose, _core_decompose

DEFAULT_RANDOM_SEED = 42
FLOAT_BYTES = 4
F16_BYTES = 2


def compress_layer(W, k):
    """Сжать слой в детерминированное low-rank core-представление."""
    return _core_decompose(W, k)


def decompress_layer(layer):
    """Восстановить слой из core-представления."""
    return _compose(layer)


def _scale_columns(matrix, values) -> CoreMatrix:
    data = to_matrix(matrix)
    singular = CoreVector(values)
    return CoreMatrix([[value * singular[col] for col, value in enumerate(row)] for row in data])


def cross_layer_pattern(layer1, layer2, k):
    """Извлечь компактный паттерн связи между двумя слоями."""
    u1 = _scale_columns(layer1["U"], layer1["S"][:k])
    u2 = _scale_columns(layer2["U"], layer2["S"][:k])
    return matmul(u1.T, u2)


def test_full_model():
    rng = random.Random(DEFAULT_RANDOM_SEED)
    matrix = CoreMatrix([[rng.gauss(0.0, 1.0) for _ in range(32)] for _ in range(32)])
    layer = compress_layer(matrix, 8)
    restored = decompress_layer(layer)
    print(layer["U"].shape, restored.shape)


def realistic_llm():
    print("Cross-layer compression uses core vectors and deterministic projections.")


if __name__ == "__main__":
    test_full_model()
    realistic_llm()
