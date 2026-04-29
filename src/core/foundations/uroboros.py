"""Great Uroboros cycle from Universe/Math/The_Great_Cycle_Of_Uroboros.md."""

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
from typing import Final

from .constants import OMEGA
from .infinity import PI

CYCLE_START: Final[int] = 0
CYCLE_END: Final[int] = 9
CYCLE_LENGTH: Final[int] = 10
CENTER_DIGIT: Final[int] = 5
NEGATIVE_BOUND: Final[float] = -1.0
CENTER_VALUE: Final[float] = 0.0
POSITIVE_BOUND: Final[float] = 1.0


def normalize_digit(digit: int) -> int:
    """Return digit projected to the closed 0→...→9→0 cycle."""
    return int(digit) % CYCLE_LENGTH


def cycle_step(digit: int, *, steps: int = 1) -> int:
    """Move along the Uroboros digit cycle."""
    return normalize_digit(int(digit) + int(steps))


def state_range_value(digit: int) -> float:
    """Map digit state to the continuous range [-1, 1] with center 5 = Id."""
    normalized = normalize_digit(digit)
    if normalized <= CENTER_DIGIT:
        return NEGATIVE_BOUND + normalized / CENTER_DIGIT
    return (normalized - CENTER_DIGIT) / (CYCLE_END - CENTER_DIGIT)


def state_kind(digit: int) -> str:
    """Return semantic state kind: Ω, Id, Π or transition."""
    normalized = normalize_digit(digit)
    if normalized == CYCLE_START:
        return "Ω"
    if normalized == CENTER_DIGIT:
        return "Id"
    if normalized == CYCLE_END:
        return "Π"
    return "transition"


def state_symbol(digit: int) -> object:
    """Return algebraic symbol at Ω/Id/Π positions, otherwise range value."""
    kind = state_kind(digit)
    if kind == "Ω":
        return OMEGA
    if kind == "Id":
        return CENTER_VALUE
    if kind == "Π":
        return PI
    return state_range_value(digit)


def cycle_distance(left: int, right: int) -> int:
    """Return shortest distance on the closed digit cycle."""
    forward = (normalize_digit(right) - normalize_digit(left)) % CYCLE_LENGTH
    backward = (normalize_digit(left) - normalize_digit(right)) % CYCLE_LENGTH
    return min(forward, backward)


@dataclass(frozen=True)
class UroborosState:
    """One state of the Great Uroboros cycle."""

    digit: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "digit", normalize_digit(self.digit))

    @property
    def value(self) -> float:
        """Return coordinate in [-1, 1]."""
        return state_range_value(self.digit)

    @property
    def kind(self) -> str:
        """Return semantic kind."""
        return state_kind(self.digit)

    @property
    def symbol(self) -> object:
        """Return algebraic symbol for this position."""
        return state_symbol(self.digit)

    def step(self, *, steps: int = 1) -> UroborosState:
        """Move forward in the cycle."""
        return UroborosState(cycle_step(self.digit, steps=steps))


def state_at(digit: int) -> UroborosState:
    """Return Uroboros state by digit."""
    return UroborosState(digit)
