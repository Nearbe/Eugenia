"""Computability through interaction from Universe/Math/20–21."""

#  Copyright (c) 2026.
#  ╔═══════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═══════════════════════════════════╝
from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeVar

from ..foundations.u_algebra import branch, compress

State = TypeVar("State")
START_NODE = "START"
STOP_NODE = "STOP"


class ComputabilityState(StrEnum):
    """Reachability state under recursion/regression interaction."""

    HALTS = "halts"
    CYCLES = "cycles"


@dataclass(frozen=True)
class InteractionResult:
    """Result of reverse connectivity analysis from STOP to START."""

    state: ComputabilityState
    regression_frontier: tuple[object, ...]
    path: tuple[object, ...]

    @property
    def halts(self) -> bool:
        """Return true when START is connected to STOP."""
        return self.state == ComputabilityState.HALTS


def recursive_step(state: object) -> object:
    """Universe recursion: ``Ψₙ₊₁ = D(Ψₙ)``."""
    return branch(state)


def regressive_step(state: object) -> object:
    """Mind regression: ``Ψₙ₋₁ = H(Ψₙ)``."""
    return compress(state)


def interaction_cycle(state: object) -> object:
    """Return ``H(D(state))`` — the information-preserving U-cycle."""
    return regressive_step(recursive_step(state))


def reverse_reachable_states(
    stop: State,
    predecessors: Callable[[State], Iterable[State]],
    *,
    max_depth: int,
) -> tuple[State, ...]:
    """Return all states visible by regressing from STOP."""
    if max_depth < 0:
        raise ValueError("max_depth must be non-negative")
    visited: set[State] = {stop}
    queue: deque[tuple[State, int]] = deque([(stop, 0)])

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
    parent: dict[State, State | None] = {stop: None}
    queue: deque[tuple[State, int]] = deque([(stop, 0)])

    while queue:
        current, depth = queue.popleft()
        if current == start:
            path: list[State] = []
            cursor: State | None = current
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
