#!/usr/bin/env python3
"""Stress map (gradient magnitude)."""

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
    fig, axes = plt.subplots(
        1, n_show, figsize=(n_show * 4, 5), subplot_kw={"projection": "3d"}
    )
    axes = axes if n_show > 1 else [axes]
    for i in range(n_show):
        d_img = symbols[i].cpu().numpy()
        H, W = d_img.shape
        if H < 2 or W < 2:
            axes[i].scatter([0], [0], [d_img.flatten().mean()], c="red", s=50)
            axes[i].set_title(f"#{i} (микробъект)")
            continue
        gy, gx = np.gradient(d_img)
        grad_mag = np.sqrt(gx**2 + gy**2)
        X, Y = np.meshgrid(range(W), range(H))
        axes[i].plot_surface(
            X, Y, grad_mag, cmap=v["cmap_heatmap"], alpha=0.9, edgecolor="none"
        )
        axes[i].set_title(f"#{i} (Напряжение)")
        axes[i].set_zlim(0, grad_mag.max())
    plt.tight_layout()
    plt.savefig(f"{out_dir}/stress_map.png", dpi=v["dpi_default"])
    plt.close()
