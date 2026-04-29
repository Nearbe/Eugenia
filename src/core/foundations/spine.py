"""Spine levels ``Dⁿ(Id)`` from Universe/Math/06_Степени_двойки.md."""

from __future__ import annotations

from dataclasses import dataclass

from .constants import D_ID

MIN_SPINE_LEVEL = 0


@dataclass(frozen=True)
class SpineLevel:
    """One support node on the U-system spine: ``Dⁿ(Id)``."""

    depth: int = MIN_SPINE_LEVEL

    def __post_init__(self) -> None:
        if self.depth < MIN_SPINE_LEVEL:
            raise ValueError("spine depth must be non-negative")

    def branch(self) -> SpineLevel:
        """Return ``Hⁿ⁺¹ = D(Hⁿ)``."""
        return SpineLevel(self.depth + 1)

    def compress(self) -> SpineLevel:
        """Return ``Dⁿ(Id) : D(Id) = Dⁿ⁻¹(Id)`` with Id fixed at depth 0."""
        if self.depth == MIN_SPINE_LEVEL:
            return self
        return SpineLevel(self.depth - 1)

    def value(self) -> float:
        """Return the arithmetic representative ``2ⁿ``."""
        return D_ID**self.depth

    def level(self) -> int:
        """Return ``L(Dⁿ(Id)) = n``."""
        return self.depth

    def __float__(self) -> float:
        return float(self.value())

    def __repr__(self) -> str:
        if self.depth == MIN_SPINE_LEVEL:
            return "Id"
        return f"D^{self.depth}(Id)"


def spine_level(depth: int = MIN_SPINE_LEVEL) -> SpineLevel:
    """Construct a spine level ``Dⁿ(Id)``."""
    return SpineLevel(depth)


def is_spine_level(value: object) -> bool:
    """Return True when ``value`` is a spine-level object."""
    return isinstance(value, SpineLevel)
