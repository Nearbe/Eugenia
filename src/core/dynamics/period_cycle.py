from __future__ import annotations

from .dynamic_step import DynamicStep
from .orbit import Orbit
from .orbit_function import orbit

DEFAULT_PERIODS = 1


def period_cycle(seed: object, *, periods: int = DEFAULT_PERIODS) -> Orbit:
    """Return repeated ``D → H`` periods."""
    if periods < 0:
        raise ValueError("periods must be non-negative")
    return orbit(seed, (DynamicStep.BRANCH, DynamicStep.COMPRESS) * periods)
