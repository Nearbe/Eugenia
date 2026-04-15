#!/usr/bin/env python3
"""individual: Отдельные гистограммы Δ по классам."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    hist_dir = os.path.join(out_dir, "individual_hists")
    os.makedirs(hist_dir, exist_ok=True)
    for c in range(n_classes):
        vals = symbols[c].cpu().numpy().flatten()
        fig_w = v["fig_individual_w"] * v["individual_fig_w_factor"]
        fig_h = v["fig_individual_h"] * v["individual_fig_h_factor"]
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        ax.hist(
            vals,
            bins=v["hist_bins_default"],
            color=v["hist_color"],
            alpha=v["hist_alpha"],
        )
        ax.set_title(f"Класс {c} (n={vals.size})")
        ax.set_xlabel("Δ")
        ax.set_ylabel("count")
        ax.axvline(
            x=v["hist_ref_line_x"],
            color=v["ref_line_color"],
            ls=v["ref_line_ls"],
            lw=v["ref_line_lw"],
        )
        plt.tight_layout()
        plt.savefig(f"{hist_dir}/class_{c}_individual.png", dpi=v["dpi_individual"])
        plt.close()
