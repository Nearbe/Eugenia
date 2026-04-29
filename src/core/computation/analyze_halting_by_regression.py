from __future__ import annotations

from collections.abc import Callable, Iterable

from .computability_state import ComputabilityState
from .interaction_result import InteractionResult
from .reverse_reachable_states import reverse_reachable_states
from .connectivity_path import connectivity_path
from .state import State


def analyze_halting_by_regression(
    start: State,
    stop: State,
    predecessors: Callable[[State], Iterable[State]],
    *,
    max_depth: int,
) -> InteractionResult:
    """Analyze stopping by asking where STOP could have come from."""
    frontier = reverse_reachable_states(stop, predecessors, max_depth=max_depth)
    path = connectivity_path(start, stop, predecessors, max_depth=max_depth)
    state = ComputabilityState.HALTS if path else ComputabilityState.CYCLES
    return InteractionResult(state, frontier, path)
