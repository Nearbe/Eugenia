"""Function classes from Universe/Math/16_Функции.md."""

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

from collections.abc import Callable
from dataclasses import dataclass

from .complex_plane import ComplexState
from .u_algebra import add, branch, compress, multiply, power


def _finite(value: object) -> float:
    """Normalize a finite scalar for function parameters."""
    return float(value)


@dataclass(frozen=True)
class UFunction:
    """A law ``f: 𝕌 → 𝕌`` with explicit response to branching/compression."""

    apply: Callable[[object], object]
    branch_input: Callable[[object], object]
    compress_input: Callable[[object], object]

    def __call__(self, value: object) -> object:
        """Apply the function to a U-state."""
        return self.apply(value)

    def on_branch(self, value: object) -> object:
        """Return ``f(value : Ω)``."""
        return self.branch_input(value)

    def on_compress(self, value: object) -> object:
        """Return ``f(value : D(Id))``."""
        return self.compress_input(value)

    def compose(self, inner: UFunction) -> UFunction:
        """Return composition ``self ∘ inner``."""
        return compose(self, inner)


def power_function(exponent: object) -> UFunction:
    """Return scale-covariant function ``f(x)=x^b``."""
    exponent_value = _finite(exponent)

    def apply(value: object) -> object:
        return power(value, exponent_value)

    return UFunction(
        apply=apply,
        branch_input=lambda value: apply(branch(value)),
        compress_input=lambda value: apply(compress(value)),
    )


def branching_function() -> UFunction:
    """Return exponential branching function ``f(x)=D(x)``."""
    return UFunction(
        apply=branch,
        branch_input=lambda value: branch(branch(value)),
        compress_input=lambda value: branch(compress(value)),
    )


def logarithmic_function() -> UFunction:
    """Return navigation function ``L(x)``."""
    from ..operators.L import L

    def branch_shift(value: object) -> object:
        return add(L(value), 1.0)

    def compress_shift(value: object) -> object:
        return add(L(value), -1.0)

    return UFunction(apply=L, branch_input=branch_shift, compress_input=compress_shift)


def periodic_function(k: object) -> UFunction:
    """Return cyclic function ``e^(i·k·x)`` as a point on the flow plane."""
    from ..transcendental.cos import cos
    from ..transcendental.sin import sin

    wave_number = _finite(k)

    def apply(value: object) -> ComplexState:
        angle = multiply(wave_number, value)
        return ComplexState(cos(angle), sin(angle))

    return UFunction(
        apply=apply,
        branch_input=lambda value: apply(branch(value)),
        compress_input=lambda value: apply(compress(value)),
    )


def compose(outer: UFunction, inner: UFunction) -> UFunction:
    """Return ``outer ∘ inner`` with branching passing through the inner law."""
    return UFunction(
        apply=lambda value: outer(inner(value)),
        branch_input=lambda value: outer(inner.on_branch(value)),
        compress_input=lambda value: outer(inner.on_compress(value)),
    )
