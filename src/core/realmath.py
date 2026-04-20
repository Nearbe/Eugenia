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
from .vector import normalize_vector_safe

# ============================================================
# Nucleus-specific convenience functions
# ============================================================


def pattern_similarity_from_delta(
    values_a: list[float],
    values_b: list[float],
) -> float:
    """
    Compute similarity between two data series using delta field transformation.

    Pipeline:
        1. Transform raw values through delta_field: X → log2(X+1) - log2(256-X)
        2. Compute cosine similarity in delta-space (RealMath-aware)

    This is more robust than raw cosine similarity because the delta field
    maps pixel intensities to a logarithmic spine scale where branching
    structure is preserved (Essentials [08_Логарифм.md], [22_Геометрия.md]).

    Args:
        values_a: First data series (pixel values 0-255 or normalized).
        values_b: Second data series (pixel values 0-255 or normalized).

    Returns:
        Cosine similarity in delta-space ∈ [-1, 1].
    """
    if not values_a or not values_b:
        return 0.0

    # Transform through delta field
    delta_a = delta_field(values_a)
    delta_b = delta_field(values_b)

    # Ensure list form for iteration
    if isinstance(delta_a, float):
        delta_a = [delta_a]
    if isinstance(delta_b, float):
        delta_b = [delta_b]

    # Cosine similarity in delta-space
    norm_a = sum(x**2 for x in delta_a) ** 0.5
    norm_b = sum(x**2 for x in delta_b) ** 0.5

    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0

    dot = sum(x * y for x, y in zip(delta_a, delta_b))
    return dot / (norm_a * norm_b)


def pattern_similarity_from_complex(
    values_a: list[float],
    values_b: list[float],
) -> float:
    """
    Compute similarity between two data series using complex delta field.

    Pipeline:
        1. Transform through complex_delta_field: X → complex(x, 1-x)
        2. Compute norm-based similarity in complex space

    This captures both magnitude AND phase information of the data,
    providing richer pattern comparison than real-valued delta_field alone.

    Args:
        values_a: First data series.
        values_b: Second data series.

    Returns:
        Cosine similarity in complex delta-space ∈ [-1, 1].
    """
    if not values_a or not values_b:
        return 0.0

    # Transform through complex delta field
    complex_a = complex_delta_field(values_a)
    complex_b = complex_delta_field(values_b)

    # Ensure list form for iteration
    if isinstance(complex_a, complex):
        complex_a = [complex_a]
    if isinstance(complex_b, complex):
        complex_b = [complex_b]

    # Extract real and imaginary parts
    real_a = [c.real for c in complex_a]
    imag_a = [c.imag for c in complex_a]
    real_b = [c.real for c in complex_b]
    imag_b = [c.imag for c in complex_b]

    # Cosine similarity in complex space
    norm_a = (sum(r**2 + i**2 for r, i in zip(real_a, imag_a))) ** 0.5
    norm_b = (sum(r**2 + i**2 for r, i in zip(real_b, imag_b))) ** 0.5

    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0

    dot = sum(r1 * r2 + i1 * i2 for r1, i1, r2, i2 in zip(real_a, imag_a, real_b, imag_b))
    return dot / (norm_a * norm_b)


def pattern_distance_from_delta(
    values_a: list[float],
    values_b: list[float],
) -> float:
    """
    Compute delta-aware distance between two data series.

    Uses delta_distance on the spine levels of the delta field values,
    which respects the branching structure of the data.

    Args:
        values_a: First data series.
        values_b: Second data series.

    Returns:
        Distance on the logarithmic spine scale.
    """
    if not values_a or not values_b:
        return float("inf")

    delta_a = delta_field(values_a)
    delta_b = delta_field(values_b)
    dist = delta_distance(delta_a, delta_b)
    # Ensure scalar return
    if isinstance(dist, list):
        return sum(dist) / len(dist) if dist else 0.0
    return dist


def solenoid_encode_pattern(values: list[float], depth: int = 30) -> list[int]:
    """
    Encode a data pattern as a solenoid trajectory.

    Per Essentials [23_Соленоид.md]:
    Each point on the solenoid is the full branching history:
    z₀ = D(z₁) = D²(z₂) = ... = Dⁿ(zₙ)

    Encoded as binary fraction: ξ = 0.ε₀ε₁ε₂… where εₙ ∈ {0, 1}

    This provides a lossless, deterministic encoding of the pattern
    that preserves branching structure and enables queryable storage.

    Args:
        values: Data values to encode.
        depth: Number of bits in the binary representation.

    Returns:
        Binary trajectory [ε₀, ε₁, ..., εₙ₋₁].
    """
    # Average the values to get a representative point
    avg = sum(values) / len(values) if values else 0.0
    return encode_solenoid_trajectory(avg, depth)


def solenoid_pattern_distance(
    values_a: list[float],
    values_b: list[float],
    depth: int = 30,
) -> float:
    """
    Compute solenoid distance between two data patterns.

    Per Essentials [23_Соленоид.md, XI. Метрика Близости]:
    Two points are close if their binary histories match on many
    initial steps. If histories diverge early — points are far,
    even if current values are close.
    "Происхождение важнее текущего вида."

    Args:
        values_a: First data pattern.
        values_b: Second data pattern.
        depth: Bit depth for encoding.

    Returns:
        Closeness: 2^(-k) where k is the first differing bit.
    """
    traj_a = solenoid_encode_pattern(values_a, depth)
    traj_b = solenoid_encode_pattern(values_b, depth)
    return solenoid_distance(traj_a, traj_b)


def fractal_pattern_signature(
    values: list[float],
    n_thresholds: int = 64,
) -> dict:
    """
    Compute a fractal pattern signature for a data series.

    Combines:
    1. Binary sweep profile (64 thresholds)
    2. Jump events (topological changes)
    3. Fractal dimension (Betti scaling)
    4. Spine levels (ridge mapping)

    This signature is used by GeometricExtractor to create
    deterministic pattern vectors for the KnowledgeGraph.

    Args:
        values: Data values (pixel intensities, normalized data, etc.).
        n_thresholds: Number of sweep thresholds.

    Returns:
        Dictionary with fractal signature components.
    """
    # Binary sweep
    thresholds = [i / n_thresholds for i in range(n_thresholds + 1)]
    binary_profile = [float(v > t) for v in values for t in thresholds]

    # Aggregate profile
    profile = []
    bin_size = len(values)
    for i in range(n_thresholds + 1):
        start = i * bin_size
        end = start + bin_size
        profile.append(sum(binary_profile[start:end]) / bin_size)

    # Jump events
    jumps = [abs(profile[i + 1] - profile[i]) for i in range(len(profile) - 1)]
    top_jumps = sorted(jumps, reverse=True)[:5]

    # Fractal dimension estimate
    betti_values = [max(1, int(p * len(values))) for p in profile]
    try:
        fd = fractal_dimension_from_betti(betti_values, thresholds, reference_threshold=0.5)
    except (ValueError, ZeroDivisionError):
        fd = 0.0

    # Spine levels
    avg_val = sum(values) / len(values) if values else 0.0
    spine_lvl = ridge_level(avg_val)

    return {
        "profile": profile,
        "top_jumps": top_jumps,
        "fractal_dimension": fd,
        "spine_level": spine_lvl,
        "percentage": ridge_to_percentage(spine_lvl),
        "avg_value": avg_val,
        "delta_value": delta_field(avg_val) if values else 0.0,
    }


def dual_pattern_transform(
    values: list[float],
    derivative: list[float],
) -> tuple[list[float], list[float]]:
    """
    Apply dual number transformation to a pattern.

    Z = x + v·ε where:
    - x = current pattern values (Form / Явное)
    - v = derivative/potential (Growth potential / Скрытое)
    - ε² = Ω (acceleration is negligible)

    This captures both the current state AND the potential for change,
    enabling more sophisticated pattern matching in the Nucleus system.

    Args:
        values: Current pattern values.
        derivative: Derivative/growth potential values.

    Returns:
        Tuple (form, velocity) representing the dual number Z.
    """
    form, velocity = dual_form(values, derivative)
    # Ensure list form
    if isinstance(form, float):
        form = [form]
    if isinstance(velocity, float):
        velocity = [velocity]
    return form, velocity


# ============================================================
# Nucleus convenience functions: Pyramid & Chain
# ============================================================


def fractal_pyramid_structure(max_level: int = 10) -> list[dict]:
    """
    Generate fractal pyramid structure as analysis-ready dicts.

    Per Essentials: the pyramid has Ω (0) at the center of each level,
    with branching (right: 1, 2, 3, ...) and compression (left: 3, 2, 1)
    forming a bridge through potential.

    This is useful for:
    - Analyzing the branching/compression balance in a pattern
    - Visualizing the Ω → Π evolution of a knowledge structure
    - Computing the bridge identity for pattern validation

    Args:
        max_level: Maximum pyramid level.

    Returns:
        List of dicts with level, left, center, right, and analysis.
    """
    pyramid = []
    for level in range(1, max_level + 1):
        left, center, right = fractal_pyramid_level(level)
        bridge = fractal_bridge_analysis(level)
        pyramid.append(
            {
                "level": level,
                "left": left,
                "center": center,
                "right": right,
                "bridge_analysis": bridge,
            }
        )
    return pyramid


def pattern_spine_chain(n_steps: int = 10) -> list[dict]:
    """
    Generate the Ω → Id → D(Id) → ... → Π chain for a pattern.

    This chain shows the relationship between the spine and fraction algebra:
    - 0 = Ω (potential)
    - 1 = Id (unity)
    - 2 = D(Id) (first branching)
    - ∞ = Π (completeness)
    - 100% = Π (in percentages)

    Useful for:
    - Understanding the branching depth of a pattern
    - Mapping pattern values to their spine levels
    - Computing percentage-of-completeness for any value

    Args:
        n_steps: Number of branching steps.

    Returns:
        List of dicts with step, symbol, value, spine_level, percentage.
    """
    return omega_to_pi_chain(n_steps)


def pattern_pyramid_depth(value: float) -> int:
    """
    Compute the fractal pyramid depth for a given value.

    Maps a value to its spine level (ridge_level), which corresponds
    to the pyramid level at which this value first appears.

    Per Essentials: ridge_level(x) = log2(|x|) = branching depth.

    Args:
        value: A numeric value.

    Returns:
        Pyramid level (spine level) for the value.
    """
    lvl = ridge_level(value)
    if isinstance(lvl, list):
        lvl = lvl[0] if lvl else 0
    return int(lvl)


def pattern_bridge_identity(value: float) -> dict:
    """
    Check the bridge identity for a value through Ω.

    For a value v at pyramid level n:
    - left: reverse sequence (n-1, n-2, ..., 1) → compression H
    - right: forward sequence (1, 2, ..., n-1) → branching D
    - center: 0 = Ω (bridge, not barrier)

    Identity: left:Ω:right = Id (through potential, not division)

    Args:
        value: A numeric value to analyze.

    Returns:
        Bridge analysis dict with identity check results.
    """
    depth = pattern_pyramid_depth(value)
    return fractal_bridge_analysis(max(depth, 1))


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
    # Nucleus convenience functions
    "pattern_similarity_from_delta",
    "pattern_similarity_from_complex",
    "pattern_distance_from_delta",
    "solenoid_encode_pattern",
    "solenoid_pattern_distance",
    "fractal_pattern_signature",
    "dual_pattern_transform",
    "fractal_pyramid_structure",
    "pattern_spine_chain",
    "pattern_pyramid_depth",
    "pattern_bridge_identity",
]
