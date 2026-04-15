#!/usr/bin/env python3
"""Persistence landscape visualization."""

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
        persist = (d_img - d_img.min()) / (d_img.max() - d_img.min() + 1e-10)
        mask = persist > 0.1
        X, Y = np.meshgrid(range(W), range(H))
        Z = np.where(mask, d_img, np.nan)
        axes[i].plot_surface(X, Y, Z, cmap=v["cmap_3d"], alpha=0.9, edgecolor="none")
        axes[i].set_title(f"#{i} (Скелет)")
        axes[i].set_zlim(d_img.min(), d_img.max())
    plt.tight_layout()
    plt.savefig(f"{out_dir}/persistence_landscape.png", dpi=v["dpi_default"])
    plt.close()
