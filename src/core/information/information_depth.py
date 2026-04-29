from __future__ import annotations
from dataclasses import dataclass
from .. import OMEGA, PI, branch, compress, is_omega
from ..utils.logarithmic_axis import LOG_POSITIVE_INFINITY
from ..states.spine import spine_level, SpineLevel


def information(value: object) -> object:
    """Return information depth of a state."""
    if value == PI:
        return LOG_POSITIVE_INFINITY
    if isinstance(value, SpineLevel):
        return float(value.depth)
    if is_omega(value):
        return OMEGA
    return 0.0


def mass_from_information(info: object) -> object:
    """Return mass (spine level) from information depth."""
    if info == LOG_POSITIVE_INFINITY:
        return PI
    if info == OMEGA:
        return spine_level(0)
    return spine_level(int(float(info)))


def branch_information(value: object) -> float:
    """Return information depth of branched state."""
    return float(information(branch(value)))


def compress_information(value: object) -> float:
    """Return information depth of compressed state."""
    return float(information(compress(value)))


@dataclass(frozen=True)
class AddressState:
    """Information state with address and depth."""

    address: tuple[int, ...]
    information: float


def address_state(value: int, depth: int) -> AddressState:
    """Construct an address state from integer value."""
    address = tuple(int(x) for x in f"{value:0{depth}b}")
    return AddressState(address, float(depth))


def address_cost(address: tuple) -> int:
    """Return bit-length cost of an address."""
    return len(address)


def branching_level_information(level: object) -> float:
    """Return information capacity of a branching level."""
    return float(getattr(level, "depth", 0.0))


def choice_capacity(depth: int) -> int:
    """Return number of possible choices at a given depth."""
    return 2**depth
