#!/usr/bin/env python3
"""07: CDF по классам."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    thr = sweep["thresholds"]
    fig, ax = plt.subplots(figsize=(v["fig_cdf_w"], v["fig_cdf_h"]))
    for c in range(n_classes):
        vals = symbols[c].cpu().numpy().flatten()
        cdf = np.array([np.mean(vals <= t) for t in thr])
        ax.plot(thr, cdf, label=str(c), linewidth=1.5)
    ax.set_xlabel("Δ")
    ax.set_ylabel("CDF")
    ax.legend(fontsize=8, ncol=(n_classes + 4) // 5)
    ax.grid(alpha=v["grid_alpha"])
    plt.tight_layout()
    plt.savefig(f"{out_dir}/07_cdf_by_class.png", dpi=v["dpi_default"])
    plt.close()
