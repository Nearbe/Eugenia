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

from ..constants.constants import D_ID, OMEGA
from ..infinity.infinity import PI, is_fullness
from ._complex_fullness import _complex_fullness
from ._complex_state import _complex_state
from ._dual_number import _dual_number
from ._fullness_share import _fullness_share
from ._participation_ratio import _participation_ratio
from .branch import branch
from .compress import compress
from .identity import IDENTITY
from .is_omega import is_omega


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
        return (
            numerator_complex_fullness
            if not _complex_fullness(denominator)
            else IDENTITY
        )

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
