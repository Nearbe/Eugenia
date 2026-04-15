#!/usr/bin/env python3
"""12: Характеристика Эйлера."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage


def render(data, sweep, out_dir):
    v = data["viz"]
    symbols = data["symbols_delta"]
    n_classes = data["n_classes"]
    np.random.seed(42)
    thr = np.linspace(v["sweep_min"], v["sweep_max"], v["betti_n_thr_default"])
    eu, b0 = np.zeros(len(thr)), np.zeros(len(thr))
    for j, t in enumerate(thr):
        for c in range(n_classes):
            sym = symbols[c].cpu().numpy()
            ba = (sym > t).astype(np.uint8)
            _, nc = ndimage.label(ba)
            eu[j] += nc
            b0[j] += nc
    eu /= n_classes
    b0 /= n_classes
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].plot(thr, eu, color="purple", lw=1.5)
    axes[0].set_xlabel("Δ")
    axes[0].set_ylabel("χ")
    axes[0].grid(alpha=0.3)
    axes[1].plot(thr, b0, color="steelblue", lw=1.5)
    axes[1].set_xlabel("Δ")
    axes[1].set_ylabel("Betti-0")
    axes[1].grid(alpha=0.3)
    axes[2].plot(thr, np.abs(np.gradient(eu, thr)), color="darkorange", lw=1.5)
    axes[2].set_xlabel("Δ")
    axes[2].set_ylabel("|dχ/dΔ|")
    axes[2].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/12_euler_persistence_complexity.png", dpi=120)
    plt.close()


#!/usr/bin/env python3
"""13: Ландшафт Персистенции."""
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
    plt.savefig(f"{out_dir}/13_persistence_landscape.png", dpi=v["dpi_default"])
    plt.close()


#!/usr/bin/env python3
"""14: Карта Напряжений."""
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
    plt.savefig(f"{out_dir}/14_stress_map.png", dpi=v["dpi_default"])
    plt.close()


#!/usr/bin/env python3
"""15: Фазовый Объем."""
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
    plt.savefig(f"{out_dir}/15_phase_volume.png", dpi=v["dpi_default"])
    plt.close()
