#!/usr/bin/env python3
"""
Persistence landscape visualization.

Displays the "skeleton" of each delta field by filtering out low-persistence
regions. Shows only the most significant topological features as a 3D surface.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def render(data, sweep, out_dir):
    """
    Render persistence landscape visualization.

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

    figure, axes = plt.subplots(
        1,
        display_count,
        figsize=(display_count * 4, 5),
        subplot_kw={"projection": "3d"},
    )
    axes = axes if display_count > 1 else [axes]

    for index in range(display_count):
        delta_image = symbols[index].cpu().numpy()
        image_height, image_width = delta_image.shape

        # Normalize and filter by persistence threshold
        normalized = (delta_image - delta_image.min()) / (
            delta_image.max() - delta_image.min() + 1e-10
        )
        persistence_mask = normalized > configuration["persistence_threshold"]

        # Create mesh grid
        horizontal_axis, vertical_axis = np.meshgrid(
            range(image_width), range(image_height)
        )

        # Apply mask (set filtered values to NaN)
        filtered_surface = np.where(persistence_mask, delta_image, np.nan)

        axes[index].plot_surface(
            horizontal_axis,
            vertical_axis,
            filtered_surface,
            cmap=configuration["colormap_3d"],
            alpha=0.9,
            edgecolor="none",
        )
        axes[index].set_title(f"Class {index} (Skeleton)")
        axes[index].set_zlim(delta_image.min(), delta_image.max())

    plt.tight_layout()
    plt.savefig(
        f"{out_dir}/persistence_landscape.png", dpi=configuration["dpi_default"]
    )
    plt.close()
