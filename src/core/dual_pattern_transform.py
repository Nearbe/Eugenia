"""
dual_pattern_transform — Дуальное преобразование паттерна.

Z = x + v·ε where:
    - x = current pattern values (Form / Явное)
    - v = derivative/potential (Growth potential / Скрытое)
    - ε² = Ω (acceleration is negligible)

This captures both the current state AND the potential for change,
enabling more sophisticated pattern matching in the Nucleus system.
"""

from .dual import dual_form


def dual_pattern_transform(
    values: list[float],
    derivative: list[float],
) -> tuple[list[float], list[float]]:
    """
    Apply dual number transformation to a pattern.

    Args:
        values: Current pattern values.
        derivative: Derivative/growth potential values.

    Returns:
        Tuple (form, velocity) representing the dual number Z.
    """
    form, velocity = dual_form(values, derivative)

    if isinstance(form, float):
        form = [form]
    if isinstance(velocity, float):
        velocity = [velocity]
    return form, velocity
