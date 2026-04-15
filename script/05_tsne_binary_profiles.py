#!/usr/bin/env python3
"""05: t-SNE бинарных профилей."""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def render(data, sweep, out_dir):
    v = data["viz"]
    bits = sweep["bits_tr_all"].cpu().numpy()
    y = data["y_train"].cpu().numpy()
    n_classes = int(y.max()) + 1
    profiles = bits.T
    fig, ax = plt.subplots(figsize=(v["fig_tsne_w"], v["fig_tsne_h"]))
    perplexity = min(v["tsne_perplexity"], n_classes - 1)
    if n_classes >= 2:
        tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
        coords = tsne.fit_transform(profiles)
        ax.scatter(coords[:, 0], coords[:, 1], c=range(n_classes), s=50, cmap="tab20")
        for c in range(n_classes):
            ax.annotate(
                str(c), (coords[c, 0], coords[c, 1]), fontsize=10, fontweight="bold"
            )
    ax.set_title(f"t-SNE профилей ({n_classes} классов)")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/05_tsne_binary_profiles.png", dpi=v["dpi_default"])
    plt.close()
