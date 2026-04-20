"""
Core mathematical operators for the RealMath / Essentials framework.

Exports:
- delta: delta_field, inverse_delta_field (для sweep)
- complex_delta: complex_delta_field, complex_delta_properties (для Nucleus)
- complex: complex_norm, complex_conjugate, complex_multiply (для Nucleus)
- dual: dual_form, dual_multiply, dual_branch, dual_compress (для Nucleus)
- potential: has_potential, is_potential, resolve_potential
- vector: normalize_vector_safe
- limits: limit_branching, limit_compression
- percent: to_percentage, from_percentage, percentage_add, percentage_multiply
- similarity: similarity (cosine на алгебре долей)
- distance: delta_distance, euclidean_distance
- p_adic: v2_adic_valuation, p_adic_distance, d_adic_convergence
- fractal_dimension: fractal_dimension_from_betti, compute_betti_scaling_exponent
- sweep: compute_sweep, encode_solenoid_trajectory, solenoid_distance, rg_aware_sweep
- spine: ridge_level, ridge_to_percentage, percentage_to_ridge, spine_value, spine_value_array
- pyramid: fractal_pyramid_level, fractal_pyramid, fractal_pyramid_to_string, fractal_bridge_analysis
- chain: omega_to_pi_chain, chain_identity_check
- branching: D, H
- constants: PI, OMEGA, D_ID
"""

from .delta import (
    delta_field,
    inverse_delta_field,
)
from .complex_delta import (
    complex_delta_field,
    complex_delta_properties,
    inverse_complex_delta_field,
)
from .complex import (
    complex_branch,
    complex_compress,
    complex_conjugate,
    complex_multiply,
    complex_norm,
    complex_norm_squared,
    complex_rotate,
)
from .dual import (
    dual_add,
    dual_branch,
    dual_compress,
    dual_form,
    dual_func,
    dual_multiply,
    dual_power,
)
from .potential import (
    has_potential,
    is_potential,
    resolve_potential,
)
from .vector import normalize_vector_safe
from .limits import (
    limit_branching,
    limit_compression,
    continuity_D,
    continuity_H,
)
from .percent import (
    from_percentage,
    percentage_add,
    percentage_multiply,
    to_percentage,
)
from .similarity import similarity
from .distance import (
    delta_distance,
    euclidean_distance,
)
from .division import (
    safe_divide,
    div_safe,
)
from .p_adic import (
    v2_adic_valuation,
    p_adic_distance,
    d_adic_convergence,
    p_adic_threshold_spacing,
    bernoulli_shift,
    solenoid_trajectory,
    gcd,
    lcm,
    mod_congruence,
    mod_congruence_branch_invariant,
)
from .fractal_dimension import (
    fractal_dimension_from_betti,
    fractal_dimension_from_multiple_scales,
    compute_betti_scaling_exponent,
    fractal_volume_scaling,
    fractal_similarity_score,
    solenoid_similarity,
    solenoid_distance_from_masks,
)
from .sweep import (
    compute_sweep,
    encode_solenoid_trajectory,
    solenoid_distance,
    rg_aware_sweep,
    inverse_jump_analysis,
    binomial_probability,
    theoretical_occupancy,
)
from .spine import (
    L,
    ridge_level,
    ridge_to_percentage,
    percentage_to_ridge,
    spine_value,
    spine_value_array,
)
from .pyramid import (
    fractal_pyramid_level,
    fractal_pyramid,
    fractal_pyramid_to_string,
    fractal_bridge_analysis,
)
from .chain import (
    omega_to_pi_chain,
    chain_identity_check,
)
from .branching import (
    D,
    H,
)
from .constants import (
    PI,
    OMEGA,
    D_ID,
)

__all__ = [
    # Delta field
    "delta_field",
    "inverse_delta_field",
    # Complex delta (Nucleus)
    "complex_delta_field",
    "complex_delta_properties",
    "inverse_complex_delta_field",
    # Complex (Nucleus)
    "complex_norm",
    "complex_norm_squared",
    "complex_conjugate",
    "complex_multiply",
    "complex_branch",
    "complex_compress",
    "complex_rotate",
    # Dual (Nucleus)
    "dual_form",
    "dual_add",
    "dual_multiply",
    "dual_branch",
    "dual_compress",
    "dual_power",
    "dual_func",
    # Potential
    "has_potential",
    "is_potential",
    "resolve_potential",
    # Vector
    "normalize_vector_safe",
    # Limits
    "limit_branching",
    "limit_compression",
    "continuity_D",
    "continuity_H",
    # Percent
    "to_percentage",
    "from_percentage",
    "percentage_add",
    "percentage_multiply",
    # Similarity
    "similarity",
    # Distance
    "delta_distance",
    "euclidean_distance",
    # Division
    "safe_divide",
    "div_safe",
    # p-adic
    "v2_adic_valuation",
    "p_adic_distance",
    "d_adic_convergence",
    "p_adic_threshold_spacing",
    "bernoulli_shift",
    "solenoid_trajectory",
    "gcd",
    "lcm",
    "mod_congruence",
    "mod_congruence_branch_invariant",
    # Fractal dimension
    "fractal_dimension_from_betti",
    "fractal_dimension_from_multiple_scales",
    "compute_betti_scaling_exponent",
    "fractal_volume_scaling",
    "fractal_similarity_score",
    "solenoid_similarity",
    "solenoid_distance_from_masks",
    # Sweep
    "compute_sweep",
    "encode_solenoid_trajectory",
    "solenoid_distance",
    "rg_aware_sweep",
    "inverse_jump_analysis",
    "binomial_probability",
    "theoretical_occupancy",
    # Spine
    "L",
    "ridge_level",
    "ridge_to_percentage",
    "percentage_to_ridge",
    "spine_value",
    "spine_value_array",
    # Pyramid
    "fractal_pyramid_level",
    "fractal_pyramid",
    "fractal_pyramid_to_string",
    "fractal_bridge_analysis",
    # Chain
    "omega_to_pi_chain",
    "chain_identity_check",
    # Branching
    "D",
    "H",
    # Constants
    "PI",
    "OMEGA",
    "D_ID",
]
