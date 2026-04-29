"""Number structure from Universe/Math/25_Строение_чисел.md."""

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

from ..constants.constants import D_ID
from ..states.spine import SpineLevel, spine_level
from ..algebra import branch

ATOM_DEPTH = 1.0
BINARY_BASE = int(D_ID)


def system_atom() -> SpineLevel:
    """Return the only prime atom of the system: ``D(Id)``."""
    return spine_level(ATOM_DEPTH)


def is_system_atom(value: object) -> bool:
    """Return true only for ``D(Id)``."""
    return isinstance(value, SpineLevel) and value.depth == ATOM_DEPTH


def is_composite_spine(value: object) -> bool:
    """Return true for all ``Dⁿ(Id)`` with ``n > Id``."""
    return isinstance(value, SpineLevel) and value.depth > ATOM_DEPTH


def spine_gcd(left: SpineLevel, right: SpineLevel) -> SpineLevel:
    """Return common ancestor: ``D^min(n,m)(Id)``."""
    return spine_level(min(left.depth, right.depth))


def spine_lcm(left: SpineLevel, right: SpineLevel) -> SpineLevel:
    """Return common descendant: ``D^max(n,m)(Id)``."""
    return spine_level(max(left.depth, right.depth))


def branched_spine_gcd(left: SpineLevel, right: SpineLevel) -> SpineLevel:
    """Return ``gcd(D(a),D(b)) = D(gcd(a,b))``."""
    result = branch(spine_gcd(left, right))
    if not isinstance(result, SpineLevel):
        raise TypeError("branched spine gcd must stay on the spine")
    return result


def branched_spine_lcm(left: SpineLevel, right: SpineLevel) -> SpineLevel:
    """Return ``lcm(D(a),D(b)) = D(lcm(a,b))``."""
    result = branch(spine_lcm(left, right))
    if not isinstance(result, SpineLevel):
        raise TypeError("branched spine lcm must stay on the spine")
    return result


def modulus_from_depth(depth: int) -> int:
    """Return ``Dⁿ(Id)`` as an integer modulus."""
    if depth < 0:
        raise ValueError("address depth must be non-negative")
    return BINARY_BASE**depth


def congruent(left: int, right: int, *, modulus: int) -> bool:
    """Return ``left ≡ right (mod modulus)``."""
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    return (int(left) - int(right)) % int(modulus) == 0


def branching_preserves_congruence(left: int, right: int, *, modulus: int) -> bool:
    """Return equivalence of congruence before and after branching."""
    return congruent(left, right, modulus=modulus) == congruent(
        BINARY_BASE * int(left),
        BINARY_BASE * int(right),
        modulus=BINARY_BASE * int(modulus),
    )


def binary_address(value: int, *, depth: int) -> tuple[int, ...]:
    """Return ``value mod Dⁿ(Id)`` as binary word of length ``n``."""
    modulus = modulus_from_depth(depth)
    residue = int(value) % modulus
    bits = tuple(int(bit) for bit in format(residue, f"0{depth}b"))
    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("binary address produced a non-binary digit")
    return bits
