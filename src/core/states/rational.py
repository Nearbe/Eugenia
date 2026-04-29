"""Participation ratios from Universe/Math/05_Рациональные.md.

A rational state is not just a collapsed float. It is the relation ``p : q``
inside the whole, with ``q`` outside Ω. Branching and compression act on both
parts, preserving the participation ratio.
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

from ..algebra import add, branch, compress, divide, is_omega, multiply


@dataclass(frozen=True)
class ParticipationRatio:
    """A U-system participation ratio ``numerator : denominator``."""

    numerator: object
    denominator: object

    def __post_init__(self) -> None:
        if is_omega(self.denominator):
            raise ValueError("participation ratio denominator must not be Ω")

    def __repr__(self) -> str:
        return f"{self.numerator!r} : {self.denominator!r}"

    def value(self) -> object:
        """Collapse the relation to the current U-division value."""
        return divide(self.numerator, self.denominator)

    def branch(self) -> ParticipationRatio:
        """Return ``(p : q) : Ω = D(p) : D(q)``."""
        return ParticipationRatio(branch(self.numerator), branch(self.denominator))

    def compress(self) -> ParticipationRatio:
        """Return ``(p : q) : D(Id) = H(p) : H(q)``."""
        return ParticipationRatio(compress(self.numerator), compress(self.denominator))

    def add(self, other: ParticipationRatio) -> ParticipationRatio:
        """Return ``(p1 : q) ⊕ (p2 : q) = (p1 ⊕ p2) : q``."""
        if self.denominator != other.denominator:
            raise ValueError("participation addition requires the same denominator")
        return ParticipationRatio(add(self.numerator, other.numerator), self.denominator)

    def multiply(self, other: ParticipationRatio) -> ParticipationRatio:
        """Return ``(p1 : q1) ⊗ (p2 : q2) = (p1 ⊗ p2) : (q1 ⊗ q2)``."""
        return ParticipationRatio(
            multiply(self.numerator, other.numerator),
            multiply(self.denominator, other.denominator),
        )

    def divide_by(self, denominator: object) -> ParticipationRatio:
        """Return ordinary scale division of the relation by finite ``denominator``."""
        if is_omega(denominator):
            return self.branch()
        return ParticipationRatio(self.numerator, multiply(self.denominator, denominator))

    def __float__(self) -> float:
        return float(self.value())


def participation_ratio(numerator: object, denominator: object) -> ParticipationRatio:
    """Construct a participation ratio ``numerator : denominator``."""
    return ParticipationRatio(numerator, denominator)
