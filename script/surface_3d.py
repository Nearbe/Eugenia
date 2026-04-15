#!/usr/bin/env python3
"""
3D surface visualization.

Displays delta field values as 3D surface plots for each class,
showing the topological structure of the delta field.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Colormaps for different color spaces
CMYK_COLORMAPS = ["Blues", "Purples", "YlOrBr", "Greys"]
RGB_COLORMAPS = ["Reds", "Greens", "Blues"]


def render(data, sweep, out_dir):
    """
    Render 3D surface visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    symbols = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]
    is_color = data.get("is_color", False)
    color_space = data.get("color_space", "Grayscale")
    symbol_names = data.get("symbol_names", None)

    # Select colormaps based on data type
    if is_color:
        if color_space == "CMYK":
            channel_colormaps = CMYK_COLORMAPS
        else:
            channel_colormaps = RGB_COLORMAPS
    else:
        channel_colormaps = [configuration["colormap_3d"]] * number_of_classes

    # Limit number of displayed classes
    display_count = min(configuration["surface_samples"], number_of_classes)

    figure = plt.figure(figsize=configuration["figure_3d_multi"])

    for index in range(display_count):
        delta_image = symbols[index].cpu().numpy()
        height, width = delta_image.shape

        axis = figure.add_subplot(1, display_count, index + 1, projection="3d")

        horizontal_axis, vertical_axis = np.meshgrid(range(width), range(height))
        axis.plot_surface(
            horizontal_axis,
            vertical_axis,
            delta_image,
            cmap=channel_colormaps[index],
            alpha=configuration["colormap_3d_alpha"],
        )

        label = symbol_names[index] if symbol_names else f"#{index}"
        axis.set_title(label)

        # Set consistent z-axis range
        if delta_image.min() == delta_image.max():
            axis.set_zlim(delta_image.min() - 1, delta_image.max() + 1)
        else:
            axis.set_zlim(delta_image.min(), delta_image.max())

    plt.tight_layout()
    plt.savefig(f"{out_dir}/surface_3d.png", dpi=configuration["dpi_default"])
    plt.close()
