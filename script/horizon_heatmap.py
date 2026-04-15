#!/usr/bin/env python3
"""
Horizon heatmap visualization.

Displays the occupancy rate (percentage of pixels above threshold)
for each class across all threshold values as a heatmap.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    """
    Render horizon heatmap visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    number_of_classes = data["number_of_classes"]
    threshold_values = sweep["thresholds"]
    occupancy_rates = sweep["occupancy_rates"].cpu().numpy()

    figure_width, figure_height = configuration["figure_heatmap_wide"]
    figure, axis = plt.subplots(figsize=(figure_width, figure_height))

    image = axis.imshow(
        occupancy_rates.T,
        aspect="auto",
        cmap=configuration["colormap_heatmap"],
        origin="lower",
        extent=[threshold_values[0], threshold_values[-1], 0, number_of_classes],
        vmin=configuration["heatmap_vmin"],
        vmax=configuration["heatmap_vmax"],
    )

    axis.set_yticks(range(number_of_classes))
    axis.set_yticklabels([f"Class {class_id}" for class_id in range(number_of_classes)])
    axis.set_xlabel("Threshold Value")
    figure.colorbar(image, ax=axis)

    plt.tight_layout()
    plt.savefig(f"{out_dir}/horizon_heatmap.png", dpi=configuration["dpi_default"])
    plt.close()
