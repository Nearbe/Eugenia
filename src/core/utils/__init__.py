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
"""Utilities: Lo Shu, logarithmic axis, safe division, vectorization."""

from .lo_shu import (
    LO_SHU_SIZE,
    GRID,
    LO_SHU_CENTER_VALUE,
    LO_SHU_DECIMAL_CYCLE,
    LO_SHU_MAGIC_SUM,
    Direction,
    LoShuAddress,
    LoShuOperation,
    LoShuPosition,
    POSITION_BY_DIGIT,
    POSITION_BY_DIRECTION,
    address_path,
    base_number,
    columns,
    context_number,
    cpu_gpu_balance,
    diagonals,
    digit_address,
    digit_position,
    direction_position,
    equation_sums,
    equations,
    layer_count,
    operation_address,
    operation_digit,
    rows,
    scale_number,
)
from .logarithmic_axis import (
    LogInfinity,
    POSITIVE_DIRECTION,
    NEGATIVE_DIRECTION,
    ZERO_DEPTH,
    is_log_infinity,
    depth_add,
    depth_scale,
)
from .safe_divide import safe_divide
from .vectorization import (
    is_scalar,
    is_vector,
    to_scalar,
    to_vector,
    map_scalar_or_vector,
    zip_vectors,
    vector_delta,
    last_or_default,
    ScalarResult,
    VectorizedResult,
)

__all__ = [
    "LO_SHU_SIZE",
    "GRID",
    "LO_SHU_CENTER_VALUE",
    "LO_SHU_DECIMAL_CYCLE",
    "LO_SHU_MAGIC_SUM",
    "Direction",
    "LoShuAddress",
    "LoShuOperation",
    "LoShuPosition",
    "POSITION_BY_DIGIT",
    "POSITION_BY_DIRECTION",
    "address_path",
    "base_number",
    "columns",
    "context_number",
    "cpu_gpu_balance",
    "diagonals",
    "digit_address",
    "digit_position",
    "direction_position",
    "equation_sums",
    "equations",
    "layer_count",
    "operation_address",
    "operation_digit",
    "rows",
    "scale_number",
    "LogInfinity",
    "POSITIVE_DIRECTION",
    "NEGATIVE_DIRECTION",
    "ZERO_DEPTH",
    "is_log_infinity",
    "depth_add",
    "depth_scale",
    "safe_divide",
    "is_scalar",
    "is_vector",
    "to_scalar",
    "to_vector",
    "map_scalar_or_vector",
    "zip_vectors",
    "vector_delta",
    "last_or_default",
    "ScalarResult",
    "VectorizedResult",
]
