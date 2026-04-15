#!/usr/bin/env python3
"""06: 3D поверхности Δ."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    is_color = data.get("is_color", False)
    color_space = data.get("color_space", "RGB")
    symbol_names = data.get("symbol_names", None)

    if is_color:
        if color_space == "CMYK":
            channel_cmaps = ["Blues", "Purples", "YlOrBr", "Greys"]
        else:
            channel_cmaps = ["Reds", "Greens", "Blues"]
    else:
        channel_cmaps = [v["cmap_3d"]] * n_classes

    n_show = min(v["surface_n_samples"], n_classes)
    fig = plt.figure(figsize=(v["fig_3d_multi_w"], v["fig_3d_multi_h"]))
    for i in range(n_show):
        d_img = symbols[i].cpu().numpy()
        H, W = d_img.shape
        ax = fig.add_subplot(1, n_show, i + 1, projection="3d")
        X, Y = np.meshgrid(range(W), range(H))
        ax.plot_surface(X, Y, d_img, cmap=channel_cmaps[i], alpha=v["cmap_3d_alpha"])
        label = symbol_names[i] if symbol_names else f"#{i}"
        ax.set_title(label)
        if d_img.min() == d_img.max():
            ax.set_zlim(d_img.min() - 1, d_img.max() + 1)
        else:
            ax.set_zlim(d_img.min(), d_img.max())
    plt.tight_layout()
    plt.savefig(f"{out_dir}/06_3d_surface.png", dpi=v["dpi_default"])
    plt.close()
