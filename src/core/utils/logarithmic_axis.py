"""Logarithmic axis values from Universe/Math/08_Логарифм.md."""

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

from dataclasses import dataclass
from typing import Final

POSITIVE_DIRECTION: Final[int] = 1
NEGATIVE_DIRECTION: Final[int] = -1
ZERO_DEPTH: Final[float] = 0.0


@dataclass(frozen=True)
class LogInfinity:
    """Signed algebraic infinity on the logarithmic depth axis."""

    direction: int
    symbol: str

    def __post_init__(self) -> None:
        if self.direction not in (NEGATIVE_DIRECTION, POSITIVE_DIRECTION):
            raise ValueError("log infinity direction must be -1 or +1")

    def __neg__(self) -> LogInfinity:
        if self.direction == POSITIVE_DIRECTION:
            return LOG_NEGATIVE_INFINITY
        return LOG_POSITIVE_INFINITY

    def __repr__(self) -> str:
        return self.symbol

    def __str__(self) -> str:
        return self.symbol


LOG_POSITIVE_INFINITY: Final[LogInfinity] = LogInfinity(POSITIVE_DIRECTION, "+∞")
LOG_NEGATIVE_INFINITY: Final[LogInfinity] = LogInfinity(NEGATIVE_DIRECTION, "-∞")


def is_log_infinity(value: object) -> bool:
    """Return True when ``value`` is an algebraic depth infinity."""
    return isinstance(value, LogInfinity)


def depth_add(left: object, right: object) -> object:
    """Add two logarithmic depths with closed same-direction infinities."""
    if is_log_infinity(left) and is_log_infinity(right):
        if left == right:
            return left
        raise ValueError("opposite logarithmic infinities cannot be added directly")
    if is_log_infinity(left):
        return left
    if is_log_infinity(right):
        return right
    return float(left) + float(right)


def depth_scale(depth: object, scale: object) -> object:
    """Scale a logarithmic depth, flipping infinity when scale is negative."""
    scale_value = float(scale)
    if scale_value == ZERO_DEPTH:
        return ZERO_DEPTH
    if is_log_infinity(depth):
        if scale_value < ZERO_DEPTH:
            return -depth
        return depth
    return float(depth) * scale_value
