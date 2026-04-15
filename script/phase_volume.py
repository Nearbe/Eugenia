#!/usr/bin/env python3
"""
Phase volume visualization.

Displays multiple binary threshold layers stacked in 3D, showing how the
volume occupied by the delta field changes as the threshold increases.
Each layer represents a different threshold level.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def render(data, sweep, out_dir):
    """
    Render phase volume visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    symbols = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]

    # Limit number of displayed classes
    display_count = min(configuration["surface_samples"], number_of_classes)

    # Key threshold levels to visualize
    key_thresholds = [-5.0, -2.0, 0.0, 2.0, 4.0]

    figure = plt.figure(figsize=configuration["figure_phase"])
    grid_layout = figure.add_gridspec(1, display_count)

    for index in range(display_count):
        delta_image = symbols[index].cpu().numpy()
        image_height, image_width = delta_image.shape

        axis = figure.add_subplot(grid_layout[index], projection="3d")

        horizontal_axis, vertical_axis = np.meshgrid(
            range(image_width), range(image_height)
        )

        # Plot each threshold level as a layer
        for layer_index, threshold_value in enumerate(key_thresholds):
            binary_mask = (delta_image > threshold_value).astype(float)

            if binary_mask.sum() > 0:
                # Elevate each layer to its position in the stack
                layer_elevation = binary_mask * (layer_index + 1)
                axis.plot_surface(
                    horizontal_axis,
                    vertical_axis,
                    layer_elevation,
                    cmap="viridis",
                    alpha=0.3,
                )

        axis.set_title(f"Class {index}")
        axis.set_zlim(0, len(key_thresholds) + 1)

    plt.tight_layout()
    plt.savefig(f"{out_dir}/phase_volume.png", dpi=configuration["dpi_default"])
    plt.close()
