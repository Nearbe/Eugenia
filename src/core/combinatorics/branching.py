"""Combinatorics from Universe/Math/26_Комбинаторика.md."""

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

from ..foundations.spine import SpineLevel, spine_level
from ..number_theory.number_structure import binary_address, modulus_from_depth

MIN_COUNT = 0
IDENTITY_COUNT = 1


@dataclass(frozen=True)
class BranchingLevel:
    """Decision-tree level with capacity ``Dⁿ(Id)``."""

    depth: int

    def __post_init__(self) -> None:
        if self.depth < MIN_COUNT:
            raise ValueError("branching depth must be non-negative")

    @property
    def spine(self) -> SpineLevel:
        """Return the corresponding spine state ``Dⁿ(Id)``."""
        return spine_level(self.depth)

    @property
    def paths(self) -> int:
        """Return number of paths of this length."""
        return paths_count(self.depth)

    def branch(self) -> BranchingLevel:
        """Return the next bifurcation level."""
        return BranchingLevel(self.depth + IDENTITY_COUNT)

    def address(self, value: int) -> tuple[int, ...]:
        """Return binary route to ``value`` at this level."""
        return binary_address(value, depth=self.depth)


def _validate_non_negative(value: int, *, name: str) -> int:
    """Validate a non-negative integer."""
    integer = int(value)
    if integer < MIN_COUNT:
        raise ValueError(f"{name} must be non-negative")
    return integer


def paths_count(depth: int) -> int:
    """Return number of paths of length ``depth``: ``Dⁿ(Id)``."""
    depth_value = _validate_non_negative(depth, name="depth")
    return modulus_from_depth(depth_value)


def factorial(count: int) -> int:
    """Return ``n!``: orderings of distinguishable acts."""
    count_value = _validate_non_negative(count, name="count")
    result = IDENTITY_COUNT
    for value in range(2, count_value + IDENTITY_COUNT):
        result *= value
    return result


def binomial_coefficient(total: int, chosen: int) -> int:
    """Return ``C(n,k)`` paths with exactly ``k`` right-branch choices."""
    total_value = _validate_non_negative(total, name="total")
    chosen_value = _validate_non_negative(chosen, name="chosen")
    if chosen_value > total_value:
        return MIN_COUNT
    left_count = chosen_value
    right_count = total_value - chosen_value
    return factorial(total_value) // (factorial(left_count) * factorial(right_count))


def boolean_capacity(size: int) -> int:
    """Return power-set capacity ``|P(A)| = Dⁿ(Id)``."""
    return paths_count(size)


def branching_distribution(depth: int) -> tuple[int, ...]:
    """Return binomial layer distribution for all right-choice counts."""
    depth_value = _validate_non_negative(depth, name="depth")
    return tuple(binomial_coefficient(depth_value, choice) for choice in range(depth_value + 1))


def routes(depth: int) -> tuple[tuple[int, ...], ...]:
    """Return all binary routes at a finite branching depth."""
    depth_value = _validate_non_negative(depth, name="depth")
    return tuple(binary_address(value, depth=depth_value) for value in range(paths_count(depth_value)))
