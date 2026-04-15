#!/usr/bin/env python3
"""
Scatter plot of mean vs standard deviation by class.

Visualizes the distribution of delta field values for each class
by plotting mean (x-axis) vs standard deviation (y-axis).
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    """
    Render scatter plot of mean vs std for each class.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    symbols = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]

    # Calculate mean and standard deviation for each class
    mean_values = []
    std_values = []

    for class_id in range(number_of_classes):
        values = symbols[class_id].cpu().numpy().flatten()
        mean_values.append(values.mean())
        std_values.append(values.std())

    # Create scatter plot
    figure, axis = plt.subplots(figsize=configuration["figure_scatter"])

    scatter = axis.scatter(
        mean_values, std_values, c=range(number_of_classes), s=80, cmap="tab20"
    )

    # Add class labels
    for class_id in range(number_of_classes):
        label = str(class_id) if number_of_classes <= 20 else f"#{class_id}"
        axis.annotate(
            label,
            (mean_values[class_id], std_values[class_id]),
            fontsize=10,
            fontweight="bold",
        )

    axis.set_xlabel("Mean Delta")
    axis.set_ylabel("Standard Deviation")
    axis.grid(alpha=configuration["alpha_grid"])
    axis.set_title(f"{number_of_classes} Classes")

    plt.tight_layout()
    plt.savefig(f"{out_dir}/scatter_mean_std.png", dpi=configuration["dpi_default"])
    plt.close()
