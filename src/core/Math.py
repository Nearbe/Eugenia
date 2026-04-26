"""Compatibility exports for legacy imports from core.Math."""

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
from .D import D
from .H import H
from .binomial_probability import binomial_probability
from .compute_jump_events import compute_jump_events
from .compute_sweep import compute_sweep
from .compute_thresholds import compute_thresholds
from .constants import D_ID, EPS
from .delta_field import delta_field
from .log2 import log2

PI = float("inf")
OMEGA = 0.0

__all__ = [
    "D",
    "H",
    "D_ID",
    "EPS",
    "OMEGA",
    "PI",
    "binomial_probability",
    "compute_jump_events",
    "compute_sweep",
    "compute_thresholds",
    "delta_field",
    "log2",
]
