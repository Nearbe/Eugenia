#!/usr/bin/env python3
"""Information field scales (I, Q, ρ, M)."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    v = data["viz"]
    b = sweep["bits_tr_all"].cpu().numpy()
    thr = sweep["thresholds"]

    fig, axes = plt.subplots(2, 2, figsize=(v["fig_entropy_w"], v["fig_entropy_h"]))
    axes = axes.flatten()

    I = np.sum(b, axis=1)
    axes[0].plot(thr, I, color="green")
    axes[0].fill_between(thr, 0, I, alpha=v["hist_alpha"], color="green")
    axes[0].set_title("I — Информационная ёмкость (глобальный)")
    axes[0].set_ylabel("∑ bits")

    Q = np.sum(b**2, axis=1)
    axes[1].plot(thr, Q, color="blue")
    axes[1].fill_between(thr, 0, Q, alpha=v["hist_alpha"], color="blue")
    axes[1].set_title("Q — Структурная сложность (локальный)")
    axes[1].set_ylabel("∑ bits²")

    rho = np.sum(b**3, axis=1)
    axes[2].plot(thr, rho, color="red")
    axes[2].fill_between(thr, 0, rho, alpha=v["hist_alpha"], color="red")
    axes[2].set_title("ρ — Плотность состояния (точечный)")
    axes[2].set_ylabel("∑ bits³")

    M = np.sum(b**4, axis=1)
    axes[3].plot(thr, M, color="purple")
    axes[3].fill_between(thr, 0, M, alpha=v["hist_alpha"], color="purple")
    axes[3].set_title("M — Мера поля (интегральный)")
    axes[3].set_ylabel("∑ bits⁴")

    for ax in axes:
        ax.set_xlabel("Порог Δ")
        ax.axvline(x=0, color=v["ref_line_color"], ls=v["ref_line_ls"])
        ax.grid(alpha=v["grid_alpha"])

    plt.tight_layout()
    plt.savefig(f"{out_dir}/entropy_analysis.png", dpi=v["dpi_default"])
    plt.close()
