from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable

from .state import State


def connectivity_path(
    start: State,
    stop: State,
    predecessors: Callable[[State], Iterable[State]],
    *,
    max_depth: int,
) -> tuple[State, ...]:
    """Return reverse path ``STOP → ... → START`` when it exists."""
    if max_depth < 0:
        raise ValueError("max_depth must be non-negative")
    parent: dict["State", "State" | None] = {stop: None}
    queue: deque[tuple["State", int]] = deque([(stop, 0)])

    while queue:
        current, depth = queue.popleft()
        if current == start:
            path: list["State"] = []
            cursor: "State" | None = current
            while cursor is not None:
                path.append(cursor)
                cursor = parent[cursor]
            return tuple(reversed(path))
        if depth >= max_depth:
            continue
        for previous in predecessors(current):
            if previous in parent:
                continue
            parent[previous] = current
            queue.append((previous, depth + 1))
    return ()
