#!/usr/bin/env python3
"""Euler characteristic analysis."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    np.random.seed(42)
    thr = np.linspace(v["sweep_min"], v["sweep_max"], v["betti_n_thr_default"])
    eu, b0 = np.zeros(len(thr)), np.zeros(len(thr))
    for j, t in enumerate(thr):
        for c in range(n_classes):
            sym = symbols[c].cpu().numpy()
            ba = (sym > t).astype(np.uint8)
            _, nc = ndimage.label(ba)
            eu[j] += nc
            b0[j] += nc
    eu /= n_classes
    b0 /= n_classes
    fig, axes = plt.subplots(1, 3, figsize=(v["fig_euler_w"], v["fig_euler_h"]))
    axes[0].plot(thr, eu, color="purple", lw=v["marker_size"])
    axes[0].set_xlabel("Δ")
    axes[0].set_ylabel("χ")
    axes[0].grid(alpha=v["grid_alpha"])
    axes[1].plot(thr, b0, color="steelblue", lw=v["marker_size"])
    axes[1].set_xlabel("Δ")
    axes[1].set_ylabel("Betti-0")
    axes[1].grid(alpha=v["grid_alpha"])
    axes[2].plot(
        thr, np.abs(np.gradient(eu, thr)), color="darkorange", lw=v["marker_size"]
    )
    axes[2].set_xlabel("Δ")
    axes[2].set_ylabel("|dχ/dΔ|")
    axes[2].grid(alpha=v["grid_alpha"])
    plt.tight_layout()
    plt.savefig(f"{out_dir}/euler_persistence.png", dpi=v["dpi_default"])
    plt.close()
