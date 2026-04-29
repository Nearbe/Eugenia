from __future__ import annotations

from ..algebra import branch, compress
from .dynamic_step import DynamicStep


def apply_step(value: object, step: DynamicStep | str) -> object:
    """Apply one dynamic operator."""
    dynamic_step = DynamicStep(step)
    if dynamic_step == DynamicStep.BRANCH:
        return branch(value)
    return compress(value)
