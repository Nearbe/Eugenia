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
from typing import Union

from ..states.complex_plane import ComplexState, complex_state
from ..constants.constants import D_ID
from ..algebra import branch, compress, power
from ..transcendental.sqrt import sqrt

MIN_DIMENSION = 0
CURVATURE_EXPONENT = 3.0 / D_ID


def distance(a: Union[float, int], b: Union[float, int]) -> float:
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
    return float(measure) * float(scale)  # type: ignore[arg-type]


def compress_measure(measure: object, *, dimension: int) -> object:
    """Return measure scaled by ``Hᵏ(Id)`` for k-dimensional geometry."""
    if dimension < MIN_DIMENSION:
        raise ValueError("dimension must be non-negative")
    scale = power(D_ID, dimension)
    return float(measure) / float(scale)  # type: ignore[arg-type]


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
        return Segment(float(branch(self.start)), float(branch(self.end)))  # type: ignore[arg-type]

    def compress(self) -> Segment:
        """Return ``[H(a),H(b)]``."""
        return Segment(float(compress(self.start)), float(compress(self.end)))  # type: ignore[arg-type]


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
        return Circle(branched_center, float(branch(self.radius)))  # type: ignore[arg-type]

    def compress(self) -> Circle:
        """Return compressed circle with radius ``H(r)``."""
        compressed_center = compress(self.center)
        if not isinstance(compressed_center, ComplexState):
            raise TypeError("compressed circle center must stay finite complex")
        return Circle(compressed_center, float(compress(self.radius)))  # type: ignore[arg-type]


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
        return Ball(branched_center, float(branch(self.radius)))  # type: ignore[arg-type]

    def compress(self) -> Ball:
        """Return compressed ball."""
        compressed_center = compress(self.center)
        if not isinstance(compressed_center, ComplexState):
            raise TypeError("compressed ball center must stay finite complex")
        return Ball(compressed_center, float(compress(self.radius)))  # type: ignore[arg-type]


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
    return float(complex_radius(_relative_complex(point, ball.center))) <= ball.radius  # type: ignore[arg-type]


def curvature(first_derivative: object, second_derivative: object) -> object:
    """Return ``κ = |f''(x)| : (Id⊕f'(x)²)^(3:D(Id))``."""
    denominator = power(1.0 + float(first_derivative) * float(first_derivative), CURVATURE_EXPONENT)  # type: ignore[arg-type]
    return abs(float(second_derivative)) / float(denominator)  # type: ignore[arg-type]


def compressed_curvature(value: object) -> object:
    """Return curvature after branching: ``κ : D(Id)``."""
    return compress(value)


def branched_distance(a: object, b: object) -> float:
    """Return ``d(D(a), D(b)) = D(d(a,b))``."""
    return distance(float(branch(a)), float(branch(b)))  # type: ignore[arg-type]


def compressed_distance(a: object, b: object) -> float:
    """Return ``d(H(a), H(b)) = H(d(a,b))``."""
    return distance(float(compress(a)), float(compress(b)))  # type: ignore[arg-type]


def rotate_z(value: object, angle: object) -> object:
    """Return ``z · e^{i·θ}`` — norm-preserving rotation on ℂ."""
    state = complex_state(value)
    if not isinstance(state, ComplexState):
        raise TypeError("rotate_z requires a finite complex state")
    return state.rotate(angle)
