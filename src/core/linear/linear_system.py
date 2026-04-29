"""Linear systems from Universe/Math/18_Системы_линейных_уравнений.md."""

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

from dataclasses import dataclass
from enum import StrEnum

from ..constants.constants import OMEGA
from ..algebra import add, branch, compress, is_omega
from .linear_algebra import CoreMatrix, CoreVector, mat_vec, to_matrix, to_vector


class LinearSystemState(StrEnum):
    """States of a U-linear system realization."""

    UNIQUE = "unique"
    COUPLED_STRUCTURE = "coupled_structure"
    IMPOSSIBLE_REALIZATION = "impossible_realization"


@dataclass(frozen=True)
class LinearSystemSolution:
    """Result of solving ``M·x = b``."""

    state: LinearSystemState
    values: CoreVector | None = None
    determinant: object = OMEGA


@dataclass(frozen=True)
class LinearSystem:
    """Interaction map ``M`` and target vector ``b``."""

    matrix: object
    target: object

    def solve(self) -> LinearSystemSolution:
        """Solve the system according to its interaction determinant."""
        return solve_linear_system(self.matrix, self.target)

    def evaluate(self, values: object) -> CoreVector:
        """Return ``M·values``."""
        return mat_vec(self.matrix, values)

    def branch(self) -> LinearSystem:
        """Return the branched system ``D(M)·x = D(b)``."""
        return LinearSystem(branch_matrix(self.matrix), branch_vector(self.target))

    def compress(self) -> LinearSystem:
        """Return the compressed system ``H(M)·x = H(b)``."""
        return LinearSystem(compress_matrix(self.matrix), compress_vector(self.target))


def _validate_square_system(matrix: CoreMatrix, target: CoreVector) -> None:
    """Validate dimensions of ``M·x=b``."""
    row_count, col_count = matrix.shape
    if row_count != col_count:
        raise ValueError(f"linear system requires a square matrix, got {matrix.shape}")
    if row_count != len(target):
        raise ValueError(
            "linear system target size mismatch: "
            f"matrix has {row_count} rows, target has {len(target)} values"
        )


def _finite_rows(matrix: object) -> list[list[float]]:
    """Return mutable finite matrix rows."""
    return [[float(value) for value in row] for row in to_matrix(matrix)]


def _finite_target(target: object) -> list[float]:
    """Return mutable finite target values."""
    return [float(value) for value in to_vector(target)]


def determinant(matrix: object) -> object:
    """Return determinant of a finite square matrix, or Ω for collapsed maps."""
    rows = _finite_rows(matrix)
    size = len(rows)
    if any(len(row) != size for row in rows):
        raise ValueError("determinant requires a square matrix")

    det_value = 1.0
    for col_index in range(size):
        pivot_index = next(
            (row_index for row_index in range(col_index, size) if rows[row_index][col_index] != OMEGA),
            None,
        )
        if pivot_index is None:
            return OMEGA
        if pivot_index != col_index:
            rows[col_index], rows[pivot_index] = rows[pivot_index], rows[col_index]
            det_value = -det_value

        pivot = rows[col_index][col_index]
        det_value *= pivot
        for row_index in range(col_index + 1, size):
            factor = rows[row_index][col_index] / pivot
            for inner_col in range(col_index, size):
                rows[row_index][inner_col] -= factor * rows[col_index][inner_col]
    return det_value


def solve_linear_system(matrix: object, target: object) -> LinearSystemSolution:
    """Solve ``M·x=b`` when ``det(M) != Ω``; otherwise report coupled structure."""
    rows = _finite_rows(matrix)
    target_values = _finite_target(target)
    core_matrix = CoreMatrix(rows)
    core_target = CoreVector(target_values)
    _validate_square_system(core_matrix, core_target)

    det_value = determinant(core_matrix)
    if is_omega(det_value):
        return LinearSystemSolution(LinearSystemState.COUPLED_STRUCTURE, determinant=det_value)

    solution = _gauss_jordan_solve(rows, target_values)
    if solution is None:
        return LinearSystemSolution(LinearSystemState.COUPLED_STRUCTURE, determinant=OMEGA)
    return LinearSystemSolution(LinearSystemState.UNIQUE, CoreVector(solution), det_value)


def _gauss_jordan_solve(rows: list[list[float]], target: list[float]) -> list[float] | None:
    """Solve finite square system by exact-pivot Gauss-Jordan elimination."""
    size = len(rows)
    augmented = [list(row) + [target[row_index]] for row_index, row in enumerate(rows)]

    for col_index in range(size):
        pivot_index = next(
            (row_index for row_index in range(col_index, size) if augmented[row_index][col_index] != OMEGA),
            None,
        )
        if pivot_index is None:
            return None
        if pivot_index != col_index:
            augmented[col_index], augmented[pivot_index] = augmented[pivot_index], augmented[col_index]

        pivot = augmented[col_index][col_index]
        for inner_col in range(col_index, size + 1):
            augmented[col_index][inner_col] /= pivot

        for row_index in range(size):
            if row_index == col_index:
                continue
            factor = augmented[row_index][col_index]
            for inner_col in range(col_index, size + 1):
                augmented[row_index][inner_col] -= factor * augmented[col_index][inner_col]

    return [augmented[row_index][size] for row_index in range(size)]


def branch_matrix(matrix: object) -> CoreMatrix:
    """Return ``D(M)`` by branching each interaction coefficient."""
    return CoreMatrix([[branch(value) for value in row] for row in to_matrix(matrix)])


def compress_matrix(matrix: object) -> CoreMatrix:
    """Return ``H(M)`` by compressing each interaction coefficient."""
    return CoreMatrix([[compress(value) for value in row] for row in to_matrix(matrix)])


def branch_vector(vector: object) -> CoreVector:
    """Return ``D(b⃗)``."""
    return CoreVector(branch(value) for value in to_vector(vector))


def compress_vector(vector: object) -> CoreVector:
    """Return ``H(b⃗)``."""
    return CoreVector(compress(value) for value in to_vector(vector))


def operator_matrix(branch_part: object, base_part: object) -> CoreMatrix:
    """Return matrix ``D(A) ⊕ B`` from the explicit-D system form."""
    branched = branch_matrix(branch_part)
    base = to_matrix(base_part)
    if branched.shape != base.shape:
        raise ValueError(f"operator matrices require equal shapes, got {branched.shape} and {base.shape}")
    return CoreMatrix(
        [[add(left, right) for left, right in zip(row_left, row_right)] for row_left, row_right in zip(branched, base)]
    )
