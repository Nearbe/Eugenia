#!/usr/bin/env python3
"""04: Анализ скачков (jumps)."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    thr = sweep["thresholds"]
    jpe = np.zeros(len(thr))
    for t, _, _, _, _ in sweep["jump_events"]:
        jpe[np.argmin(np.abs(thr - t))] += 1
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(thr, jpe, color="crimson", linewidth=0.5)
    ax.fill_between(thr, 0, jpe, alpha=0.3, color="crimson")
    ax.set_xlabel("Порог Δ")
    ax.set_ylabel("Скачков (>1%)")
    ax.set_title(f"Скачков всего: {sweep['jump_count']}", fontsize=14)
    ax.axvline(x=0, color="gray", linestyle="--")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/04_jumps_analysis.png", dpi=120)
    plt.close()
