"""Core mathematical operators for Eugenia."""

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
from .D import D
from .H import H
from .L import L
from .binomial_probability import binomial_probability
from .complex_delta_field import complex_delta_field
from .compute_jump_events import compute_jump_events
from .compute_sweep import compute_sweep
from .compute_thresholds import compute_thresholds
from .constants import D_ID, EPS
from .delta_distance import delta_distance
from .delta_field import delta_field
from .euclidean_distance import euclidean_distance
from .fractal_pattern_signature import fractal_pattern_signature
from .fractal_pyramid_structure import fractal_pyramid_structure
from .has_potential import has_potential
from .is_potential import is_potential
from .log2 import log2
from .normalize_vector_safe import normalize_vector_safe
from .p_adic_distance import p_adic_distance
from .pattern_bridge_identity import pattern_bridge_identity
from .pattern_distance_from_delta import pattern_distance_from_delta
from .pattern_pyramid_depth import pattern_pyramid_depth
from .pattern_similarity_from_complex import pattern_similarity_from_complex
from .pattern_similarity_from_delta import pattern_similarity_from_delta
from .pattern_spine_chain import pattern_spine_chain
from .resolve_potential import resolve_potential
from .safe_divide import safe_divide
from .solenoid_distance import solenoid_distance
from .solenoid_encode_pattern import solenoid_encode_pattern
from .solenoid_pattern_distance import solenoid_pattern_distance
from .sweep_results import SweepResults

PI = float("inf")
OMEGA = 0.0

div_safe = safe_divide

__all__ = [
    "D",
    "D_ID",
    "EPS",
    "H",
    "L",
    "OMEGA",
    "PI",
    "SweepResults",
    "binomial_probability",
    "complex_delta_field",
    "compute_jump_events",
    "compute_sweep",
    "compute_thresholds",
    "delta_distance",
    "delta_field",
    "div_safe",
    "euclidean_distance",
    "fractal_pattern_signature",
    "fractal_pyramid_structure",
    "has_potential",
    "is_potential",
    "log2",
    "normalize_vector_safe",
    "p_adic_distance",
    "pattern_bridge_identity",
    "pattern_distance_from_delta",
    "pattern_pyramid_depth",
    "pattern_similarity_from_complex",
    "pattern_similarity_from_delta",
    "pattern_spine_chain",
    "resolve_potential",
    "safe_divide",
    "solenoid_distance",
    "solenoid_encode_pattern",
    "solenoid_pattern_distance",
]
