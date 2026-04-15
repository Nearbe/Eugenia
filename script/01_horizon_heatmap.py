#!/usr/bin/env python3
"""01: Тепловая карта горизонта."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    v = data["viz"]
    n_classes = data["n_classes"]
    thr = sweep["thresholds"]
    bits = sweep["bits_tr_all"].cpu().numpy()
    fig, ax = plt.subplots(figsize=(v["fig_heatmap_wide_w"], v["fig_heatmap_wide_h"]))
    im = ax.imshow(
        bits.T,
        aspect="auto",
        cmap=v["cmap_heatmap"],
        origin="lower",
        extent=[thr[0], thr[-1], 0, n_classes],
        vmin=v["heatmap_vmin"],
        vmax=v["heatmap_vmax"],
    )
    ax.set_yticks(range(n_classes))
    ax.set_yticklabels([f"Класс {c}" for c in range(n_classes)])
    ax.set_xlabel("Порог Δ")
    fig.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/01_horizon_heatmap.png", dpi=v["dpi_default"])
    plt.close()
