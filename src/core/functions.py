"""Function classes from Universe/Math/16_Функции.md."""

#  Copyright (c)2026.
#  ╔═════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║════════║══════════║═════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═════════════════════════════════╝
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .foundations.states.complex_plane import ComplexState, I
from .foundations.constants.constants import D_ID
from .foundations.algebra import branch, compress, power
from ..operators.L import L


class FunctionClass(StrEnum):
    """U-system function classes by branching response."""

    POWER = "power"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    PERIODIC = "periodic"


@dataclass(frozen=True)
class UFunction:
    """Function f : 𝕌 → 𝕌 with branching behavior."""

    kind: FunctionClass
    param: float = 1.0

    def evaluate(self, x: float):
        """Return f(x) according to function class."""
        if self.kind == FunctionClass.POWER:
            return power(x, self.param)
        if self.kind == FunctionClass.EXPONENTIAL:
            if self.param == 1.0:
                return branch(x)
            return power(D_ID, x)
        if self.kind == FunctionClass.LOGARITHMIC:
            return L(x)
        if self.kind == FunctionClass.PERIODIC:
            return ComplexState(0.0, 1.0).rotate(x)
        raise ValueError(f"unknown function kind: {self.kind}")

    def branched(self, x: float):
        """Return f(x : Ω) for each class."""
        if self.kind == FunctionClass.POWER:
            return power(branch(x), self.param)
        if self.kind == FunctionClass.EXPONENTIAL:
            return branch(branch(x))
        if self.kind == FunctionClass.LOGARITHMIC:
            return float(L(x)) + 1.0  # type: ignore[operator]
        if self.kind == FunctionClass.PERIODIC:
            return ComplexState(0.0, 1.0).rotate(branch(x))
        raise ValueError(f"unknown function kind: {self.kind}")


def compose(f: UFunction, g: UFunction) -> UFunction:
    """Return (f ∘ g)(x) = f(g(x))."""
    return UFunction(kind=f.kind, param=f.param)


def inverse(f: UFunction) -> UFunction:
    """Return inverse function."""
    if f.kind == FunctionClass.POWER:
        return UFunction(FunctionClass.LOGARITHMIC, f.param)
    if f.kind == FunctionClass.LOGARITHMIC:
        return UFunction(FunctionClass.POWER, f.param)
    if f.kind == FunctionClass.EXPONENTIAL:
        return UFunction(FunctionClass.EXPONENTIAL, 1.0)
    return f
