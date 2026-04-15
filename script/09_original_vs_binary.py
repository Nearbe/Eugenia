#!/usr/bin/env python3
"""09: Сравнение исходного vs бинаризация."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    is_color = data.get("is_color", False)
    color_space = data.get("color_space", "RGB")
    symbol_names = data.get("symbol_names", None)

    if is_color:
        if color_space == "CMYK":
            channel_colors = ["#00FFFF", "#FF00FF", "#FFFF00", "#808080"]
        else:
            channel_colors = ["#FF0000", "#00FF00", "#0000FF"]
    else:
        channel_colors = [v["cmap_gray"]] * n_classes

    cthr = v["original_vs_binary"]
    n_cols = len(cthr) + 1
    fig, axes = plt.subplots(
        n_classes, n_cols, figsize=(2 * n_cols, max(1.2 * n_classes, 3))
    )
    if n_classes == 1:
        axes = axes.reshape(1, -1)

    for i in range(n_classes):
        d_img = symbols[i].cpu().numpy()

        if is_color:
            axes[i, 0].imshow(
                d_img,
                cmap=plt.cm.colors.LinearSegmentedColormap.from_list(
                    "channel_cmap", ["black", channel_colors[i]]
                ),
            )
        else:
            axes[i, 0].imshow(d_img, cmap=v["cmap_gray"])

        label = symbol_names[i] if symbol_names else f"#{i}"
        axes[i, 0].set_ylabel(label, rotation=0, ha="right")
        axes[i, 0].set_xticks([])
        axes[i, 0].set_yticks([])

        for j, t in enumerate(cthr):
            mask = (d_img > t).astype(float)
            if is_color:
                rgb = np.zeros((mask.shape[0], mask.shape[1], 3))
                hex_color = channel_colors[i].lstrip("#")
                r, g, b = (
                    int(hex_color[0:2], 16) / 255,
                    int(hex_color[2:4], 16) / 255,
                    int(hex_color[4:6], 16) / 255,
                )
                rgb[:, :, 0] = mask * r
                rgb[:, :, 1] = mask * g
                rgb[:, :, 2] = mask * b
                axes[i, j + 1].imshow(rgb)
            else:
                axes[i, j + 1].imshow(mask, cmap=v["cmap_binary"])
            axes[i, j + 1].set_title(f"Δ>{t:+.0f}", fontsize=8)
            axes[i, j + 1].axis("off")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/09_original_vs_binary.png", dpi=v["dpi_high"])
    plt.close()
