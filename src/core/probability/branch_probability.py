"""Probability as branch share from Universe/Math/27_Вероятность.md."""

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

from ..combinatorics.branching import binomial_coefficient, paths_count
from ..foundations.fullness_share import FullnessShare, fullness_share
from ..foundations.u_algebra import divide

NO_BRANCHES: Final[int] = 0
CERTAINTY: Final[float] = 1.0
IMPOSSIBILITY: Final[float] = 0.0


@dataclass(frozen=True)
class BranchProbability:
    """Probability as ``matching branches : total branches``."""

    matching_branches: int
    total_branches: int

    def __post_init__(self) -> None:
        if self.matching_branches < NO_BRANCHES:
            raise ValueError("matching branches must be non-negative")
        if self.total_branches <= NO_BRANCHES:
            raise ValueError("total branches must be positive")
        if self.matching_branches > self.total_branches:
            raise ValueError("matching branches cannot exceed total branches")

    @property
    def value(self) -> object:
        """Return ``matching : total`` through U-division."""
        return divide(self.matching_branches, self.total_branches)

    def to_fullness_share(self) -> FullnessShare:
        """Return ``P(A) ⊗ Π`` as a fullness share."""
        return fullness_share(self.value)

    def conditional(self, condition: BranchProbability) -> object:
        """Return ``P(A|B)=P(A∩B):P(B)`` for finite branch shares."""
        return conditional_probability(self, condition)


def branch_probability(matching_branches: int, total_branches: int) -> BranchProbability:
    """Create a validated branch probability."""
    return BranchProbability(int(matching_branches), int(total_branches))


def binomial_probability(successes: int, acts: int) -> BranchProbability:
    """Return ``P(k)=C(n,k):Dⁿ(Id)``."""
    if successes < NO_BRANCHES or acts < NO_BRANCHES or successes > acts:
        return branch_probability(NO_BRANCHES, CERTAINTY_AS_BRANCHES)
    return branch_probability(binomial_coefficient(acts, successes), paths_count(acts))


CERTAINTY_AS_BRANCHES: Final[int] = 1


def conditional_probability(intersection: BranchProbability, condition: BranchProbability) -> object:
    """Return ``P(A∩B):P(B)``."""
    if condition.matching_branches == NO_BRANCHES:
        raise ValueError("condition probability must be active")
    return divide(intersection.value, condition.value)


def total_probability(parts: tuple[BranchProbability, ...]) -> object:
    """Return sum of disjoint branch shares."""
    if not parts:
        return IMPOSSIBILITY
    total_denominator = parts[0].total_branches
    if any(part.total_branches != total_denominator for part in parts):
        raise ValueError("total probability requires common branch depth")
    return divide(sum(part.matching_branches for part in parts), total_denominator)


def universe_probability() -> float:
    """Return the system's own certainty: Id."""
    return CERTAINTY
