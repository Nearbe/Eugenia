from __future__ import annotations

from .dynamic_step import DynamicStep
from .orbit import Orbit
from .orbit_function import orbit


def oscillation(seed: object) -> Orbit:
    """Return elementary cycle ``D → H``."""
    return orbit(seed, (DynamicStep.BRANCH, DynamicStep.COMPRESS))
