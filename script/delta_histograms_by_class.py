#!/usr/bin/env python3
"""Delta histograms by class."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    n_cols = v["hist_grid_cols"]
    n_rows = (n_classes + n_cols - 1) // n_cols
    fig_h = max(v["fig_hist_wide_h"], n_rows * v["hist_row_height"])
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(v["fig_hist_wide_w"], fig_h))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]
    for c in range(n_classes):
        vals = symbols[c].cpu().numpy().flatten()
        axes[c].hist(vals, bins=v["hist_bins_default"], color="steelblue", alpha=0.7)
        axes[c].set_title(
            f"Класс {c} (n={vals.size})", fontsize=v["hist_title_fontsize"]
        )
        axes[c].set_xlabel("Δ")
        axes[c].set_ylabel("count")
        axes[c].axvline(
            x=v["hist_ref_line_x"],
            color=v["ref_line_color"],
            ls=v["ref_line_ls"],
            lw=v["ref_line_lw"],
        )
    for c in range(n_classes, len(axes)):
        axes[c].axis("off")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/delta_histograms_by_class.png", dpi=v["dpi_default"])
    plt.close()
