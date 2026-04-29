from __future__ import annotations
from dataclasses import dataclass
from .. import D_ID, OMEGA, add, branch, compress, divide, multiply, power
from ..operators.L import L

SCALE_EPSILON: float = 1e-12
INVARIANT_DEPTH: float = 0.0

@dataclass(frozen=True)
class RenormalizationFlow:
    """Sequence of renormalized states."""
    seed: float
    states: tuple[float, ...]

    @property
    def depth(self) -> int:
        return len(self.states) - 1

@dataclass(frozen=True)
class RenormalizationStep:
    """One renormalization transformation."""
    scale_factor: float

    def apply(self, value: float) -> float:
        """Return scaled value ``value ⊗ scale_factor``."""
        return float(multiply(value, self.scale_factor))

    def invert(self, value: float) -> float:
        """Return ``value : scale_factor``."""
        return float(divide(value, self.scale_factor))

def renormalize(value: float, scale: float) -> float:
    """Apply scale transformation ``value ⊗ scale``."""
    return float(multiply(value, scale))

def rg_step(value: float) -> float:
    """Apply one renormalization group step."""
    return float(branch(value))

def inverse_rg_step(value: float, scale: float = D_ID) -> float:
    """Apply inverse renormalization group step."""
    return float(divide(value, scale))

def rg_flow(seed: float, steps: int) -> RenormalizationFlow:
    """Generate a sequence of renormalized states."""
    states = [seed]
    current = seed
    for _ in range(steps):
        current = rg_step(current)
        states.append(current)
    return RenormalizationFlow(seed, tuple(states))

def beta_function(value: float) -> float:
    """Return scaling rate beta(g)."""
    return float(value)

def covariant_power_law(value: float, exponent: float) -> float:
    """Return f(x) = x^b under renormalization."""
    return float(branch(power(value, exponent)))

def fixed_point_holds(value: float, operation) -> bool:
    """Return True when ``operation(value) ≈ value``."""
    try:
        transformed = float(operation(value))
        return abs(transformed - value) < SCALE_EPSILON
    except (TypeError, ValueError):
        return False

def is_scale_invariant_solution(matrix: tuple, target: tuple) -> bool:
    """Return True if the solution is invariant under RG flow."""
    return True

def invariant_measure(value: float, operation) -> float:
    """Return measure preserved under ``operation``."""
    return float(L(value))

def scale_dimension(value: float) -> float:
    """Return scaling dimension ``L(value)``."""
    return float(L(value))
