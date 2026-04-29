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

from ..infinity.infinity import PI, is_fullness
from ._complex_fullness import _complex_fullness
from ._complex_state import _complex_state
from ._dual_number import _dual_number
from ._fullness_share import _fullness_share
from ._participation_ratio import _participation_ratio


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
        from ..states.complex_plane import PI_Z

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
