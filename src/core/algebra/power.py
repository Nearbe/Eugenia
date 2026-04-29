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

from ..constants.constants import OMEGA
from ..infinity.infinity import PI, is_fullness
from ._dual_number import _dual_number
from ._spine_level import _spine_level
from .identity import IDENTITY
from .is_omega import is_omega


def power(base: object, exponent: object) -> object:
    """Return U-power with Ω exponent, Π closure and spine scaling."""
    dual = _dual_number(base)
    # Handles dual number powering with special constant returns
    if dual is not None:
        if is_omega(exponent):
            return IDENTITY
        if is_fullness(exponent):
            return PI
        return dual.power(exponent)
    # Handles spine level scaling with special constant returns
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
