#!/usr/bin/env python3
"""Betti-1 holes detection."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    thr = np.linspace(v["betti_thr_min"], v["betti_thr_max"], v["betti_n_thr"])
    b1 = {c: [] for c in range(n_classes)}
    for c in range(n_classes):
        sym = symbols[c].cpu().numpy()
        for t in thr:
            ba = (sym > t).astype(np.uint8)
            p = np.pad(ba, v["betti_pad"], mode="constant")
            lb, nb = ndimage.label(1 - p)
            edge = set(lb[0, :]) | set(lb[-1, :]) | set(lb[:, 0]) | set(lb[:, -1])
            edge.discard(0)
            b1[c].append(max(v["betti_holes_min"], nb - len(edge)))
    fig, ax = plt.subplots(figsize=(v["fig_betti_w"], v["fig_betti_h"]))
    for c in range(n_classes):
        ax.plot(thr, b1[c], "s-", ms=2, label=str(c))
    ax.set_xlabel("Порог Δ")
    ax.set_ylabel("Дырок")
    ax.legend(fontsize=8)
    ax.grid(alpha=v["grid_alpha"])
    plt.tight_layout()
    plt.savefig(f"{out_dir}/betti1_holes.png", dpi=v["dpi_high"])
    plt.close()
