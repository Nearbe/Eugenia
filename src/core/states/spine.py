"""Spine levels ``Dⁿ(Id)`` from Universe/Math/06–07."""

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

from ..constants.constants import D_ID

MIN_SPINE_DEPTH = 0.0
DEPTH_STEP = 1.0


@dataclass(frozen=True)
class SpineLevel:
    """One support node or fractional step on the U-system spine: ``Dⁿ(Id)``."""

    depth: float = MIN_SPINE_DEPTH

    def __post_init__(self) -> None:
        depth = float(self.depth)
        if depth < MIN_SPINE_DEPTH:
            raise ValueError("spine depth must be non-negative")
        object.__setattr__(self, "depth", depth)

    def branch(self) -> SpineLevel:
        """Return ``Hⁿ⁺¹ = D(Hⁿ)``."""
        return SpineLevel(self.depth + DEPTH_STEP)

    def compress(self) -> SpineLevel:
        """Return ``Dⁿ(Id) : D(Id) = Dⁿ⁻¹(Id)`` with Id fixed at depth 0."""
        if self.depth == MIN_SPINE_DEPTH:
            return self
        return SpineLevel(max(MIN_SPINE_DEPTH, self.depth - DEPTH_STEP))

    def scale(self, exponent: object) -> SpineLevel:
        """Return ``(Dⁿ(Id))^b = D^(n·b)(Id)``."""
        return SpineLevel(self.depth * float(exponent))

    def root(self, degree: object) -> SpineLevel:
        """Return ``√[degree]{Dⁿ(Id)} = D^(n:degree)(Id)``."""
        degree_value = float(degree)
        if degree_value == 0.0:
            raise ValueError("root degree must not be Ω")
        return SpineLevel(self.depth / degree_value)

    def value(self) -> float:
        """Return the arithmetic representative ``2ⁿ``."""
        return D_ID**self.depth

    def level(self) -> float:
        """Return ``L(Dⁿ(Id)) = n``."""
        return self.depth

    def __float__(self) -> float:
        return float(self.value())

    def __repr__(self) -> str:
        if self.depth == MIN_SPINE_DEPTH:
            return "Id"
        return f"D^{self.depth:g}(Id)"


def spine_level(depth: float = MIN_SPINE_DEPTH) -> SpineLevel:
    """Construct a spine level ``Dⁿ(Id)``."""
    return SpineLevel(depth)


def root(value: SpineLevel, degree: object) -> SpineLevel:
    """Return a fractional spine step: ``√[degree]{value}``."""
    return value.root(degree)


def is_spine_level(value: object) -> bool:
    """Return True when ``value`` is a spine-level object."""
    return isinstance(value, SpineLevel)
