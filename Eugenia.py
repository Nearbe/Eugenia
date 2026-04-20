#!/usr/bin/env python3
from itertools import cycle
from math import (
    cos,
    log10,
    sin,
)
from sys import (
    set_int_max_str_digits,
    setrecursionlimit,
    setswitchinterval,
)
from time import perf_counter


def f() -> None:
    return  # Возвращает немедленно — дальнейший рост стека не требуется


def main() -> None:
    start: float = perf_counter()
    count = 0

    # Q = D_f = 10 — цикл 0-9 (10 шагов), каждый шаг = смена масштаба ×10
    # 1.0 = 1000000000.0000000001
    #   слева: 10^9 (10 цифр минус)  +  справа: 10^-10 (10 цифр плюс)
    # шаг=0 → scale=10^9, шаг=9 → scale=10^0=1
    Q = 10
    FULL_RANGE = 10**Q  # 10^10 = 10000000000

    for step in cycle(range(Q)):
        count += 1
        elapsed: float = perf_counter() - start
        calls_per_sec: float = step + 1 / elapsed if elapsed > 0 else float("inf")

        # ── масштабный сдвиг: step=0..9 → 10^9 .. 10^0 ────────────
        power = Q - 1 - step  # 9, 8, 7, ..., 0
        scale = 10.0**power

        # spine = L(x₀) = log10(scale) — номер уровня хребта
        spine = log10(scale)  # 9, 8, 7, ..., 0

        # pct = ridge_to_percentage(spine) = sigmoid(spine) × 100%
        if spine >= 1000:
            pct = 100.0
        elif spine <= -1000:
            pct = 0.0
        else:
            exp_arg = -spine
            if exp_arg > 700:
                pct = 0.0
            elif exp_arg < -700:
                pct = 100.0
            else:
                pct = 100.0 / (1.0 + 10.0**exp_arg)

        # delta = delta_field на полном диапазоне [0, 10^Q-1] → [-Q, +Q]
        X = max(min(spine, FULL_RANGE - 1.001), 0.0)
        delta = log10(X + 1.0) - log10(FULL_RANGE - X)

        # branch = D(delta) = delta × 2
        branch = delta * 2.0
        # compress = H(delta) = delta / 2
        compress = delta / 2.0

        # complex rotation: theta = step × π / Q
        theta = step * 3.141592653589793 / Q
        rot_real = delta * cos(theta) - spine * sin(theta)
        rot_imag = delta * sin(theta) + spine * cos(theta)

        # dual form: (form, velocity) = (delta, spine)
        form = delta
        velocity = spine

        # 2-adic valuation: v2(step)
        v = step
        if v == 0:
            v2 = float("inf")
        else:
            v = abs(v)
            n = 0
            while v > 0 and (v & 1) == 0:
                v >>= 1
                n += 1
            v2 = float(n)

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

        # ── вывод ───────────────────────────────────────────────────
        print(
            f"step={step} | scale={scale:>16.0f} | spine={spine:.4f} | "
            f"pct={pct:.1f}% | delta={delta:.4f} | D(δ)={branch:.1f} | "
            f"H(δ)={compress:.1f} | v2={v2} | sol=[{sol_str}] | "
            f"rot=({rot_real:.3f}, {rot_imag:.3f}) | "
            f"count={count} | {elapsed:.9f}с | {calls_per_sec:,.9f} вызовов/с"
        )
        f()


if __name__ == "__main__":
    set_int_max_str_digits(0)
    setswitchinterval(0.00000000000000001)
    setrecursionlimit(3)
    main()
