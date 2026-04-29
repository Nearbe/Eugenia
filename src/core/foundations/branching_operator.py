"""Linear branching operator from Universe/Math/13."""

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

from .constants import D_ID, OMEGA

SCALAR_BASIS_SIZE: Final[int] = 1
DUAL_BASIS_SIZE: Final[int] = 2


@dataclass(frozen=True)
class BranchingOperator:
    """Operator ``D(a) = a : Ω = a ⊕ a``."""

    eigenvalue: float = D_ID

    def apply(self, value: object) -> object:
        """Apply the U-system branching operator."""
        from .u_algebra import branch

        return branch(value)

    def inverse(self, value: object) -> object:
        """Apply the compression operator ``H``."""
        from .u_algebra import compress

        return compress(value)

    def eigen_class(self) -> float:
        """Return the only scaling eigen-class ``D(Id)``."""
        return self.eigenvalue

    def kernel(self) -> frozenset[float]:
        """Return ``Ker D = {Ω}``."""
        return frozenset({OMEGA})

    def image_is_carrier(self) -> bool:
        """Return True because ``Im D = 𝕌``: every x comes from ``H(x)``."""
        return True

    def scalar_matrix(self) -> tuple[tuple[float, ...], ...]:
        """Return matrix ``[D(Id)]`` in basis ``{Id}``."""
        return ((self.eigenvalue,),)

    def dual_matrix(self) -> tuple[tuple[float, ...], ...]:
        """Return homothety matrix in basis ``{Id, ε}``."""
        return ((self.eigenvalue, OMEGA), (OMEGA, self.eigenvalue))

    def is_linear_on_pair(self, left: object, right: object) -> bool:
        """Check ``D(a ⊕ b) = D(a) ⊕ D(b)`` for two finite states."""
        from .u_algebra import add

        return self.apply(add(left, right)) == add(self.apply(left), self.apply(right))


D_OPERATOR: Final[BranchingOperator] = BranchingOperator()


def branching_operator() -> BranchingOperator:
    """Return the canonical branching operator instance."""
    return D_OPERATOR
