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
from ._complex_fullness import _complex_fullness
from ._complex_state import _complex_state
from ._dual_number import _dual_number
from ._fullness_share import _fullness_share
from ._participation_ratio import _participation_ratio
from .is_omega import is_omega


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
        from ..states.complex_plane import PI_Z

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
            raise TypeError(
                "participation multiplication requires two participation ratios"
            )
        return left_ratio.multiply(right_ratio)
    if is_omega(left) or is_omega(right):
        return OMEGA
    if is_fullness(left) or is_fullness(right):
        return PI
    return float(left) * float(right)
