#!/usr/bin/env python3
"""Horizon animation."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


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
        channel_colors = [v["cmap_binary"]] * n_classes

    thr = sweep["thresholds"]
    n_frames = v["anim_n_frames"]
    anim_dir = os.path.join(out_dir, "anim_frames")
    os.makedirs(anim_dir, exist_ok=True)
    frame_idxs = np.linspace(0, len(thr) - 1, n_frames).astype(int)
    n_cols_anim = min(v["anim_grid_cols"], n_classes)
    n_rows_anim = (n_classes + n_cols_anim - 1) // n_cols_anim
    for fi, ti in enumerate(frame_idxs):
        fig, axes = plt.subplots(
            n_rows_anim,
            n_cols_anim,
            figsize=(v["fig_animation_w"], v["fig_animation_h"]),
        )
        axes = axes.flatten() if hasattr(axes, "flatten") else [axes]
        t = thr[ti]
        for c in range(n_classes):
            sym = symbols[c].cpu().numpy()
            mask = (sym > t).astype(float)
            if is_color:
                rgb = np.zeros((mask.shape[0], mask.shape[1], 3))
                hex_color = channel_colors[c].lstrip("#")
                r, g, b = (
                    int(hex_color[0:2], 16) / 255,
                    int(hex_color[2:4], 16) / 255,
                    int(hex_color[4:6], 16) / 255,
                )
                rgb[:, :, 0] = mask * r
                rgb[:, :, 1] = mask * g
                rgb[:, :, 2] = mask * b
                axes[c].imshow(rgb)
            else:
                axes[c].imshow(mask, cmap=channel_colors[c])
            label = symbol_names[c] if symbol_names else str(c)
            axes[c].set_title(f"{label}  Δ>{t:.1f}", fontsize=9)
            axes[c].axis("off")
        for c in range(n_classes, len(axes)):
            axes[c].axis("off")
        plt.tight_layout()
        plt.savefig(f"{anim_dir}/frame_{fi:04d}.png", dpi=v["dpi_low"])
        plt.close()
    try:
        from PIL import Image

        frames = [Image.open(f"{anim_dir}/frame_{i:04d}.png") for i in range(n_frames)]
        frames[0].save(
            f"{out_dir}/horizon_animation.gif",
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
        )
    except:
        pass
