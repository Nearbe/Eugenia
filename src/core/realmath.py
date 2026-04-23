"""
RealMath Bridge — Unified interface for Nucleus integration.

This module provides a clean, single-import interface that connects
the RealMath / Essentials mathematical operators (src/core/) to the
Nucleus deterministic knowledge system (src/nucleus/).

Architecture:

    src/core/ (RealMath operators)          src/nucleus/ (Knowledge system)
    ┌─────────────────────────┐            ┌──────────────────────────┐
    │ delta_field             │───────────►│ GeometricExtractor       │
    │ complex_delta_field     │───────────►│ DeterministicKnowledge   │
    │ dual_form, dual_multiply│───────────►│ UniversalKnowledgeMap    │
    │ D(), H()                │───────────►│ CorrelationEngine        │
    │ p_adic_distance         │───────────►│ KnowledgeGraph           │
    │ similarity              │───────────►│ PatternNode              │
    │ solenoid_trajectory     │───────────►│ Seed / Explorer          │
    │ fractal_dimension       │───────────►│ GeometricExtractor       │
    │ spine_value, ridge_level│───────────►│ KnowledgeSystem          │
    └─────────────────────────┘            └──────────────────────────┘

All core operators are re-exported for convenience. The primary purpose
is to provide:

1. Unified imports (one import instead of 20+)
2. Nucleus-specific convenience functions (pattern_similarity, etc.)
3. Solenoid-based pattern encoding utilities
4. Delta-field-aware pattern extraction helpers

Mathematical Foundation (Essentials):
-------------------------------------
- D(a) = branching: D(a) = a * 2 (creates distinction)
- H(a) = compression: H(a) = a / 2 (removes noise)
- H(D(a)) = a = D(H(a)) — lossless cycle
- Ω = 0 (potential), Π = ∞ (completeness)
- D(Id) = 2 (first branching)
- L(x) = log2(|x|) — spine level / branching depth
"""

# ============================================================
# Re-exports: All core operators available via single import
# ============================================================

from .branching import D, H
from .chain import (
    chain_identity_check,
    omega_to_pi_chain,
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
from .complex_delta import (
    complex_delta_field,
    complex_delta_properties,
    inverse_complex_delta_field,
)
from .constants import D_ID, OMEGA, PI
from .delta import delta_field, inverse_delta_field
from .distance import delta_distance, euclidean_distance
from .division import div_safe, safe_divide
from .dual import (
    dual_add,
    dual_branch,
    dual_compress,
    dual_form,
    dual_func,
    dual_multiply,
    dual_power,
)
from .fractal_dimension import (
    compute_betti_scaling_exponent,
    fractal_dimension_from_betti,
    fractal_dimension_from_multiple_scales,
    fractal_similarity_score,
    fractal_volume_scaling,
    solenoid_distance_from_masks,
    solenoid_similarity,
)
from .limits import (
    continuity_D,
    continuity_H,
    limit_branching,
    limit_compression,
)
from .p_adic import (
    bernoulli_shift,
    d_adic_convergence,
    gcd,
    lcm,
    mod_congruence,
    mod_congruence_branch_invariant,
    p_adic_distance,
    p_adic_threshold_spacing,
    solenoid_trajectory,
    v2_adic_valuation,
)
from .percent import (
    from_percentage,
    percentage_add,
    percentage_multiply,
    to_percentage,
)
from .potential import has_potential, is_potential, resolve_potential
from .pyramid import (
    fractal_bridge_analysis,
    fractal_pyramid,
    fractal_pyramid_level,
    fractal_pyramid_to_string,
)
from .similarity import similarity
from .spine import (
    L,
    percentage_to_ridge,
    ridge_level,
    ridge_to_percentage,
    spine_value,
    spine_value_array,
)
from .sweep import (
    binomial_probability,
    compute_sweep,
    encode_solenoid_trajectory,
    inverse_jump_analysis,
    rg_aware_sweep,
    solenoid_distance,
    theoretical_occupancy,
)
from .svd import svd, svd_reconstruct, svd_error
from .vector import normalize_vector_safe


__all__ = [
    # Branching / Compression
    "D",
    "H",
    # Chain
    "omega_to_pi_chain",
    "chain_identity_check",
    # Complex
    "complex_norm",
    "complex_norm_squared",
    "complex_conjugate",
    "complex_multiply",
    "complex_branch",
    "complex_compress",
    "complex_rotate",
    # Complex delta
    "complex_delta_field",
    "complex_delta_properties",
    "inverse_complex_delta_field",
    # Constants
    "PI",
    "OMEGA",
    "D_ID",
    # Delta field
    "delta_field",
    "inverse_delta_field",
    # Distance
    "delta_distance",
    "euclidean_distance",
    # Division
    "safe_divide",
    "div_safe",
    # Dual numbers
    "dual_form",
    "dual_add",
    "dual_multiply",
    "dual_branch",
    "dual_compress",
    "dual_power",
    "dual_func",
    # Fractal dimension
    "fractal_dimension_from_betti",
    "fractal_dimension_from_multiple_scales",
    "compute_betti_scaling_exponent",
    "fractal_volume_scaling",
    "fractal_similarity_score",
    "solenoid_similarity",
    "solenoid_distance_from_masks",
    # Limits
    "limit_branching",
    "limit_compression",
    "continuity_D",
    "continuity_H",
    # Percentage / Fraction algebra
    "to_percentage",
    "from_percentage",
    "percentage_add",
    "percentage_multiply",
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
    # Potential
    "has_potential",
    "is_potential",
    "resolve_potential",
    # Pyramid
    "fractal_pyramid_level",
    "fractal_pyramid",
    "fractal_pyramid_to_string",
    "fractal_bridge_analysis",
    # Similarity
    "similarity",
    # Spine
    "L",
    "ridge_level",
    "ridge_to_percentage",
    "percentage_to_ridge",
    "spine_value",
    "spine_value_array",
    # Sweep
    "compute_sweep",
    "encode_solenoid_trajectory",
    "solenoid_distance",
    "rg_aware_sweep",
    "inverse_jump_analysis",
    "binomial_probability",
    "theoretical_occupancy",
    # Vector
    "normalize_vector_safe",
    # SVD — запись, не оптимизация
    "svd",
    "svd_reconstruct",
    "svd_error",
]
