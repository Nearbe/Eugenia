"""Integral calculus from Universe/Math/21_Интегральное_исчисление.md."""

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
from ..foundations.spine import SpineLevel
from ..foundations.u_algebra import add, branch, compress, divide, multiply, power
from ..operators.L import L

IDENTITY_POWER = 1.0


def power_antiderivative(exponent: object, point: object) -> object:
    """Return primitive of ``x^b`` at ``point``: ``x^(b⊕Id) : (b⊕Id)``."""
    next_exponent = add(exponent, IDENTITY_POWER)
    return divide(power(point, next_exponent), next_exponent)


def antiderivative(
    primitive_fn: Callable[[object], object],
    point: object,
    *,
    constant: object = 0.0,
) -> object:
    """Return ``F(x) ⊕ C`` for an indefinite integral."""
    return add(primitive_fn(point), constant)


def definite_integral(
    primitive_fn: Callable[[object], object],
    lower: object,
    upper: object,
) -> object:
    """Return ``∫ₐᵇ f(x)dx = F(b) ⊖ F(a)``."""
    return add(primitive_fn(upper), -float(primitive_fn(lower)))


def branched_integral(primitive_fn: Callable[[object], object], point: object) -> object:
    """Return ``∫ f(D(x))dx = (∫ f(u)du) : D(Id)``."""
    return compress(primitive_fn(branch(point)))


def compressed_integral(primitive_fn: Callable[[object], object], point: object) -> object:
    """Return ``∫ f(x:D(Id))dx = (∫ f(u)du) ⊗ D(Id)``."""
    return branch(primitive_fn(compress(point)))


def integral_on_log_depth(fn: Callable[[object], object], depth: SpineLevel) -> object:
    """Return log-depth integrand ``f(D^ℓ)·L(D(Id))·D^ℓ``."""
    state = depth.value()
    return multiply(multiply(fn(state), L(D_ID)), state)
