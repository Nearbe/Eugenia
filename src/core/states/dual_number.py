"""Dual numbers from Universe/Math/14_Дуальные_числа.md."""

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
from typing import Final

from ..constants.constants import D_ID, OMEGA

EPSILON_SQUARED: Final[float] = OMEGA


@dataclass(frozen=True)
class DualNumber:
    """Dual state ``x + v·ε`` with ``ε² = Ω``."""

    form: object
    velocity: object = OMEGA

    def branch(self) -> DualNumber:
        """Return ``D(x) + D(v)ε``."""
        from ..algebra import branch

        return DualNumber(branch(self.form), branch(self.velocity))

    def compress(self) -> DualNumber:
        """Return ``H(x) + H(v)ε``."""
        from ..algebra import compress

        return DualNumber(compress(self.form), compress(self.velocity))

    def add(self, other: DualNumber) -> DualNumber:
        """Return ``(x⊕y) + (v⊕u)ε``."""
        from ..algebra import add

        return DualNumber(
            add(self.form, other.form), add(self.velocity, other.velocity)
        )

    def multiply(self, other: DualNumber) -> DualNumber:
        """Return ``(x⊗y) + (x⊗u ⊕ y⊗v)ε``."""
        from ..algebra import add, multiply

        form = multiply(self.form, other.form)
        velocity = add(
            multiply(self.form, other.velocity), multiply(other.form, self.velocity)
        )
        return DualNumber(form, velocity)

    def scale(self, factor: object) -> DualNumber:
        """Scale both form and velocity by a finite factor."""
        from ..algebra import multiply

        return DualNumber(multiply(self.form, factor), multiply(self.velocity, factor))

    def power(self, exponent: object) -> DualNumber:
        """Return ``xⁿ + n·xⁿ⁻¹·v·ε``."""
        from ..algebra import multiply, power

        exponent_value = float(exponent)
        form_power = power(self.form, exponent_value)
        derivative = multiply(exponent_value, power(self.form, exponent_value - 1.0))
        return DualNumber(form_power, multiply(derivative, self.velocity))

    def apply(
        self, fn: Callable[[object], object], derivative: Callable[[object], object]
    ) -> DualNumber:
        """Return ``f(x) + f'(x)·v·ε``."""
        from ..algebra import multiply

        return DualNumber(fn(self.form), multiply(derivative(self.form), self.velocity))

    def as_tuple(self) -> tuple[object, object]:
        """Return ``(x, v)`` for compatibility wrappers."""
        return self.form, self.velocity

    def __repr__(self) -> str:
        return f"{self.form!r} + {self.velocity!r}·ε"


def dual_number(form: object, velocity: object = OMEGA) -> DualNumber:
    """Construct ``form + velocity·ε``."""
    return DualNumber(form, velocity)


def is_dual_number(value: object) -> bool:
    """Return True for dual-number states."""
    return isinstance(value, DualNumber)


def natural_velocity(form: object) -> object:
    """Return ``v = x · L(D(Id))`` for D-growth, where ``L(D(Id)) = 1``."""
    from ..algebra import multiply

    return multiply(form, 1.0)
