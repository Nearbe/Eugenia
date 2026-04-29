"""Nucleus seed system based on direct Lo Shu addressing.

Hash/random seeds are intentionally absent: the first address comes from
Lo Shu, then unfolds into solenoid history.
"""

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

from core.foundations.lo_shu import (
    LoShuAddress,
    LoShuOperation,
    address_path,
    digit_address,
    operation_address,
)
from core.fractal.solenoid_point import SolenoidPoint, solenoid_seed_from_lo_shu
from core.linear.linear_algebra import CoreVector


@dataclass(frozen=True)
class NucleusSeed:
    """Deterministic nucleus address unfolded from Lo Shu."""

    key: str
    lo_shu_addresses: tuple[LoShuAddress, ...]
    solenoid: SolenoidPoint

    @property
    def vector(self) -> CoreVector:
        """Raw Lo Shu path vector; weights are not normalized."""
        return CoreVector(float(bit) for bit in address_path(self.lo_shu_addresses))


def _address_token(token: str) -> LoShuAddress:
    if token.isdigit():
        digit = int(token) % 10
        return digit_address(5 if digit == 0 else digit)
    if token in {operation.value for operation in LoShuOperation}:
        return operation_address(token)
    code = sum(ord(char) for char in token)
    digit = code % 10
    return digit_address(5 if digit == 0 else digit)


def _tokenize(value: object) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value)
    text = str(value)
    return tuple(text) if text else ("Id",)


def lo_shu_seed_from_tokens(tokens: list[str] | tuple[str, ...]) -> NucleusSeed:
    """Build a nucleus seed from explicit digits/operations/text tokens."""
    token_tuple = tuple(tokens)
    addresses = tuple(_address_token(token) for token in token_tuple) or (digit_address(5),)
    head = solenoid_seed_from_lo_shu(addresses[0])
    history = address_path(addresses)
    solenoid = SolenoidPoint(phase=head.phase, history=history)
    key = "|".join(token_tuple) if token_tuple else "Id"
    return NucleusSeed(key=key, lo_shu_addresses=addresses, solenoid=solenoid)


def deterministic_vector(value: object, *, size: int = 32) -> CoreVector:
    """Return deterministic raw Lo Shu address bits for compatibility."""
    seed = lo_shu_seed_from_tokens(_tokenize(value))
    bits = list(seed.vector)
    if not bits:
        bits = [0.0]
    while len(bits) < size:
        bits.extend(bits)
    return CoreVector(bits[:size])


__all__ = [
    "NucleusSeed",
    "deterministic_vector",
    "lo_shu_seed_from_tokens",
]
