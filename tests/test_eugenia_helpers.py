# Tests for eugenia_helpers module
"""
These tests verify the pure helper functions extracted from ``Eugenia.py``.
They cover typical, edge and extreme cases to ensure mathematical correctness.
"""

import math
import sys
from pathlib import Path

# Ensure the project root is on PYTHONPATH for imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from Eugenia import (
    pct_from_spine,
    delta_from_spine,
    v2_of_step,
    solenoid_bits,
    Q,
    FULL_RANGE,
)


def test_pct_from_spine_basic():
    # spine = 0 => sigmoid gives exactly 50%
    assert math.isclose(pct_from_spine(0.0), 50.0, rel_tol=1e-12)
    # large positive spine (near max 9) → near 100%
    assert pct_from_spine(9.0) > 99.999999
    # large negative spine (not used in main loop but function should handle)
    assert pct_from_spine(-9.0) < 0.000001
    # overflow guard branches
    assert pct_from_spine(1001) == 100.0
    assert pct_from_spine(-1001) == 0.0
    # extreme exponent guards
    assert pct_from_spine(701) == 100.0  # exp_arg = -701 < -700 => returns 100
    assert pct_from_spine(-701) == 0.0   # exp_arg = 701 > 700 => returns 0


def test_delta_from_spine_bounds():
    # spine = 0 → delta should be -log10(FULL_RANGE)
    expected = -math.log10(FULL_RANGE)
    assert math.isclose(delta_from_spine(0.0), expected, rel_tol=1e-12)
    # spine = FULL_RANGE - 1 (max possible) → delta ≈ log10(FULL_RANGE) - log10(1) = +log10(FULL_RANGE)
    max_spine = FULL_RANGE - 1.0
    expected_max = math.log10(max_spine + 1.0) - math.log10(FULL_RANGE - max_spine)
    assert math.isclose(delta_from_spine(max_spine), expected_max, rel_tol=1e-12)
    # typical middle value
    mid = FULL_RANGE / 2.0 - 0.5
    delta_mid = delta_from_spine(mid)
    # symmetry: delta should be close to 0 for the midpoint
    assert abs(delta_mid) < 1e-12


def test_v2_of_step_cases():
    assert math.isinf(v2_of_step(0))
    # odd numbers have valuation 0
    for step in (1, 3, 5, 7, 9):
        assert v2_of_step(step) == 0.0
    # powers of two have increasing valuation
    assert v2_of_step(2) == 1.0
    assert v2_of_step(4) == 2.0
    assert v2_of_step(8) == 3.0


def test_solenoid_bits_patterns():
    # delta = 0 → all zeros
    assert solenoid_bits(0.0) == "00000"
    # delta = 1 (less than 2) → pattern of alternating zeros and ones
    # Simulate manually: start=1 (<2) ->0, double to 2; then >=2 ->1, halve to1; repeat => 0,1,0,1,0
    assert solenoid_bits(1.0) == "01010"
    # delta = 2 (exact threshold) → first step >=2 ->1, halve to1, then pattern as above => 1,0,1,0,1
    assert solenoid_bits(2.0) == "10101"
    # delta = 3 (greater than 2) → first >=2 ->1, halve to1.5 (<2) ->0, double to3; then >=2 ->1, halve to1.5... pattern 1,0,1,0,1
    assert solenoid_bits(3.0) == "10101"
