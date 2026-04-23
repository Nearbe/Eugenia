#!/usr/bin/env python3

from __future__ import annotations

from itertools import cycle
from math import cos, log10, sin
from sys import set_int_max_str_digits, setrecursionlimit, setswitchinterval
from time import perf_counter
from typing import Final

# ── Constants ────────────────────────────────────────────────────────────────
Q: Final[int] = 10
FULL_RANGE: Final[int] = 10 ** Q


# ── Helper functions ─────────────────────────────────────────────────────────

def pct_from_spine(spine: float) -> float:
    if spine >= 1000:
        return 100.0
    if spine <= -1000:
        return 0.0
    exp_arg = -spine
    if exp_arg > 700:
        return 0.0
    if exp_arg < -700:
        return 100.0
    return 100.0 / (1.0 + 10.0 ** exp_arg)


def delta_from_spine(spine: float) -> float:
    X = max(min(spine, FULL_RANGE - 1.001), 0.0)
    return log10(X + 1.0) - log10(FULL_RANGE - X)


def v2_of_step(step: int) -> float:
    v = step
    if v == 0:
        return float("inf")
    v = abs(v)
    n = 0
    while v > 0 and (v & 1) == 0:
        v >>= 1
        n += 1
    return float(n)


# ── The pure cycle ───────────────────────────────────────────────────────────

def f() -> None:
    return


# ── Core computation ─────────────────────────────────────────────────────────

def main() -> None:
    start: float = perf_counter()
    count = 0

    for step in cycle(range(Q)):
        count += 1
        elapsed: float = perf_counter() - start
        calls_per_sec: float = step + 1 / elapsed if elapsed > 0 else float("inf")

        power = Q - 1 - step
        scale = 10.0**power

        spine = log10(scale)

        pct = pct_from_spine(spine)

        delta = delta_from_spine(spine)

        branch = delta * 2.0
        compress = delta / 2.0

        theta = step * 3.141592653589793 / Q
        rot_real = delta * cos(theta) - spine * sin(theta)
        rot_imag = delta * sin(theta) + spine * cos(theta)

        form = delta
        velocity = spine

        v2 = v2_of_step(step)

        # solenoid trajectory: encode_solenoid_trajectory(delta, depth=30)
        sol = []
        current = abs(delta)
        for _ in range(30):
            if current >= 2.0:
                sol.append(1)
                current = current / 2.0
            else:
                sol.append(0)
                current = current * 2.0
        sol_bits = sol[:5] if len(sol) >= 5 else sol + [0] * (5 - len(sol))
        sol_str = "".join(str(b) for b in sol_bits)

        print(
            f"step={step} | scale={scale:>16.0f} | spine={spine:.4f} | "
            f"pct={pct:.1f}% | delta={delta:.4f} | D(δ)={branch:.1f} | "
            f"H(δ)={compress:.1f} | v2={v2} | sol=[{sol_str}] | "
            f"rot=({rot_real:.3f}, {rot_imag:.3f}) | "
            f"count={count} | {elapsed:.9f}с | {calls_per_sec:,.9f} вызовов/с"
        )
        f()


# ── Runtime settings ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    set_int_max_str_digits(0)
    setswitchinterval(0.00000000000000001)
    setrecursionlimit(3)
    main()
