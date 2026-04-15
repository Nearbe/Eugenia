#!/usr/bin/env python3
"""
Stress map (gradient magnitude) visualization.

Computes and displays the gradient magnitude of each delta field,
showing areas of high "stress" (rapid change) as 3D surfaces.
The gradient magnitude indicates how quickly values change,
which relates to the local complexity of the delta field.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def render(data, sweep, out_dir):
    """
    Render stress map visualization.

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

        # Skip very small images
        if image_height < 2 or image_width < 2:
            axes[index].scatter([0], [0], [delta_image.flatten().mean()], c="red", s=50)
            axes[index].set_title(f"Class {index} (Small Object)")
            continue

        # Compute gradient magnitude
        vertical_gradient, horizontal_gradient = np.gradient(delta_image)
        gradient_magnitude = np.sqrt(horizontal_gradient**2 + vertical_gradient**2)

        # Create mesh grid
        horizontal_axis, vertical_axis = np.meshgrid(
            range(image_width), range(image_height)
        )

        axes[index].plot_surface(
            horizontal_axis,
            vertical_axis,
            gradient_magnitude,
            cmap=configuration["colormap_heatmap"],
            alpha=0.9,
            edgecolor="none",
        )
        axes[index].set_title(f"Class {index} (Stress)")
        axes[index].set_zlim(0, gradient_magnitude.max())

    plt.tight_layout()
    plt.savefig(f"{out_dir}/stress_map.png", dpi=configuration["dpi_default"])
    plt.close()
