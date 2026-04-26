#!/usr/bin/env python3
"""Correlation-based compression on Eugenia core math, no external arrays."""

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
import math
import random
from struct import pack

from core.linear_algebra import (
    CoreMatrix,
    CoreVector,
    deterministic_matrix,
    matmul,
    max_abs,
    norm,
    quantize_int8,
    scalar_multiply,
    subtract,
    to_matrix,
)

DEFAULT_RANDOM_SEED = 42
DEFAULT_RANDOM_SCALE = 0.01
DEFAULT_SVD_K = 32
FLOAT_BYTES = 4
F16_BYTES = 2


def _matrix_size(matrix) -> tuple[int, int]:
    rows = to_matrix(matrix)
    return rows.shape


def _zeros_like(matrix) -> CoreMatrix:
    rows, cols = _matrix_size(matrix)
    return CoreMatrix([[0.0 for _ in range(cols)] for _ in range(rows)])


def _column(matrix: CoreMatrix, index: int) -> CoreVector:
    return CoreVector(row[index] for row in matrix if index < len(row))


def _row(matrix: CoreMatrix, index: int) -> CoreVector:
    if not matrix:
        return CoreVector()
    return CoreVector(matrix[index % len(matrix)])


def _normalized(values) -> CoreVector:
    vector = CoreVector(values)
    magnitude = norm(vector)
    if magnitude == 0.0:
        return CoreVector(0.0 for _ in vector)
    return CoreVector(value / magnitude for value in vector)


def _core_decompose(matrix, k: int) -> dict:
    data = to_matrix(matrix)
    rows, cols = data.shape
    rank = max(0, min(k, rows, cols))
    left: list[list[float]] = [[0.0 for _ in range(rank)] for _ in range(rows)]
    singular: list[float] = []
    right: list[list[float]] = []

    for comp in range(rank):
        col = _normalized(_column(data, comp))
        row = _normalized(_row(data, comp))
        singular_value = max(norm(_column(data, comp)), norm(_row(data, comp)))
        singular.append(float(singular_value))
        for row_index in range(rows):
            left[row_index][comp] = col[row_index] if row_index < len(col) else 0.0
        right.append(list(row[:cols]))

    return {
        "U": CoreMatrix(left),
        "S": CoreVector(singular),
        "Vt": CoreMatrix(right),
        "k": rank,
        "shape": (rows, cols),
    }


def _compose(components: dict) -> CoreMatrix:
    left = to_matrix(components["U"])
    singular = CoreVector(components["S"])
    right = to_matrix(components["Vt"])
    scaled_left = CoreMatrix(
        [[value * singular[col] for col, value in enumerate(row)] for row in left]
    )
    return matmul(scaled_left, right)


class CorrelationCompressor:
    """Компрессор на основе корреляционных структур и core-операторов."""

    def __init__(self):
        self.delta = None
        self.correlation_eigen = None
        self.graph = None

    def compress_delta(self, W, init_type="random"):
        matrix = to_matrix(W)
        rows, cols = matrix.shape
        if init_type == "zeros":
            W_init = _zeros_like(matrix)
        else:
            scale = DEFAULT_RANDOM_SCALE
            if init_type == "xavier" and rows + cols > 0:
                scale = math.sqrt(2.0 / (rows + cols))
            W_init = deterministic_matrix(f"{init_type}:{rows}:{cols}", rows, cols, scale)

        delta = subtract(matrix, W_init)
        self.delta = delta
        return delta, W_init

    def compress_correlation_svd(self, W, k=None):
        matrix = to_matrix(W)
        rows, cols = matrix.shape
        rank = min(k if k is not None else DEFAULT_SVD_K, rows, cols)
        self.correlation_eigen = _core_decompose(matrix, rank)
        return self.correlation_eigen

    def decompress_correlation_svd(self):
        if self.correlation_eigen is None:
            return CoreMatrix()
        return _compose(self.correlation_eigen)

    def compress_graph(self, W, threshold=0.5):
        matrix = to_matrix(W)
        rows, cols = matrix.shape
        peak = max_abs(matrix)
        cutoff = float(threshold) * peak
        entries: list[tuple[int, int, float]] = []
        for row_index, row in enumerate(matrix):
            for col_index, value in enumerate(row):
                if abs(value) > cutoff:
                    entries.append((row_index, col_index, value))

        data = bytearray()
        data += pack("<ii", rows, cols)
        data += pack("<i", len(entries))
        for row_index, col_index, _ in entries:
            data += pack("<II", row_index, col_index)
        scale = max((abs(value) for _, _, value in entries), default=0.0)
        data += pack("<f", scale)
        data += quantize_int8([value for _, _, value in entries], scale)
        total = rows * cols if rows and cols else 1
        return bytes(data), len(entries) / total

    def compress_hessian_pattern(self, W):
        matrix = to_matrix(W)
        return matmul(matrix, matrix.T)


def test_methods():
    rng = random.Random(DEFAULT_RANDOM_SEED)
    W = CoreMatrix([[rng.gauss(0.0, 1.0) for _ in range(32)] for _ in range(32)])
    compressor = CorrelationCompressor()
    compressor.compress_delta(W, "xavier")
    compressor.compress_correlation_svd(W, k=8)
    compressor.compress_graph(W, threshold=0.3)


def correlation_idea():
    print("Correlation structure is stored as deterministic core patterns.")


if __name__ == "__main__":
    test_methods()
    correlation_idea()
