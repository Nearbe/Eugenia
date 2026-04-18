"""
Operators module — compatibility shim.

Все функции перемещены в специализированные модули:
- potential: has_potential, is_potential, resolve_potential
- vector: normalize_vector_safe
- dual: dual_form, dual_multiply, dual_branch, dual_compress
- complex: complex_norm, complex_conjugate, complex_multiply
- limits: limit_branching, limit_compression
- percent: to_percentage (для branching_cosine)
- branching: D, H (для dual_branch, dual_compress)
- constants: D_ID, OMEGA, PI (для limit_branching, limit_compression)
"""

from .complex import (
    complex_conjugate,
    complex_multiply,
    complex_norm,
)
from .dual import (
    dual_branch,
    dual_compress,
    dual_form,
    dual_multiply,
)
from .limits import (
    limit_branching,
    limit_compression,
)
from .potential import (
    has_potential,
    is_potential,
    resolve_potential,
)
from .vector import normalize_vector_safe

__all__ = [
    "has_potential",
    "is_potential",
    "resolve_potential",
    "normalize_vector_safe",
    "dual_form",
    "dual_multiply",
    "dual_branch",
    "dual_compress",
    "complex_norm",
    "complex_conjugate",
    "complex_multiply",
    "limit_branching",
    "limit_compression",
]
