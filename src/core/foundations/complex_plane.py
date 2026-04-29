"""Complex flow plane from Universe/Math/09_Комплексные.md."""

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

from .constants import D_ID, OMEGA
from .infinity import is_fullness

REAL_INDEX: Final[int] = 0
IMAGINARY_INDEX: Final[int] = 1
COMPLEX_ARITY: Final[int] = 2
IDENTITY_REAL: Final[float] = 1.0
ZERO_COMPONENT: Final[float] = 0.0


@dataclass(frozen=True)
class ComplexFullness:
    """Complex fullness ``Π_z``: fullness on the Re/Im plane."""

    symbol: str = "Π_z"

    def branch(self) -> ComplexFullness:
        """Return ``Π_z : Ω = Π_z``."""
        return self

    def compress(self) -> ComplexFullness:
        """Return ``Π_z : D(Id) = Π_z``."""
        return self

    def __repr__(self) -> str:
        return self.symbol

    def __str__(self) -> str:
        return self.symbol


PI_Z: Final[ComplexFullness] = ComplexFullness()


@dataclass(frozen=True)
class ComplexState:
    """State ``x + i·y`` where x is explicit flow and y is hidden flow."""

    real: float = ZERO_COMPONENT
    imaginary: float = ZERO_COMPONENT

    def __post_init__(self) -> None:
        object.__setattr__(self, "real", float(self.real))
        object.__setattr__(self, "imaginary", float(self.imaginary))

    def branch(self) -> ComplexState:
        """Return ``(x + i·y) : Ω = D(x) + i·D(y)``."""
        return ComplexState(self.real * D_ID, self.imaginary * D_ID)

    def compress(self) -> ComplexState:
        """Return ``(x + i·y) : D(Id) = H(x) + i·H(y)``."""
        return ComplexState(self.real / D_ID, self.imaginary / D_ID)

    def conjugate(self) -> ComplexState:
        """Return ``z̄ = x − i·y``."""
        return ComplexState(self.real, -self.imaginary)

    def norm_squared(self) -> float:
        """Return ``|z|² = x² + y²``."""
        return self.real * self.real + self.imaginary * self.imaginary

    def add(self, other: ComplexState) -> ComplexState:
        """Return component-wise complex addition."""
        return ComplexState(self.real + other.real, self.imaginary + other.imaginary)

    def multiply(self, other: ComplexState) -> ComplexState:
        """Return complex multiplication with ``i² = -Id``."""
        real = self.real * other.real - self.imaginary * other.imaginary
        imaginary = self.real * other.imaginary + self.imaginary * other.real
        return ComplexState(real, imaginary)

    def scale(self, factor: object) -> ComplexState:
        """Scale both Re and Im flows by the same finite factor."""
        factor_value = float(factor)
        return ComplexState(self.real * factor_value, self.imaginary * factor_value)

    def divide_by(self, denominator: ComplexState) -> ComplexState:
        """Return ordinary complex division, with zero denominator as Ω-branching."""
        norm = denominator.norm_squared()
        if norm == OMEGA:
            return self.branch()
        real = (self.real * denominator.real + self.imaginary * denominator.imaginary) / norm
        imaginary = (self.imaginary * denominator.real - self.real * denominator.imaginary) / norm
        return ComplexState(real, imaginary)

    def rotate(self, angle: object) -> ComplexState:
        """Return ``z · e^(i·angle)`` as norm-preserving Re/Im exchange."""
        from ..transcendental.cos import cos
        from ..transcendental.sin import sin

        cosine = float(cos(float(angle)))
        sine = float(sin(float(angle)))
        return ComplexState(
            self.real * cosine - self.imaginary * sine,
            self.real * sine + self.imaginary * cosine,
        )

    def to_builtin(self) -> complex:
        """Return Python's complex representation for interop only."""
        return complex(self.real, self.imaginary)

    def __complex__(self) -> complex:
        return self.to_builtin()

    def __repr__(self) -> str:
        return f"{self.real:g} + i·{self.imaginary:g}"


I: Final[ComplexState] = ComplexState(ZERO_COMPONENT, IDENTITY_REAL)


def is_complex_fullness(value: object) -> bool:
    """Return True for complex fullness ``Π_z``."""
    return value == PI_Z


def is_complex_state(value: object) -> bool:
    """Return True for finite Re/Im states."""
    return isinstance(value, ComplexState)


def complex_state(real: object = ZERO_COMPONENT, imaginary: object = ZERO_COMPONENT) -> ComplexState | ComplexFullness:
    """Construct a complex U-state from scalar, pair, Python complex or Π."""
    if is_complex_fullness(real) or is_fullness(real):
        return PI_Z
    if isinstance(real, ComplexState) and imaginary == ZERO_COMPONENT:
        return real
    if isinstance(real, complex) and imaginary == ZERO_COMPONENT:
        return ComplexState(real.real, real.imag)
    if isinstance(real, tuple | list) and len(real) == COMPLEX_ARITY and imaginary == ZERO_COMPONENT:
        return ComplexState(real[REAL_INDEX], real[IMAGINARY_INDEX])
    return ComplexState(real, imaginary)


def conjugate(value: object) -> ComplexState | ComplexFullness:
    """Return reflection in the explicit flow axis."""
    state = complex_state(value)
    if is_complex_fullness(state):
        return PI_Z
    return state.conjugate()


def norm_squared(value: object) -> float | ComplexFullness:
    """Return total intensity ``|z|²``."""
    state = complex_state(value)
    if is_complex_fullness(state):
        return PI_Z
    return state.norm_squared()


def rotate(value: object, angle: object) -> ComplexState | ComplexFullness:
    """Rotate a finite complex state without changing its norm."""
    state = complex_state(value)
    if is_complex_fullness(state):
        return PI_Z
    return state.rotate(angle)
