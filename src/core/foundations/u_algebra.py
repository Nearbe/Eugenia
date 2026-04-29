"""Base U-algebra rules.

The U-system uses ordinary arithmetic for finite values. The only changed
finite operation is division by Ω: ``a : Ω = D(a)``. Algebraic Π/Fullness is a
separate closed state described in Universe/Math/10–12.
"""

from __future__ import annotations

from collections.abc import Iterable

from .constants import D_ID, OMEGA
from .infinity import PI, is_fullness
from .vectorization import map_scalar_or_vector

IDENTITY = 1.0


def is_omega(value: object) -> bool:
    """Return True for the U-system potential Ω."""
    return value == OMEGA


def is_identity(value: object) -> bool:
    """Return True for the finite identity Id."""
    return value == IDENTITY


def branch(value: object) -> object:
    """Return ``D(value) = value : Ω``."""
    if is_fullness(value):
        return PI
    return map_scalar_or_vector(value, lambda scalar: scalar * D_ID, name="branch input")


def compress(value: object) -> object:
    """Return ``H(value) = value : D(Id)``."""
    if is_fullness(value):
        return PI
    return map_scalar_or_vector(value, lambda scalar: scalar / D_ID, name="compress input")


def add(left: object, right: object) -> object:
    """Return U-addition: ordinary addition with Π closed under fullness."""
    if is_fullness(left) or is_fullness(right):
        return PI
    return float(left) + float(right)


def multiply(left: object, right: object) -> object:
    """Return U-multiplication: ordinary multiplication, Ω annihilates form."""
    if is_omega(left) or is_omega(right):
        return OMEGA
    if is_fullness(left) or is_fullness(right):
        return PI
    return float(left) * float(right)


def divide(numerator: object, denominator: object) -> object:
    """Return U-division ``numerator : denominator``.

    Rules:
    - ``a : Ω = D(a)`` for active finite ``a``;
    - ``Ω : b = Ω`` for finite ``b``;
    - ``Ω : Ω = Ω``;
    - ``Π : Ω = Π``, ``Π : D(Id) = Π``, ``Π : Π = Id``;
    - otherwise ordinary real division.
    """
    if is_fullness(numerator):
        if is_fullness(denominator):
            return IDENTITY
        return PI
    if is_fullness(denominator):
        return OMEGA
    if is_omega(numerator):
        return OMEGA
    if is_omega(denominator):
        return branch(numerator)
    if denominator == D_ID:
        return compress(numerator)
    return float(numerator) / float(denominator)


def power(base: object, exponent: object) -> object:
    """Return U-power with Ω exponent and Π closure."""
    if is_fullness(base):
        return PI
    if is_omega(base) and is_omega(exponent):
        return OMEGA
    if is_omega(exponent):
        return IDENTITY
    if is_fullness(exponent):
        return PI
    return float(base) ** float(exponent)


def lift(value: float | int | Iterable[float], operation) -> object:
    """Apply a scalar U-operation to finite scalars or vectors."""
    return map_scalar_or_vector(value, operation, name="U algebra input")
