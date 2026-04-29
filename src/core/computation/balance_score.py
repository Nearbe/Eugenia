from __future__ import annotations

from .balance_delta import balance_delta

PERFECT_RESONANCE = 1.0
MIN_RESONANCE = 0.0


def balance_score(*, recursion: object, regression: object) -> float:
    """Return ``S``: one at balance, lower as recursion/regression diverge."""
    strongest = max(abs(float(recursion)), abs(float(regression)), PERFECT_RESONANCE)
    return max(
        MIN_RESONANCE,
        PERFECT_RESONANCE - balance_delta(recursion=recursion, regression=regression) / strongest,
    )
