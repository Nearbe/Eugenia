"""
pattern_spine_chain — Ω→Π цепь паттерна.

This chain shows the relationship between the spine and fraction algebra:
    - 0 = Ω (potential)
    - 1 = Id (unity)
    - 2 = D(Id) (first branching)
    - ∞ = Π (completeness)
    - 100% = Π (in percentages)
"""

from .chain import omega_to_pi_chain


def pattern_spine_chain(n_steps: int = 10) -> list[dict]:
    """
    Generate the Ω → Id → D(Id) → ... → Π chain for a pattern.

    Args:
        n_steps: Number of branching steps.

    Returns:
        List of dicts with step, symbol, value, spine_level, percentage.
    """
    return omega_to_pi_chain(n_steps)
