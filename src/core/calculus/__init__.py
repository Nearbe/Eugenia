#  Copyright (c)2026.
#  ╔═══════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═════════════════════════════════╝
"""Differential and integral U-calculus modules."""

from .add_derivative import add_derivative
from .branched_derivative import branched_derivative
from .branched_integral import branched_integral
from .chain_derivative import chain_derivative
from .compressed_derivative import compressed_derivative
from .compressed_integral import compressed_integral
from .definite_integral import definite_integral
from .derivative import derivative
from .differential_state import differential_state, IDENTITY_VELOCITY
from .integral_on_log_depth import integral_on_log_depth
from .power_antiderivative import power_antiderivative
from .power_derivative import power_derivative
from .second_derivative import second_derivative
from .branching_growth_velocity import branching_growth_velocity
from .antiderivative import antiderivative

__all__ = [
    "add_derivative",
    "branched_derivative",
    "branched_integral",
    "chain_derivative",
    "compressed_derivative",
    "compressed_integral",
    "definite_integral",
    "derivative",
    "differential_state",
    "IDENTITY_VELOCITY",
    "integral_on_log_depth",
    "power_antiderivative",
    "power_derivative",
    "second_derivative",
    "branching_growth_velocity",
    "antiderivative",
]
