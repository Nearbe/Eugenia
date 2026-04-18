#!/usr/bin/env python3
"""
Visualization renderer to display all extracted symbols in a grid.

This module generates a grid visualization of the delta field for every
extracted symbol (class) across the entire image area.
"""

import os
from typing import Dict

import matplotlib.pyplot as plt

from utils.viz_utils import get_symbol_label, save_visualization


def render(data: Dict, sweep: Dict, out_dir: str):
    """
    Render the symbol grid visualization.

    Args:
        data: Dictionary containing loaded data and configuration (VisualizationData).
        sweep: Dictionary containing threshold sweep results (SweepResults).
        out_dir: Output directory for saving the figure.
    """
    configuration = data["config"]
    symbol_delta_fields = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]

    # Create folder for individual symbol grid images directly in the source output directory
    grid_dir = os.path.join(out_dir, "symbol_grids")
    os.makedirs(grid_dir, exist_ok=True)

    print(f"Generating Symbol Grid visualizations in: {grid_dir}")

    for idx in range(number_of_classes):
        delta_image = symbol_delta_fields[idx].cpu().numpy()
        h, w = delta_image.shape

        plt.figure(figsize=(10, 2))

        plt.title(f"Delta Field for Class: {get_symbol_label(idx, data)}")

        # Display the delta field as a heatmap
        plt.imshow(delta_image, cmap=configuration["colormap_heatmap"], interpolation="nearest")

        # Add a colorbar for reference
        plt.colorbar(label="Delta Value")

        save_visualization(
            f"{idx}_delta_grid.png",
            grid_dir,
            configuration,
            "dpi_default",
            description=f"Delta field visualization for class {get_symbol_label(idx, data)}.",
        )
        plt.close()

    print("Symbol Grid rendering complete.")
