"""Lo Shu as the first address grid of the U-system.

The grid is not a numeric curiosity. It fixes the first directional
addresses for digits and operations before any hash/random seed exists.
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

from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Iterable

from core.constants import D_ID, OMEGA

LO_SHU_SIZE: Final[int] = 3
LO_SHU_CENTER_VALUE: Final[int] = 5
LO_SHU_MAGIC_SUM: Final[int] = 15
LO_SHU_DECIMAL_CYCLE: Final[int] = 10
LO_SHU_MAX_DIGIT: Final[int] = 9


class Direction(StrEnum):
    """Fixed the compass directions of the Lo Shu grid."""

    NORTH_WEST = "north_west"
    NORTH = "north"
    NORTH_EAST = "north_east"
    WEST = "west"
    CENTER = "center"
    EAST = "east"
    SOUTH_WEST = "south_west"
    SOUTH = "south"
    SOUTH_EAST = "south_east"


class LoShuOperation(StrEnum):
    """Operations addressed directly by the Lo Shu grid."""

    POTENTIAL = "Ω"
    IDENTITY = "Id"
    BRANCH = "D"
    COMPRESS = "H"
    LOG_DEPTH = "L"
    FULLNESS = "Π"
    ADD = "⊕"
    MULTIPLY = "⊗"
    DIVIDE = ":"
    CYCLE = "↻"


@dataclass(frozen=True)
class LoShuPosition:
    """A fixed position in the Lo Shu compass grid."""

    direction: Direction
    digit: int
    row: int
    column: int

    @property
    def phase(self) -> float:
        """Decimal-cycle phase associated with this position."""
        return self.digit / LO_SHU_DECIMAL_CYCLE

    @property
    def binary_history(self) -> tuple[int, ...]:
        """Four-bit residue address of the digit."""
        return tuple(int(bit) for bit in f"{self.digit:04b}")


@dataclass(frozen=True)
class LoShuAddress:
    """Primary address before any solenoid history is unfolded."""

    position: LoShuPosition
    operation: LoShuOperation | None = None

    @property
    def digit(self) -> int:
        return self.position.digit

    @property
    def phase(self) -> float:
        if self.operation is None:
            return self.position.phase
        return (self.position.digit + operation_digit(self.operation)) / LO_SHU_DECIMAL_CYCLE

    @property
    def history(self) -> tuple[int, ...]:
        if self.operation is None:
            return self.position.binary_history
        return (
            self.position.binary_history
            + digit_position(operation_digit(self.operation)).binary_history
        )


GRID: Final[tuple[tuple[int, int, int], ...]] = (
    (4, 9, 2),
    (3, 5, 7),
    (8, 1, 6),
)

POSITIONS: Final[tuple[LoShuPosition, ...]] = (
    LoShuPosition(Direction.NORTH_WEST, 4, 0, 0),
    LoShuPosition(Direction.NORTH, LO_SHU_MAX_DIGIT, 0, 1),
    LoShuPosition(Direction.NORTH_EAST, 2, 0, 2),
    LoShuPosition(Direction.WEST, LO_SHU_SIZE, 1, 0),
    LoShuPosition(Direction.CENTER, LO_SHU_CENTER_VALUE, 1, 1),
    LoShuPosition(Direction.EAST, 7, 1, 2),
    LoShuPosition(Direction.SOUTH_WEST, 8, 2, 0),
    LoShuPosition(Direction.SOUTH, 1, 2, 1),
    LoShuPosition(Direction.SOUTH_EAST, 6, 2, 2),
)

POSITION_BY_DIGIT: Final[dict[int, LoShuPosition]] = {
    position.digit: position for position in POSITIONS
}
POSITION_BY_DIRECTION: Final[dict[Direction, LoShuPosition]] = {
    position.direction: position for position in POSITIONS
}

OPERATION_DIGITS: Final[dict[LoShuOperation, int]] = {
    LoShuOperation.POTENTIAL: 0,
    LoShuOperation.IDENTITY: LO_SHU_CENTER_VALUE,
    LoShuOperation.BRANCH: LO_SHU_MAX_DIGIT,
    LoShuOperation.COMPRESS: 1,
    LoShuOperation.LOG_DEPTH: LO_SHU_SIZE,
    LoShuOperation.FULLNESS: LO_SHU_MAX_DIGIT,
    LoShuOperation.ADD: 4,
    LoShuOperation.MULTIPLY: 6,
    LoShuOperation.DIVIDE: 8,
    LoShuOperation.CYCLE: 2,
}


def rows() -> tuple[tuple[int, ...], ...]:
    return GRID


def columns() -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(row[column] for row in GRID) for column in range(LO_SHU_SIZE))


def diagonals() -> tuple[tuple[int, ...], tuple[int, ...]]:
    return (
        tuple(GRID[index][index] for index in range(LO_SHU_SIZE)),
        tuple(GRID[index][LO_SHU_SIZE - index - 1] for index in range(LO_SHU_SIZE)),
    )


def equations() -> tuple[tuple[int, ...], ...]:
    return rows() + columns() + diagonals()


def equation_sums() -> tuple[int, ...]:
    return tuple(sum(equation) for equation in equations())


def digit_position(digit: int) -> LoShuPosition:
    if digit == OMEGA:
        return LoShuPosition(Direction.CENTER, 0, 1, 1)
    if digit not in POSITION_BY_DIGIT:
        raise ValueError(f"Lo Shu digit must be from 1 to {LO_SHU_MAX_DIGIT}, got {digit!r}")
    return POSITION_BY_DIGIT[digit]


def direction_position(direction: Direction | str) -> LoShuPosition:
    key = Direction(direction)
    return POSITION_BY_DIRECTION[key]


def operation_digit(operation: LoShuOperation | str) -> int:
    key = LoShuOperation(operation)
    return OPERATION_DIGITS[key]


def digit_address(digit: int) -> LoShuAddress:
    return LoShuAddress(position=digit_position(digit))


def operation_address(operation: LoShuOperation | str) -> LoShuAddress:
    digit = operation_digit(operation)
    position = digit_position(LO_SHU_CENTER_VALUE if digit == OMEGA else digit)
    return LoShuAddress(position=position, operation=LoShuOperation(operation))


def address_path(addresses: Iterable[LoShuAddress]) -> tuple[int, ...]:
    path: list[int] = []
    for address in addresses:
        path.extend(address.history)
    return tuple(path)


def context_number() -> float:
    return 2 ** (4 * LO_SHU_CENTER_VALUE)


def scale_number() -> int:
    return LO_SHU_MAGIC_SUM * (LO_SHU_DECIMAL_CYCLE + LO_SHU_SIZE) + LO_SHU_SIZE


def base_number() -> int:
    return LO_SHU_MAX_DIGIT * 99


def layer_count() -> int:
    return 4 * 22


def cpu_gpu_balance() -> tuple[int, int]:
    cpu = 22
    gpu = cpu * LO_SHU_SIZE
    return cpu, gpu


def value(direction: Direction | str) -> int:
    """Return the digit at a given direction."""
    pos = direction_position(direction)
    return pos.digit


def magic_sum() -> int:
    """Return the magic sum of the Lo Shu square."""
    return LO_SHU_MAGIC_SUM


def is_magic_square() -> bool:
    """Check if the Lo Shu grid is a valid magic square."""
    sums = equation_sums()
    return all(s == LO_SHU_MAGIC_SUM for s in sums)


def key_numbers() -> tuple[int, ...]:
    """Return the key numbers used in the Lo Shu system."""
    return tuple(
        sorted(
            set(
                digit
                for row in GRID
                for digit in row
                if digit <= LO_SHU_CENTER_VALUE or digit == LO_SHU_MAX_DIGIT
            )
        )
    )


def corners() -> tuple[int, int, int, int]:
    """Return the four corner digits of the Lo Shu grid."""
    return GRID[0][0], GRID[0][2], GRID[2][0], GRID[2][2]


def active_principles() -> int:
    """Return the number of active principles (CPU layers)."""
    cpu, _ = cpu_gpu_balance()
    return cpu


def compute_equations():
    """Return an object containing computed equation properties."""

    class EquationResult:
        def __init__(self):
            self.context = context_number()
            self.rope_scale = scale_number()
            self.rope_base = base_number()
            self.layers = layer_count()
            cpu, gpu = cpu_gpu_balance()
            self.gpu_layers = gpu
            self.cpu_layers = cpu
            self.load_threads = 1
            self.inference_threads = LO_SHU_SIZE
            self.kv_bits = 16

    return EquationResult()


def residual_sum(equations) -> int:
    """Calculate the residual sum from equations (should be 0 for magic square)."""
    return sum(s - LO_SHU_MAGIC_SUM for s in equation_sums())


def position(direction: Direction | str):
    """Alias for direction_position."""
    return direction_position(direction)


__all__ = [
    "Direction",
    "GRID",
    "LO_SHU_CENTER_VALUE",
    "LO_SHU_DECIMAL_CYCLE",
    "LO_SHU_MAGIC_SUM",
    "LoShuAddress",
    "LoShuOperation",
    "LoShuPosition",
    "POSITION_BY_DIGIT",
    "POSITION_BY_DIRECTION",
    "address_path",
    "base_number",
    "columns",
    "context_number",
    "cpu_gpu_balance",
    "diagonals",
    "digit_address",
    "digit_position",
    "direction_position",
    "equation_sums",
    "equations",
    "layer_count",
    "operation_address",
    "operation_digit",
    "rows",
    "scale_number",
]
