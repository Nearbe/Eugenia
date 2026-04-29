"""Lo Shu invariants from Universe/Math/00_low_shy.md."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .u_algebra import add, multiply, power

LO_SHU_SIZE: Final[int] = 3
LO_SHU_MATRIX: Final[tuple[tuple[int, ...], ...]] = (
    (4, 9, 2),
    (3, 5, 7),
    (8, 1, 6),
)
KEY_NUMBERS: Final[frozenset[int]] = frozenset({1, 2, 3, 4, 5, 9})
DUALITY: Final[int] = 2
IDENTITY_POINT: Final[int] = 1
TRIANGLE_DIMENSION: Final[int] = 3
BASIC_OPERATIONS: Final[int] = 4
CENTER: Final[int] = 5
FULLNESS_DIGIT: Final[int] = 9


@dataclass(frozen=True)
class LoShuInvariants:
    """Computed Lo Shu operational invariants."""

    active_principles: int
    context: int
    rope_scale: int
    rope_base: int
    layers: int
    gpu_layers: int
    cpu_layers: int
    load_threads: int
    inference_threads: int
    kv_bits: int


def rows() -> tuple[tuple[int, ...], ...]:
    """Return Lo Shu rows."""
    return LO_SHU_MATRIX


def columns() -> tuple[tuple[int, ...], ...]:
    """Return Lo Shu columns."""
    return tuple(tuple(row[index] for row in LO_SHU_MATRIX) for index in range(LO_SHU_SIZE))


def diagonals() -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return Lo Shu main diagonals."""
    forward = tuple(LO_SHU_MATRIX[index][index] for index in range(LO_SHU_SIZE))
    backward = tuple(LO_SHU_MATRIX[index][LO_SHU_SIZE - index - 1] for index in range(LO_SHU_SIZE))
    return forward, backward


def magic_sum() -> int:
    """Return the invariant row/column/diagonal sum."""
    return sum(LO_SHU_MATRIX[0])


def is_magic_square() -> bool:
    """Validate the Lo Shu magic-square axiom."""
    expected = magic_sum()
    lines = (*rows(), *columns(), *diagonals())
    return all(sum(line) == expected for line in lines)


def active_principles() -> int:
    """Return K, the sum of key numbers excluding duality."""
    return int(sum(number for number in KEY_NUMBERS if number != DUALITY))


def compute_invariants() -> LoShuInvariants:
    """Compute the operational Lo Shu invariants from the specification."""
    k_value = active_principles()
    context_power = int(multiply(BASIC_OPERATIONS, CENTER))
    context = int(power(DUALITY, context_power))
    rope_scale = int(multiply(k_value, FULLNESS_DIGIT))
    layers = int(multiply(k_value, BASIC_OPERATIONS))
    rope_base = int(multiply(rope_scale, FULLNESS_DIGIT / DUALITY))
    gpu_layers = int(multiply(TRIANGLE_DIMENSION, k_value))
    cpu_layers = k_value
    kv_bits = int(power(DUALITY, BASIC_OPERATIONS))
    return LoShuInvariants(
        active_principles=k_value,
        context=context,
        rope_scale=rope_scale,
        rope_base=rope_base,
        layers=layers,
        gpu_layers=gpu_layers,
        cpu_layers=cpu_layers,
        load_threads=IDENTITY_POINT,
        inference_threads=TRIANGLE_DIMENSION,
        kv_bits=kv_bits,
    )


def residual_sum(invariants: LoShuInvariants | None = None) -> int:
    """Return the closure residual from the layer distribution equation."""
    values = invariants if invariants is not None else compute_invariants()
    return int(add(values.gpu_layers, values.cpu_layers) - values.layers)
