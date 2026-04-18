"""
Core mathematical operators — compatibility shim.

Все функции перемещены в специализированные модули:
- spine: ridge_level, ridge_to_percentage, percentage_to_ridge, spine_value, spine_value_array
- pyramid: fractal_pyramid_level, fractal_pyramid, fractal_pyramid_to_string, fractal_bridge_analysis
- chain: omega_to_pi_chain, chain_identity_check
"""

from .chain import (
    chain_identity_check,
    omega_to_pi_chain,
)
from .pyramid import (
    fractal_bridge_analysis,
    fractal_pyramid,
    fractal_pyramid_level,
    fractal_pyramid_to_string,
)
from .spine import (
    percentage_to_ridge,
    ridge_level,
    ridge_to_percentage,
    spine_value,
    spine_value_array,
)

__all__ = [
    "ridge_level",
    "ridge_to_percentage",
    "percentage_to_ridge",
    "spine_value",
    "spine_value_array",
    "fractal_pyramid_level",
    "fractal_pyramid",
    "fractal_pyramid_to_string",
    "fractal_bridge_analysis",
    "omega_to_pi_chain",
    "chain_identity_check",
]
