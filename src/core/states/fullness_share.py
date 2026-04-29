"""Algebra of shares ``a : Π`` from Universe/Math/11–12."""

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

from ..infinity.infinity import PI


@dataclass(frozen=True)
class FullnessShare:
    """Relative participation in Π: ``intensity : Π``."""

    intensity: object

    @property
    def denominator(self) -> object:
        """Return the fixed denominator Π."""
        return PI

    def branch(self) -> FullnessShare:
        """Return ``(a : Π) : Ω = D(a) : Π``."""
        from ..algebra import branch

        return FullnessShare(branch(self.intensity))

    def compress(self) -> FullnessShare:
        """Return ``(a : Π) : D(Id) = (a : D(Id)) : Π``."""
        from ..algebra import compress

        return FullnessShare(compress(self.intensity))

    def add(self, other: FullnessShare) -> FullnessShare:
        """Return ``(a : Π) ⊕ (b : Π) = (a ⊕ b) : Π``."""
        from ..algebra import add

        return FullnessShare(add(self.intensity, other.intensity))

    def multiply(self, other: FullnessShare) -> FullnessShare:
        """Return ``(a : Π) ⊗ (b : Π) = (a ⊗ b) : Π``."""
        from ..algebra import multiply

        return FullnessShare(multiply(self.intensity, other.intensity))

    def divide_by(self, other: object) -> object:
        """Return ``(a : Π) : (b : Π) = a : b`` or scale the share."""
        from ..algebra import divide, multiply

        if isinstance(other, FullnessShare):
            return divide(self.intensity, other.intensity)
        return FullnessShare(divide(self.intensity, other)) if other == PI else FullnessShare(
            multiply(self.intensity, divide(1.0, other))
        )

    def __repr__(self) -> str:
        return f"{self.intensity!r} : Π"


def fullness_share(intensity: object = 1.0) -> FullnessShare:
    """Construct a share ``intensity : Π``."""
    return FullnessShare(intensity)
