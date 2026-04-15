#!/usr/bin/env python3
"""Scatter plot mean/std by class."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    ms, ss = [], []
    for c in range(n_classes):
        vals = symbols[c].cpu().numpy().flatten()
        ms.append(vals.mean())
        ss.append(vals.std())
    fig, ax = plt.subplots(figsize=(v["fig_scatter_w"], v["fig_scatter_h"]))
    colors = plt.cm.tab20(np.linspace(0, 1, n_classes))
    ax.scatter(ms, ss, c=range(n_classes), s=80, cmap="tab20")
    for c in range(n_classes):
        label = str(c) if n_classes <= 20 else f"#{c}"
        ax.annotate(label, (ms[c], ss[c]), fontsize=10, fontweight="bold")
    ax.set_xlabel("Среднее Δ")
    ax.set_ylabel("Std Δ")
    ax.grid(alpha=v["grid_alpha"])
    ax.set_title(f"{n_classes} классов")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/scatter_mean_std.png", dpi=v["dpi_default"])
    plt.close()
