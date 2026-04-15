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


#!/usr/bin/env python3
"""07: CDF по классам."""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    thr = sweep["thresholds"]
    fig, ax = plt.subplots(figsize=(v["fig_cdf_w"], v["fig_cdf_h"]))
    for c in range(n_classes):
        vals = symbols[c].cpu().numpy().flatten()
        cdf = np.array([np.mean(vals <= t) for t in thr])
        ax.plot(thr, cdf, label=str(c), linewidth=1.5)
    ax.set_xlabel("Δ")
    ax.set_ylabel("CDF")
    ax.legend(fontsize=8, ncol=(n_classes + 4) // 5)
    ax.grid(alpha=v["grid_alpha"])
    plt.tight_layout()
    plt.savefig(f"{out_dir}/07_cdf_by_class.png", dpi=v["dpi_default"])
    plt.close()


#!/usr/bin/env python3
"""08: Масштабы информационного поля."""
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    b = sweep["bits_tr_all"].cpu().numpy()
    thr = sweep["thresholds"]

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()

    I = np.sum(b, axis=1)
    axes[0].plot(thr, I, color="green")
    axes[0].fill_between(thr, 0, I, alpha=0.3, color="green")
    axes[0].set_title("I — Информационная ёмкость (глобальный)")
    axes[0].set_ylabel("∑ bits")

    Q = np.sum(b**2, axis=1)
    axes[1].plot(thr, Q, color="blue")
    axes[1].fill_between(thr, 0, Q, alpha=0.3, color="blue")
    axes[1].set_title("Q — Структурная сложность (локальный)")
    axes[1].set_ylabel("∑ bits²")

    rho = np.sum(b**3, axis=1)
    axes[2].plot(thr, rho, color="red")
    axes[2].fill_between(thr, 0, rho, alpha=0.3, color="red")
    axes[2].set_title("ρ — Плотность состояния (точечный)")
    axes[2].set_ylabel("∑ bits³")

    M = np.sum(b**4, axis=1)
    axes[3].plot(thr, M, color="purple")
    axes[3].fill_between(thr, 0, M, alpha=0.3, color="purple")
    axes[3].set_title("M — Мера поля (интегральный)")
    axes[3].set_ylabel("∑ bits⁴")

    for ax in axes:
        ax.set_xlabel("Порог Δ")
        ax.axvline(x=0, color="gray", ls="--")
        ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{out_dir}/08_entropy_analysis.png", dpi=120)
    plt.close()
