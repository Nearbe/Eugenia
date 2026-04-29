from __future__ import annotations

from enum import StrEnum


class ComputabilityState(StrEnum):
    """Reachability state under recursion/regression interaction."""

    HALTS = "halts"
    CYCLES = "cycles"
