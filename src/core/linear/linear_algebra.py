"""Core vector and matrix helpers without external math dependencies.

The formulas follow Universe/Essentials/Vectorization.md:
ΔV = V_B - V_A, Euclidean norm, Euclidean distance and cosine similarity.
"""

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
from __future__ import annotations

import random
from collections.abc import Iterable, Sequence
from typing import TypeAlias, Any

from .mat_norm import mat_norm
from .vec_norm import vec_norm

Number: TypeAlias = int | float
F32_BYTES = 4
INT8_MIN = -128
INT8_MAX = 127


def _validate_rectangular_rows(rows: Sequence[Sequence[object]]) -> int:
    """Return the common column count or raise on ragged matrices."""
    if not rows:
        return 0
    col_count = len(rows[0])
    for row_index, row in enumerate(rows):
        if len(row) != col_count:
            raise ValueError(
                "matrix rows must all have the same length "
                f"(row 0 has {col_count}, row {row_index} has {len(row)})"
            )
    return col_count


class CoreVector:
    """List-backed vector used by core/nucleus code."""

    dtype = float

    def __init__(self, values=()):
        self._data = [float(v) for v in values]

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return CoreVector(self._data[item])
        return self._data[item]

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return f"CoreVector({self._data})"

    @property
    def shape(self) -> tuple[int]:
        return (len(self),)

    @property
    def size(self) -> int:
        return len(self)

    @property
    def nbytes(self) -> int:
        return len(self) * F32_BYTES

    def _compare(self, other, predicate) -> "CoreVector":
        other_values = to_vector(other)
        if not other_values:
            return CoreVector()
        if len(other_values) == 1 and len(self) != 1:
            pivot = other_values[0]
            return CoreVector(
                1.0 if predicate(value, pivot) else 0.0 for value in self._data
            )
        return CoreVector(
            1.0 if predicate(left, right) else 0.0
            for left, right in zip(self._data, other_values)
        )

    def __ge__(self, other) -> Any:
        return self._compare(other, lambda left, right: left >= right)

    def __gt__(self, other) -> Any:
        return self._compare(other, lambda left, right: left > right)

    def __le__(self, other) -> Any:
        return self._compare(other, lambda left, right: left <= right)

    def __lt__(self, other) -> Any:
        return self._compare(other, lambda left, right: left < right)

    def __sub__(self, other) -> "CoreVector":
        other_values = to_vector(other)
        if len(other_values) == 1:
            pivot = float(other_values[0])
            return CoreVector(v - pivot for v in self._data)
        return CoreVector(float(l) - float(r) for l, r in zip(self._data, other_values))

    def tolist(self) -> list[float]:
        return list(self._data)

    def copy(self) -> "CoreVector":
        return CoreVector(self._data)

    def astype(self, _dtype) -> "CoreVector":
        return CoreVector(float(value) for value in self._data)

    def flatten(self) -> "CoreVector":
        """Return self (already 1D)."""
        return self.copy()

    def cpu(self) -> "CoreVector":
        """Compatibility method - returns self since we're not using GPU."""
        return self

    def numpy(self) -> list:
        """Compatibility method - returns the underlying list structure."""
        return self.tolist()

    def __eq__(self, other):
        if hasattr(other, "tolist"):
            return self.tolist() == other.tolist()
        return self.tolist() == other


class CoreMatrix:
    """List-backed rectangular matrix used by core/nucleus code."""

    dtype = float

    def __init__(self, values=()):
        rows = []
        for row in values:
            if hasattr(row, "tolist"):
                row = row.tolist()
            if isinstance(row, Iterable) and not isinstance(row, (str, bytes)):
                rows.append([float(v) for v in row])
            else:
                rows.append([float(row)])
        _validate_rectangular_rows(rows)
        self._data = rows

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        if not isinstance(item, tuple):
            result = self._data[item]
            if isinstance(item, slice):
                return CoreMatrix(result)
            return result

        row_selector, col_selector = item
        selected_rows = self._data[row_selector]
        row_is_scalar = isinstance(row_selector, int)
        col_is_scalar = isinstance(col_selector, int)

        if isinstance(row_selector, slice):
            rows = selected_rows
        else:
            rows = [selected_rows]

        if col_is_scalar:
            column = CoreVector(row[col_selector] for row in rows)
            return column[0] if row_is_scalar else column

        sliced_rows = CoreMatrix([row[col_selector] for row in rows])
        return sliced_rows[0] if row_is_scalar else sliced_rows

    def __iter__(self):
        return iter(self._data)

    @property
    def shape(self) -> tuple[int, int]:
        row_count = len(self._data)
        col_count = len(self._data[0]) if row_count else 0
        return row_count, col_count

    @property
    def size(self) -> int:
        rows, cols = self.shape
        return rows * cols

    @property
    def nbytes(self) -> int:
        return self.size * F32_BYTES

    @property
    def T(self) -> "CoreMatrix":
        return transpose(self)

    def tolist(self) -> list[list[float]]:
        return [list(row) for row in self._data]

    def copy(self) -> "CoreMatrix":
        return CoreMatrix([list(row) for row in self._data])

    def astype(self, _dtype) -> "CoreMatrix":
        return CoreMatrix([[float(value) for value in row] for row in self._data])

    def flatten(self) -> CoreVector:
        """Flatten matrix to a 1D vector."""
        return CoreVector(value for row in self._data for value in row)

    def cpu(self) -> "CoreMatrix":
        """Compatibility method - returns self since we're not using GPU."""
        return self

    def numpy(self) -> list:
        """Compatibility method - returns the underlying list structure."""
        return self.tolist()

    def __eq__(self, other):
        if hasattr(other, "tolist"):
            return self.tolist() == other.tolist()
        return self.tolist() == other


def is_scalar(value) -> bool:

    return isinstance(value, (int, float)) and not isinstance(value, bool)


def to_vector(values) -> CoreVector:
    """Flatten scalar/list/array-like values into CoreVector."""
    if values is None:
        return CoreVector()
    if is_scalar(values):
        return CoreVector([float(values)])
    if isinstance(values, str):
        return CoreVector(float(ord(c)) for c in values)
    if isinstance(values, bytes):
        return CoreVector(float(b) for b in values)
    if hasattr(values, "tolist"):
        values = values.tolist()

    result: list[float] = []
    for value in values:
        if hasattr(value, "tolist"):
            value = value.tolist()
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            result.extend(to_vector(value))
        else:
            result.append(float(value))
    return CoreVector(result)


def to_matrix(values) -> CoreMatrix:
    """Convert scalar/vector/matrix-like values into a rectangular CoreMatrix."""
    if values is None:
        return CoreMatrix()
    if hasattr(values, "tolist"):
        values = values.tolist()
    if is_scalar(values):
        return CoreMatrix([[float(values)]])

    rows: list[list[float]] = []
    for row in values:
        if hasattr(row, "tolist"):
            row = row.tolist()
        if isinstance(row, Iterable) and not isinstance(row, (str, bytes)):
            rows.append([float(value) for value in row])
        else:
            rows.append([float(row)])
    _validate_rectangular_rows(rows)
    return CoreMatrix(rows)


def shape(values) -> tuple[int, ...]:
    if hasattr(values, "shape"):
        return tuple(int(dim) for dim in values.shape)
    if is_scalar(values) or values is None:
        return ()
    data = values.tolist() if hasattr(values, "tolist") else values
    rows = list(data)
    if not rows:
        return (0,)
    first = rows[0]
    if isinstance(first, Iterable) and not isinstance(first, (str, bytes)):
        matrix_rows: list[list[object]] = []
        for row in rows:
            if hasattr(row, "tolist"):
                row = row.tolist()
            if not isinstance(row, Iterable) or isinstance(row, (str, bytes)):
                raise ValueError("matrix rows must be iterable")
            matrix_rows.append(list(row))
        return len(matrix_rows), _validate_rectangular_rows(matrix_rows)
    return (len(rows),)


def vector_deviation(vector_a, vector_b) -> CoreVector:
    values_a = to_vector(vector_a)
    values_b = to_vector(vector_b)
    return CoreVector(right - left for left, right in zip(values_a, values_b))


def dot(vector_a, vector_b) -> float:
    values_a = to_vector(vector_a)
    values_b = to_vector(vector_b)
    if len(values_a) != len(values_b):
        raise ValueError(
            f"dot product requires equal vector lengths, got {len(values_a)} and {len(values_b)}"
        )
    return sum(left * right for left, right in zip(values_a, values_b))


def norm(vector) -> float:
    return vec_norm(to_vector(vector))


def mean(values) -> float:
    vector = to_vector(values)
    return sum(vector) / len(vector) if vector else 0.0


def variance(values) -> float:
    vector = to_vector(values)
    if not vector:
        return 0.0
    center = mean(vector)
    return sum((value - center) ** 2 for value in vector) / len(vector)


def std(values) -> float:
    return variance(values) ** 0.5


def euclidean_distance(vector_a, vector_b) -> float:
    return norm(vector_deviation(vector_a, vector_b))


def cosine_similarity(vector_a, vector_b) -> float:
    denominator = norm(vector_a) * norm(vector_b)
    if denominator == 0.0:
        return 0.0
    return dot(vector_a, vector_b) / denominator


def linspace(start: Number, stop: Number, count: int) -> CoreVector:
    if count <= 0:
        return CoreVector()
    if count == 1:
        return CoreVector([float(start)])
    step = (float(stop) - float(start)) / float(count - 1)
    return CoreVector(float(start) + step * index for index in range(count))


def diff(values) -> CoreVector:
    vector = to_vector(values)
    return CoreVector(
        vector[index + 1] - vector[index] for index in range(len(vector) - 1)
    )


def matrix_shape(matrix) -> tuple[int, int]:
    return to_matrix(matrix).shape


def zeros(rows: int, cols: int | None = None) -> CoreVector | CoreMatrix:
    if cols is None:
        return CoreVector(0.0 for _ in range(max(rows, 0)))
    return CoreMatrix([[0.0 for _ in range(max(cols, 0))] for _ in range(max(rows, 0))])


def ones(rows: int, cols: int | None = None) -> CoreVector | CoreMatrix:
    if cols is None:
        return CoreVector(1.0 for _ in range(max(rows, 0)))
    return CoreMatrix([[1.0 for _ in range(max(cols, 0))] for _ in range(max(rows, 0))])


def identity(size: int) -> CoreMatrix:
    return CoreMatrix(
        [[1.0 if row == col else 0.0 for col in range(size)] for row in range(size)]
    )


def transpose(matrix) -> CoreMatrix:
    rows = to_matrix(matrix)
    return CoreMatrix([list(col) for col in zip(*rows)]) if rows else CoreMatrix()


def mat_vec(matrix, vector) -> CoreVector:
    rows = to_matrix(matrix)
    vec = to_vector(vector)
    row_count, col_count = rows.shape
    if row_count and col_count != len(vec):
        raise ValueError(
            f"matrix-vector shape mismatch: matrix has {col_count} columns, vector has {len(vec)}"
        )
    return CoreVector(dot(row, vec) for row in rows)


def matmul(matrix_a, matrix_b) -> CoreMatrix:
    left = to_matrix(matrix_a)
    right = to_matrix(matrix_b)
    left_rows, left_cols = left.shape
    right_rows, _right_cols = right.shape
    if left_rows and right_rows and left_cols != right_rows:
        raise ValueError(
            f"matrix multiplication shape mismatch: left is {left.shape}, right is {right.shape}"
        )
    matrix_b_t = transpose(right)
    return CoreMatrix([[dot(row, col) for col in matrix_b_t] for row in left])


def outer(vector_a, vector_b) -> CoreMatrix:
    values_a = to_vector(vector_a)
    values_b = to_vector(vector_b)
    return CoreMatrix([[left * right for right in values_b] for left in values_a])


def scalar_multiply(values, factor: Number):
    factor_value = float(factor)
    if len(shape(values)) == 2:
        return CoreMatrix(
            [
                [float(value) * factor_value for value in row]
                for row in to_matrix(values)
            ]
        )
    return CoreVector(float(value) * factor_value for value in to_vector(values))


def add(values_a, values_b):
    if len(shape(values_a)) == 2 or len(shape(values_b)) == 2:
        return CoreMatrix(
            [
                [float(l) + float(r) for l, r in zip(row_a, row_b)]
                for row_a, row_b in zip(to_matrix(values_a), to_matrix(values_b))
            ]
        )
    return CoreVector(
        float(l) + float(r) for l, r in zip(to_vector(values_a), to_vector(values_b))
    )


def subtract(values_a, values_b):
    if len(shape(values_a)) == 2 or len(shape(values_b)) == 2:
        return CoreMatrix(
            [
                [float(l) - float(r) for l, r in zip(row_a, row_b)]
                for row_a, row_b in zip(to_matrix(values_a), to_matrix(values_b))
            ]
        )
    return CoreVector(
        float(l) - float(r) for l, r in zip(to_vector(values_a), to_vector(values_b))
    )


def max_abs(values) -> float:
    vector = to_vector(values)
    return max((abs(value) for value in vector), default=0.0)


def deterministic_vector(seed_text: str, size: int) -> CoreVector:
    rng = random.Random(seed_text)
    return CoreVector(rng.random() for _ in range(size))


def deterministic_matrix(
    seed_text: str, rows: int, cols: int, scale: float = 1.0
) -> CoreMatrix:
    rng = random.Random(seed_text)
    return CoreMatrix(
        [[rng.gauss(0.0, 1.0) * scale for _ in range(cols)] for _ in range(rows)]
    )


def sign(value: Number) -> int:
    value_f = float(value)
    if value_f > 0.0:
        return 1
    if value_f < 0.0:
        return -1
    return 0


def matrix_norm(matrix) -> float:
    return mat_norm(to_matrix(matrix))


def quantize_int8(values, scale: float | None = None) -> bytes:
    vector = to_vector(values)
    actual_scale = scale if scale not in (None, 0.0) else max_abs(vector)
    if actual_scale == 0.0:
        return bytes([0 for _ in vector])
    encoded = bytearray()
    for value in vector:
        quantized = round(value / actual_scale * INT8_MAX)
        quantized = max(INT8_MIN, min(INT8_MAX, quantized))
        encoded.append(quantized & 0xFF)
    return bytes(encoded)
