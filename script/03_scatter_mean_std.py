#!/usr/bin/env python3
"""03: Scatterplot mean/std по классам."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    ms, ss = [], []
    for c in range(n_classes):
        v = symbols[c].cpu().numpy().flatten()
        ms.append(v.mean())
        ss.append(v.std())
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = plt.cm.tab20(np.linspace(0, 1, n_classes))
    ax.scatter(ms, ss, c=range(n_classes), s=80, cmap="tab20")
    for c in range(n_classes):
        label = str(c) if n_classes <= 20 else f"#{c}"
        ax.annotate(label, (ms[c], ss[c]), fontsize=10, fontweight="bold")
    ax.set_xlabel("Среднее Δ")
    ax.set_ylabel("Std Δ")
    ax.grid(alpha=0.3)
    ax.set_title(f"{n_classes} классов")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/03_scatter_mean_std.png", dpi=120)
    plt.close()
