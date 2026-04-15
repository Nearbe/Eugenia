#!/usr/bin/env python3
"""Phase volume visualization."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    n_show = min(v["surface_n_samples"], n_classes)
    key_thresholds = [-5.0, -2.0, 0.0, 2.0, 4.0]
    fig = plt.figure(figsize=(v["fig_phase_w"], v["fig_phase_h"]))
    gs = fig.add_gridspec(1, n_show)
    for i in range(n_show):
        d_img = symbols[i].cpu().numpy()
        H, W = d_img.shape
        ax = fig.add_subplot(gs[i], projection="3d")
        X, Y = np.meshgrid(range(W), range(H))
        for j, t in enumerate(key_thresholds):
            mask = (d_img > t).astype(float)
            if mask.sum() > 0:
                Z = mask * (j + 1)
                ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.3)
        ax.set_title(f"#{i}")
        ax.set_zlim(0, len(key_thresholds) + 1)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/phase_volume.png", dpi=v["dpi_default"])
    plt.close()
