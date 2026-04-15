#!/usr/bin/env python3
"""12: Характеристика Эйлера."""

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
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].plot(thr, eu, color="purple", lw=1.5)
    axes[0].set_xlabel("Δ")
    axes[0].set_ylabel("χ")
    axes[0].grid(alpha=0.3)
    axes[1].plot(thr, b0, color="steelblue", lw=1.5)
    axes[1].set_xlabel("Δ")
    axes[1].set_ylabel("Betti-0")
    axes[1].grid(alpha=0.3)
    axes[2].plot(thr, np.abs(np.gradient(eu, thr)), color="darkorange", lw=1.5)
    axes[2].set_xlabel("Δ")
    axes[2].set_ylabel("|dχ/dΔ|")
    axes[2].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/12_euler_persistence_complexity.png", dpi=120)
    plt.close()
