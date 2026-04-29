"""Base U-algebra rules.

The U-system uses ordinary arithmetic for finite values. The only changed
finite operation is division by Ω: ``a : Ω = D(a)``. Algebraic Π/Fullness is a
separate closed state described in Universe/Math/10–12.
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

from collections.abc import Iterable
from typing import TYPE_CHECKING

from .constants import D_ID, OMEGA
from .infinity import PI, is_fullness
from .vectorization import map_scalar_or_vector

if TYPE_CHECKING:
    from .complex_plane import ComplexFullness, ComplexState
    from .dual_number import DualNumber
    from .fullness_share import FullnessShare
    from .rational import ParticipationRatio
    from .spine import SpineLevel

IDENTITY = 1.0


def _participation_ratio(value: object) -> ParticipationRatio | None:
    """Return ``value`` as a participation ratio when it belongs to that layer."""
    from .rational import ParticipationRatio

    return value if isinstance(value, ParticipationRatio) else None


def _dual_number(value: object) -> DualNumber | None:
    """Return ``value`` as a dual number when it belongs to that layer."""
    from .dual_number import DualNumber

    return value if isinstance(value, DualNumber) else None


def _fullness_share(value: object) -> FullnessShare | None:
    """Return ``value`` as a fullness share when it belongs to that layer."""
    from .fullness_share import FullnessShare

    return value if isinstance(value, FullnessShare) else None


def _complex_state(value: object) -> ComplexState | None:
    """Return ``value`` as a complex state when it belongs to that layer."""
    from .complex_plane import ComplexState

    return value if isinstance(value, ComplexState) else None


def _complex_fullness(value: object) -> ComplexFullness | None:
    """Return ``value`` as complex fullness when it belongs to that layer."""
    from .complex_plane import ComplexFullness

    return value if isinstance(value, ComplexFullness) else None


def _spine_level(value: object) -> SpineLevel | None:
    """Return ``value`` as a spine level when it belongs to that layer."""
    from .spine import SpineLevel

    return value if isinstance(value, SpineLevel) else None


def is_omega(value: object) -> bool:
    """Return True for the U-system potential Ω."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and float(value) == OMEGA


def is_identity(value: object) -> bool:
    """Return True for the finite identity Id."""
    level = _spine_level(value)
    return value == IDENTITY or (level is not None and level.depth == 0)


def branch(value: object) -> object:
    """Return ``D(value) = value : Ω``."""
    dual = _dual_number(value)
    if dual is not None:
        return dual.branch()
    share = _fullness_share(value)
    if share is not None:
        return share.branch()
    complex_fullness = _complex_fullness(value)
    if complex_fullness is not None:
        return complex_fullness.branch()
    complex_value = _complex_state(value)
    if complex_value is not None:
        return complex_value.branch()
    level = _spine_level(value)
    if level is not None:
        return level.branch()
    ratio = _participation_ratio(value)
    if ratio is not None:
        return ratio.branch()
    if is_fullness(value):
        return PI
    return map_scalar_or_vector(value, lambda scalar: scalar * D_ID, name="branch input")


def compress(value: object) -> object:
    """Return ``H(value) = value : D(Id)``."""
    dual = _dual_number(value)
    if dual is not None:
        return dual.compress()
    share = _fullness_share(value)
    if share is not None:
        return share.compress()
    complex_fullness = _complex_fullness(value)
    if complex_fullness is not None:
        return complex_fullness.compress()
    complex_value = _complex_state(value)
    if complex_value is not None:
        return complex_value.compress()
    level = _spine_level(value)
    if level is not None:
        return level.compress()
    ratio = _participation_ratio(value)
    if ratio is not None:
        return ratio.compress()
    if is_fullness(value):
        return PI
    return map_scalar_or_vector(value, lambda scalar: scalar / D_ID, name="compress input")


def add(left: object, right: object) -> object:
    """Return U-addition: ordinary addition with Π closed under fullness."""
    left_dual = _dual_number(left)
    right_dual = _dual_number(right)
    if left_dual is not None or right_dual is not None:
        if left_dual is None or right_dual is None:
            raise TypeError("dual addition requires two dual numbers")
        return left_dual.add(right_dual)
    left_share = _fullness_share(left)
    right_share = _fullness_share(right)
    if left_share is not None or right_share is not None:
        if left_share is None or right_share is None:
            raise TypeError("fullness-share addition requires two shares")
        return left_share.add(right_share)
    if _complex_fullness(left) is not None or _complex_fullness(right) is not None:
        from .complex_plane import PI_Z

        return PI_Z
    left_complex = _complex_state(left)
    right_complex = _complex_state(right)
    if left_complex is not None or right_complex is not None:
        if left_complex is None or right_complex is None:
            raise TypeError("complex addition requires two complex states")
        return left_complex.add(right_complex)
    left_ratio = _participation_ratio(left)
    right_ratio = _participation_ratio(right)
    if left_ratio is not None or right_ratio is not None:
        if left_ratio is None or right_ratio is None:
            raise TypeError("participation addition requires two participation ratios")
        return left_ratio.add(right_ratio)
    if is_fullness(left) or is_fullness(right):
        return PI
    return float(left) + float(right)


def multiply(left: object, right: object) -> object:
    """Return U-multiplication: ordinary multiplication, Ω annihilates form."""
    left_dual = _dual_number(left)
    right_dual = _dual_number(right)
    if left_dual is not None or right_dual is not None:
        if left_dual is None or right_dual is None:
            raise TypeError("dual multiplication requires two dual numbers")
        return left_dual.multiply(right_dual)
    left_share = _fullness_share(left)
    right_share = _fullness_share(right)
    if left_share is not None or right_share is not None:
        if left_share is None or right_share is None:
            raise TypeError("fullness-share multiplication requires two shares")
        return left_share.multiply(right_share)
    if _complex_fullness(left) is not None or _complex_fullness(right) is not None:
        from .complex_plane import PI_Z

        return PI_Z
    left_complex = _complex_state(left)
    right_complex = _complex_state(right)
    if left_complex is not None or right_complex is not None:
        if left_complex is None or right_complex is None:
            raise TypeError("complex multiplication requires two complex states")
        return left_complex.multiply(right_complex)
    left_ratio = _participation_ratio(left)
    right_ratio = _participation_ratio(right)
    if left_ratio is not None or right_ratio is not None:
        if left_ratio is None or right_ratio is None:
            raise TypeError("participation multiplication requires two participation ratios")
        return left_ratio.multiply(right_ratio)
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
    numerator_dual = _dual_number(numerator)
    if numerator_dual is not None:
        if is_omega(denominator):
            return numerator_dual.branch()
        if denominator == D_ID:
            return numerator_dual.compress()
        return numerator_dual.scale(divide(1.0, denominator))

    numerator_share = _fullness_share(numerator)
    if numerator_share is not None:
        if is_omega(denominator):
            return numerator_share.branch()
        if denominator == D_ID:
            return numerator_share.compress()
        return numerator_share.divide_by(denominator)

    numerator_complex_fullness = _complex_fullness(numerator)
    if numerator_complex_fullness is not None:
        return numerator_complex_fullness if not _complex_fullness(denominator) else IDENTITY

    numerator_complex = _complex_state(numerator)
    if numerator_complex is not None:
        if is_fullness(denominator):
            return OMEGA
        if is_omega(denominator):
            return numerator_complex.branch()
        if denominator == D_ID:
            return numerator_complex.compress()
        denominator_complex = _complex_state(denominator)
        if denominator_complex is None:
            return numerator_complex.scale(1.0 / float(denominator))
        return numerator_complex.divide_by(denominator_complex)

    numerator_ratio = _participation_ratio(numerator)
    if numerator_ratio is not None:
        if is_fullness(denominator):
            return OMEGA
        if is_omega(denominator):
            return numerator_ratio.branch()
        if denominator == D_ID:
            return numerator_ratio.compress()
        return numerator_ratio.divide_by(denominator)

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
    """Return U-power with Ω exponent, Π closure and spine scaling."""
    dual = _dual_number(base)
    if dual is not None:
        if is_omega(exponent):
            return IDENTITY
        if is_fullness(exponent):
            return PI
        return dual.power(exponent)
    level = _spine_level(base)
    if level is not None:
        if is_omega(exponent):
            return IDENTITY
        if is_fullness(exponent):
            return PI
        return level.scale(exponent)
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
