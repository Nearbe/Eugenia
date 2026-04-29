"""Geometry from Universe/Math/22_Геометрия.md."""

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

from ..foundations.complex_plane import ComplexState, complex_state
from ..foundations.constants import D_ID
from ..foundations.u_algebra import branch, compress, power
from ..transcendental.sqrt import sqrt

MIN_DIMENSION = 0
CURVATURE_EXPONENT = 3.0 / D_ID


def distance(a: object, b: object) -> float:
    """Return U-metric ``d(a,b)=|a⊖b|`` for finite scalar states."""
    return abs(float(a) - float(b))


def complex_radius(value: object) -> object:
    """Return ``|z| = √(x²⊕y²)`` on the complex plane."""
    state = complex_state(value)
    if not isinstance(state, ComplexState):
        return state
    return sqrt(state.norm_squared())


def branch_measure(measure: object, *, dimension: int) -> object:
    """Return measure scaled by ``Dᵏ(Id)`` for k-dimensional geometry."""
    if dimension < MIN_DIMENSION:
        raise ValueError("dimension must be non-negative")
    scale = power(D_ID, dimension)
    return float(measure) * float(scale)


def compress_measure(measure: object, *, dimension: int) -> object:
    """Return measure scaled by ``Hᵏ(Id)`` for k-dimensional geometry."""
    if dimension < MIN_DIMENSION:
        raise ValueError("dimension must be non-negative")
    scale = power(D_ID, dimension)
    return float(measure) / float(scale)


@dataclass(frozen=True)
class Segment:
    """Finite segment ``[a,b]``."""

    start: float
    end: float

    def length(self) -> float:
        """Return segment length."""
        return distance(self.start, self.end)

    def branch(self) -> Segment:
        """Return ``[D(a),D(b)]``."""
        return Segment(float(branch(self.start)), float(branch(self.end)))

    def compress(self) -> Segment:
        """Return ``[H(a),H(b)]``."""
        return Segment(float(compress(self.start)), float(compress(self.end)))


@dataclass(frozen=True)
class Circle:
    """Circle ``{z ∈ ℂ | |z-center| = r}``."""

    center: ComplexState
    radius: float

    def branch(self) -> Circle:
        """Return branched circle with radius ``D(r)``."""
        branched_center = branch(self.center)
        if not isinstance(branched_center, ComplexState):
            raise TypeError("branched circle center must stay finite complex")
        return Circle(branched_center, float(branch(self.radius)))

    def compress(self) -> Circle:
        """Return compressed circle with radius ``H(r)``."""
        compressed_center = compress(self.center)
        if not isinstance(compressed_center, ComplexState):
            raise TypeError("compressed circle center must stay finite complex")
        return Circle(compressed_center, float(compress(self.radius)))


@dataclass(frozen=True)
class Ball:
    """Ball ``{z ∈ ℂ | |z-center| ≤ r}``."""

    center: ComplexState
    radius: float

    def branch(self) -> Ball:
        """Return branched ball."""
        branched_center = branch(self.center)
        if not isinstance(branched_center, ComplexState):
            raise TypeError("branched ball center must stay finite complex")
        return Ball(branched_center, float(branch(self.radius)))

    def compress(self) -> Ball:
        """Return compressed ball."""
        compressed_center = compress(self.center)
        if not isinstance(compressed_center, ComplexState):
            raise TypeError("compressed ball center must stay finite complex")
        return Ball(compressed_center, float(compress(self.radius)))


def _relative_complex(point: object, center: ComplexState) -> ComplexState:
    """Return point-center in the complex plane."""
    state = complex_state(point)
    if not isinstance(state, ComplexState):
        raise TypeError("point must be a finite complex state")
    return ComplexState(state.real - center.real, state.imaginary - center.imaginary)


def is_on_circle(point: object, circle: Circle) -> bool:
    """Return true when point lies on the circle."""
    return complex_radius(_relative_complex(point, circle.center)) == circle.radius


def is_inside_ball(point: object, ball: Ball) -> bool:
    """Return true when point lies inside or on the ball."""
    return float(complex_radius(_relative_complex(point, ball.center))) <= ball.radius


def curvature(first_derivative: object, second_derivative: object) -> object:
    """Return ``κ = |f''(x)| : (Id⊕f'(x)²)^(3:D(Id))``."""
    denominator = power(1.0 + float(first_derivative) * float(first_derivative), CURVATURE_EXPONENT)
    return abs(float(second_derivative)) / float(denominator)


def compressed_curvature(value: object) -> object:
    """Return curvature after branching: ``κ : D(Id)``."""
    return compress(value)
