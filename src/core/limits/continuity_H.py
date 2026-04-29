from core.algebra import compress
from .continuity_error import continuity_error


def continuity_H(sequence: list[float]) -> float:
    """Return continuity error for compression H."""
    if not sequence:
        return 0.0
    return continuity_error(compress, sequence, sequence[-1])
