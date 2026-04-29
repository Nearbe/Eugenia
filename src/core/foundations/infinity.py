"""Algebra of Π — Fullness/Infinity in the U-system.

Π is not IEEE infinity here. It is the limit of branching and follows the
rules from Universe/Math/10_Бесконечность.md and 12_Алгебра_процентов.md.
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
from typing import Final


@dataclass(frozen=True)
class Fullness:
    """The algebraic Π state: absolute fullness, not an unbounded float."""

    symbol: str = "Π"

    def __repr__(self) -> str:
        return self.symbol

    def __str__(self) -> str:
        return self.symbol


PI: Final[Fullness] = Fullness()
PI_INFINITY: Final[Fullness] = PI


def is_fullness(value: object) -> bool:
    """Return True when ``value`` is the algebraic Π state."""
    return value == PI


def fullness_divide(numerator: object, denominator: object) -> object:
    """Apply Π division identities.

    Covered identities:
    - Π : Ω = Π
    - Π : D(Id) = Π
    - Π : Π = Id
    """
    from .constants import D_ID, OMEGA

    if not is_fullness(numerator):
        raise TypeError("fullness_divide expects Π as numerator")
    if is_fullness(denominator):
        return 1.0
    if denominator == OMEGA or denominator == D_ID:
        return PI
    return PI
