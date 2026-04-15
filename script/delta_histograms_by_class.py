#!/usr/bin/env python3
"""
Delta histograms by class.

Displays histogram of delta field values for each class in a grid layout.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    """
    Render delta field histograms for all classes.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    symbols = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]

    columns = configuration["grid_columns"]
    rows = (number_of_classes + columns - 1) // columns
    figure_height = max(
        configuration["figure_wide"][1], rows * configuration["grid_row_height"]
    )
    figure_width = configuration["figure_wide"][0]

    figure, axes = plt.subplots(rows, columns, figsize=(figure_width, figure_height))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for class_id in range(number_of_classes):
        values = symbols[class_id].cpu().numpy().flatten()
        axes[class_id].hist(
            values,
            bins=configuration["histogram_bins"],
            color=configuration["color_histogram"],
            alpha=configuration["alpha_default"],
        )
        axes[class_id].set_title(
            f"Class {class_id} (n={values.size})",
            fontsize=configuration["figure_title_fontsize"],
        )
        axes[class_id].set_xlabel("Delta")
        axes[class_id].set_ylabel("Count")
        axes[class_id].axvline(
            x=configuration["reference_line_position"],
            color=configuration["color_reference_line"],
            ls=configuration["reference_line_style"],
            lw=configuration["reference_line_width"],
        )

    for class_id in range(number_of_classes, len(axes)):
        axes[class_id].axis("off")

    plt.tight_layout()
    plt.savefig(
        f"{out_dir}/delta_histograms_by_class.png", dpi=configuration["dpi_default"]
    )
    plt.close()
