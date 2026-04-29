from __future__ import annotations

from collections.abc import Callable, Iterable


def select_stable(variants: Iterable[object], stability: Callable[[object], float]) -> object:
    """Select the most stable variant; no randomness, only evaluation."""
    iterator = iter(variants)
    try:
        selected = next(iterator)
    except StopIteration as error:
        raise ValueError("evolution requires at least one variant") from error
    selected_score = float(stability(selected))
    for variant in iterator:
        score = float(stability(variant))
        if score > selected_score:
            selected = variant
            selected_score = score
    return selected
