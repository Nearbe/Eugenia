from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable

from .state import State


def reverse_reachable_states(
    stop: State,
    predecessors: Callable[[State], Iterable[State]],
    *,
    max_depth: int,
) -> tuple[State, ...]:
    """Return all states visible by regressing from STOP."""
    if max_depth < 0:
        raise ValueError("max_depth must be non-negative")
    visited: set["State"] = {stop}
    queue: deque[tuple["State", int]] = deque([(stop, 0)])

    while queue:
        current, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for previous in predecessors(current):
            if previous in visited:
                continue
            visited.add(previous)
            queue.append((previous, depth + 1))
    return tuple(visited)
