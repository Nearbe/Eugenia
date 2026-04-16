#!/usr/bin/env python3
"""
Topological Class Correlation Analysis.

Calculates and visualizes the Pearson correlation between the
occupancy profiles of different classes across the entire threshold sweep.
"""

import logging

import matplotlib.pyplot as plt
import numpy as np

from utils.viz_utils import save_visualization, get_symbol_label

logger = logging.getLogger(__name__)


def render(data, sweep, out_dir):
    """
    Render class correlation heatmap.
    """
    configuration = data["config"]
    occupancy_rates = sweep.occupancy_rates.cpu().numpy()  # [n_thresholds, n_classes]
    num_classes = data["number_of_classes"]

    if num_classes < 2:
        logger.info("  Skipping correlation: not enough classes")
        return

    # Compute Pearson correlation matrix
    # occupancy_rates.T is (n_classes, n_thresholds)
    corr_matrix = np.corrcoef(occupancy_rates.T)

    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1)

    # Add labels
    labels = [get_symbol_label(i, data) for i in range(num_classes)]
    ax.set_xticks(np.arange(num_classes))
    ax.set_yticks(np.arange(num_classes))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_yticklabels(labels)

    # Add values in the cells
    for i in range(num_classes):
        for j in range(num_classes):
            val = corr_matrix[i, j]
            ax.text(j, i, f"{val:.2f}",
                    ha="center", va="center",
                    color="white" if abs(val) > 0.5 else "black")

    ax.set_title("Topological Class Similarity (Occupancy Correlation)", fontsize=16)
    plt.colorbar(im, ax=ax)
    plt.tight_layout()

    description = (
        "Topological Class Correlation: Measures the Pearson correlation between the "
        "occupancy profiles of different classes. High correlation indicates similar "
        "structural response to thresholding, suggesting topological similarity."
    )
    save_visualization("18_class_correlation.png", out_dir, configuration, "dpi_default", description=description)
    logger.info("  Created class correlation heatmap")


if __name__ == "__main__":
    pass
