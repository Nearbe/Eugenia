from __future__ import annotations

from dataclasses import dataclass

from ..states.spine import SpineLevel, spine_level
from .paths_count import paths_count


@dataclass(frozen=True)
class BranchingLevel:
    """Decision-tree level with capacity ``Dⁿ(Id)``."""

    depth: int

    def __post_init__(self) -> None:
        if self.depth < 0:
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
        return BranchingLevel(self.depth + 1)

    def address(self, value: int) -> tuple[int, ...]:
        """Return binary route to ``value`` at this level."""
        from ..number_theory.number_structure import binary_address

        return binary_address(value, depth=self.depth)
