"""Information from Universe/Math/30_Информация.md."""

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

from ..combinatorics.branching import BranchingLevel, paths_count
from ..foundations.constants import OMEGA
from ..foundations.infinity import PI
from ..foundations.logarithmic_axis import LOG_NEGATIVE_INFINITY, LOG_POSITIVE_INFINITY
from ..foundations.spine import SpineLevel, spine_level
from ..foundations.u_algebra import branch, compress
from ..number_theory.number_structure import binary_address
from ..operators.L import L

INFORMATION_STEP: Final[float] = 1.0
UNITY_INFORMATION = OMEGA


@dataclass(frozen=True)
class AddressedState:
    """State localized by a finite binary address."""

    mass: SpineLevel
    address: tuple[int, ...]

    @property
    def information(self) -> object:
        """Return address depth ``L(M)``."""
        return information(self.mass)


def information(mass: object) -> object:
    """Return ``I = L(M)`` with ``Id`` interpreted as unity before distinction."""
    if isinstance(mass, SpineLevel) and mass.depth == 0.0:
        return UNITY_INFORMATION
    return L(mass)


def mass_from_information(depth: object) -> object:
    """Return ``M = D^I(Id)`` from information depth."""
    if depth == LOG_POSITIVE_INFINITY:
        return PI
    if depth == UNITY_INFORMATION or depth == LOG_NEGATIVE_INFINITY:
        return spine_level(0)
    return spine_level(float(depth))


def branch_information(mass: object) -> object:
    """Return ``L(D(M)) = L(M) ⊕ Id``."""
    return information(branch(mass))


def compress_information(mass: object) -> object:
    """Return ``L(H(M)) = L(M) ⊖ Id`` for active masses."""
    return information(compress(mass))


def address_state(value: int, *, depth: int) -> AddressedState:
    """Return state localized by a binary address of length ``depth``."""
    return AddressedState(spine_level(depth), binary_address(value, depth=depth))


def address_cost(address: tuple[int, ...]) -> int:
    """Return number of choices needed to write an address."""
    return len(address)


def branching_level_information(level: BranchingLevel) -> object:
    """Return information stored in a finite branching level."""
    return information(level.spine)


def choice_capacity(depth: int) -> int:
    """Return number of distinguishable states at information depth ``depth``."""
    return paths_count(depth)
