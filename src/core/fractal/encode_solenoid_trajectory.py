"""Binary-fraction encoding of a value as a solenoid trajectory."""

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
import math


def encode_solenoid_trajectory(delta_value: float, depth: int = 30) -> list[int]:
    """Return the first ``depth`` bits of ``delta_value`` modulo ``1``.

    The solenoid history is encoded as a binary fraction ``0.b₀b₁…``.  Bits are
    extracted from the fractional part by repeated doubling, not from the
    integer part.  Negative and large values are reduced modulo ``1`` so the
    encoding is deterministic on the circle.
    """
    if depth < 0:
        raise ValueError("solenoid trajectory depth must be non-negative")
    value = float(delta_value)
    if not math.isfinite(value):
        raise ValueError("solenoid trajectory value must be finite")

    fraction = value % 1.0
    bits: list[int] = []
    for _ in range(depth):
        fraction *= 2.0
        bit = int(fraction)
        bits.append(bit)
        fraction -= bit
    return bits
