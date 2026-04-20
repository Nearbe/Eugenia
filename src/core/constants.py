"""
Mathematical constants for the RealMath / Essentials framework.

Constants — Π (Pi) and Ω (Omega)
==================================

Π — Полнота (Completeness). Represents 100% — absolute saturation.
    In practice: a sufficiently large value that is stable under all operations.
    Π : Ω = Π, Π : D(Id) = Π, √[n]{Π} = Π, Π^k = Π

Ω — Потенциал (Potential). Represents absolute potential, −∞ on log scale.
    In practice: the identity element for branching — a:Ω = D(a)

D(Id) — First branching (duality). In arithmetic: 2.
Dⁿ(Id) = 2ⁿ — the "spine" of the fractal.
"""

import math

# ============================================================
# Constants — Π (Pi) and Ω (Omega)
# ============================================================

# Π — Полнота (Completeness). Represents 100% — absolute saturation.
# In practice: a sufficiently large value that is stable under all operations.
# Π : Ω = Π, Π : D(Id) = Π, √[n]{Π} = Π, Π^k = Π
PI = math.inf  # Mathematical Π — stable under all RealMath operations

# Ω — Потенциал (Potential). Represents absolute potential, −∞ on log scale.
# In practice: the identity element for branching — a:Ω = D(a)
OMEGA = 0.0  # Mathematical Ω — branching trigger

# D(Id) — First branching (duality). In arithmetic: 2.
# Dⁿ(Id) = 2ⁿ — the "spine" of the fractal.
D_ID = 2.0
