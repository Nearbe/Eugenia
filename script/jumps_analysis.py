#!/usr/bin/env python3
"""Jump analysis."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    v = data["viz"]
    thr = sweep["thresholds"]
    jpe = np.zeros(len(thr))
    for t, _, _, _, _ in sweep["jump_events"]:
        jpe[np.argmin(np.abs(thr - t))] += 1
    fig, ax = plt.subplots(figsize=(v["fig_jumps_w"], v["fig_jumps_h"]))
    ax.plot(thr, jpe, color="crimson", linewidth=v["marker_size"])
    ax.fill_between(thr, 0, jpe, alpha=v["hist_alpha"], color="crimson")
    ax.set_xlabel("Порог Δ")
    ax.set_ylabel("Скачков (>1%)")
    ax.set_title(
        f"Скачков всего: {sweep['jump_count']}", fontsize=v["hist_title_fontsize"] + 2
    )
    ax.axvline(x=0, color=v["ref_line_color"], ls=v["ref_line_ls"])
    ax.grid(alpha=v["grid_alpha"])
    plt.tight_layout()
    plt.savefig(f"{out_dir}/jumps_analysis.png", dpi=v["dpi_default"])
    plt.close()
