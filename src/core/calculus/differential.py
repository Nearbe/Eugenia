"""
Top-level documentation for the Differential Calculus module.

This module implements fundamental rules for differential calculus using dual numbers 
and custom algebraic operations defined in `u_algebra`. It provides tools for 
calculating derivatives, chain rule applications, power rules, and basic 
differential state tracking based on the formula f(x + v*e) = f(x) + f'(x)*v*e.

Key functions include:
- differential_state: Calculates the result of a function evaluated at a point 
  offset by a velocity (epsilon).
- derivative: Extracts the derivative function for a given point.
- chain_derivative: Implements the chain rule for composite functions.
- second_derivative: Calculates the second derivative.
- add_derivative: Calculates the derivative of a sum of functions.
"""
"""Differential calculus from Universe/Math/20_Дифференциальное_исчисление.md."""

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

from ..foundations.constants import D_ID
from ..foundations.dual_number import DualNumber, dual_number
from ..foundations.u_algebra import add, branch, compress, divide, multiply, power
from ..operators.L import L

IDENTITY_VELOCITY = 1.0


def differential_state(
    fn: Callable[[object], object],
    derivative_fn: Callable[[object], object],
    point: object,
    *,
    velocity: object = IDENTITY_VELOCITY,
) -> DualNumber:
    """Return ``f(x + vε) = f(x) + f'(x)·vε``."""
    return dual_number(point, velocity).apply(fn, derivative_fn)


def derivative(
    fn: Callable[[object], object],
    derivative_fn: Callable[[object], object],
    point: object,
) -> object:
    """Extract ``f'(x)`` as the hidden coefficient for unit velocity."""
    return differential_state(fn, derivative_fn, point).velocity


def power_derivative(exponent: object, point: object) -> object:
    """Return derivative of ``x^b`` from the dual expansion rule."""
    exponent_value = float(exponent)
    return multiply(exponent_value, power(point, exponent_value - IDENTITY_VELOCITY))


def branching_growth_velocity(value: object) -> object:
    """Return ``dx/dt = L(D(Id))·x`` for ``x(t)=Dᵗ(Id)``."""
    return multiply(L(D_ID), value)


def branched_derivative(derivative_fn: Callable[[object], object], point: object) -> object:
    """Return ``g'(x)`` for ``g(x)=f(D(x))``."""
    return multiply(D_ID, derivative_fn(branch(point)))


def compressed_derivative(derivative_fn: Callable[[object], object], point: object) -> object:
    """Return ``h'(x)`` for ``h(x)=f(x : D(Id))``."""
    return divide(derivative_fn(compress(point)), D_ID)


def chain_derivative(
    outer_derivative: Callable[[object], object],
    inner_fn: Callable[[object], object],
    inner_derivative: Callable[[object], object],
    point: object,
) -> object:
    """Return ``(f∘g)'(x) = f'(g(x)) · g'(x)``."""
    return multiply(outer_derivative(inner_fn(point)), inner_derivative(point))


def second_derivative(
    first_derivative_fn: Callable[[object], object],
    second_derivative_fn: Callable[[object], object],
    point: object,
) -> object:
    """Return ``f''(x)`` by extracting dynamics of the first derivative."""
    return derivative(first_derivative_fn, second_derivative_fn, point)


def add_derivative(
    left_derivative: Callable[[object], object],
    right_derivative: Callable[[object], object],
    point: object,
) -> object:
    """Return derivative of ``f⊕g``."""
    return add(left_derivative(point), right_derivative(point))
