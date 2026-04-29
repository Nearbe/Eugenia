"""Solenoid point as phase plus D-adic binary history.

Universe/Math/23–24 treats solenoid and D-adic integers as the same space seen
from two sides: real phase on the circle and depth history by shared binary
prefixes.
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

from core.foundations.lo_shu import LoShuAddress

from .encode_solenoid_trajectory import encode_solenoid_trajectory
from .solenoid_distance import solenoid_distance
from .solenoid_similarity import solenoid_similarity

CIRCLE_PERIOD = 1.0
BIT_ZERO = 0
BIT_ONE = 1
FIRST_BIT_INDEX = 0


def validate_history(history: object) -> tuple[int, ...]:
    """Return a strict binary solenoid history."""
    bits = tuple(int(bit) for bit in history)  # type: ignore[arg-type]
    if any(bit not in (BIT_ZERO, BIT_ONE) for bit in bits):
        raise ValueError("solenoid history must contain only 0/1 bits")
    return bits


def common_prefix_length(left: object, right: object) -> int:
    """Return number of shared initial history bits."""
    left_bits = validate_history(left)
    right_bits = validate_history(right)
    common = 0
    for left_bit, right_bit in zip(left_bits, right_bits):
        if left_bit != right_bit:
            return common
        common += 1
    return common


def d_adic_norm_from_depth(depth: int) -> float:
    """Return ``|Dⁿ(Id)|_D = Id : Dⁿ(Id)``."""
    if depth < 0:
        raise ValueError("D-adic depth must be non-negative")
    return 2.0 ** (-depth)


@dataclass(frozen=True)
class SolenoidPoint:
    """One solenoid point: real phase plus D-adic binary history."""

    phase: float
    history: tuple[int, ...]

    @classmethod
    def from_value(cls, value: float, *, depth: int) -> SolenoidPoint:
        """Build a point by encoding the phase history of ``value``."""
        return cls(float(value) % CIRCLE_PERIOD, tuple(encode_solenoid_trajectory(value, depth)))

    def __post_init__(self) -> None:
        object.__setattr__(self, "phase", float(self.phase) % CIRCLE_PERIOD)
        object.__setattr__(self, "history", validate_history(self.history))

    def shift(self) -> SolenoidPoint:
        """Bernoulli shift: ``ξ ↦ 2ξ mod Id`` and drop the first history bit."""
        shifted_phase = (self.phase * 2.0) % CIRCLE_PERIOD
        shifted_history = self.history[1:] if self.history else ()
        return SolenoidPoint(shifted_phase, shifted_history)

    def shared_depth(self, other: SolenoidPoint) -> int:
        """Return D-adic shared depth with another solenoid point."""
        return common_prefix_length(self.history, other.history)

    def history_distance(self, other: SolenoidPoint) -> float:
        """Return prefix distance of histories."""
        return solenoid_distance(list(self.history), list(other.history))

    def history_similarity(self, other: SolenoidPoint) -> float:
        """Return prefix similarity of histories."""
        return solenoid_similarity(list(self.history), list(other.history))

    def d_adic_norm(self, other: SolenoidPoint) -> float:
        """Return D-adic closeness induced by the shared prefix depth."""
        if self.history == other.history:
            return 0.0
        return d_adic_norm_from_depth(self.shared_depth(other))


def solenoid_seed_from_lo_shu(address: LoShuAddress) -> SolenoidPoint:
    """Unfold a Lo Shu address into the first solenoid point."""
    return SolenoidPoint(phase=address.phase, history=address.history)
