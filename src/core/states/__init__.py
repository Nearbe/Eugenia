#  Copyright (c)2026.
#  ╔═════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║════════║══════════║═════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═════════════════════════════╝
"""State types: DualNumber, ComplexState, FullnessShare, ParticipationRatio, SpineLevel."""

from .dual_number import DualNumber, dual_number, is_dual_number, natural_velocity
from .complex_plane import (
    ComplexState,
    ComplexFullness,
    PI_Z,
    is_complex_state,
    is_complex_fullness,
    complex_state,
    conjugate,
    norm_squared,
    rotate,
    I,
)
from .fullness_share import FullnessShare, fullness_share
from .rational import ParticipationRatio, participation_ratio
from .spine import (
    SpineLevel,
    spine_level,
    root,
    is_spine_level,
    MIN_SPINE_DEPTH,
    DEPTH_STEP,
)
from .u_function import (
    UFunction,
    branching_function,
    compose,
    power_function,
    logarithmic_function,
    periodic_function,
)

__all__ = [
    "DualNumber",
    "dual_number",
    "is_dual_number",
    "natural_velocity",
    "ComplexState",
    "ComplexFullness",
    "PI_Z",
    "is_complex_state",
    "is_complex_fullness",
    "complex_state",
    "conjugate",
    "norm_squared",
    "rotate",
    "I",
    "FullnessShare",
    "fullness_share",
    "ParticipationRatio",
    "participation_ratio",
    "SpineLevel",
    "spine_level",
    "root",
    "is_spine_level",
    "MIN_SPINE_DEPTH",
    "DEPTH_STEP",
    "UFunction",
    "branching_function",
    "compose",
    "power_function",
    "logarithmic_function",
    "periodic_function",
]
