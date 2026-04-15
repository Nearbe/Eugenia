#!/usr/bin/env python3
"""
Individual delta histograms per class.

Creates separate histogram files for each class, stored in a subdirectory.
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    """
    Render individual histogram for each class.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figures
    """
    configuration = data["viz"]
    symbols = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]

    output_subdirectory = os.path.join(out_dir, "individual_hists")
    os.makedirs(output_subdirectory, exist_ok=True)

    for class_id in range(number_of_classes):
        values = symbols[class_id].cpu().numpy().flatten()
        figure_width = (
            configuration["figure_individual_histogram"][0]
            * configuration["figure_individual_histogram_factor"][0]
        )
        figure_height = (
            configuration["figure_individual_histogram"][1]
            * configuration["figure_individual_histogram_factor"][1]
        )

        figure, axis = plt.subplots(figsize=(figure_width, figure_height))
        axis.hist(
            values,
            bins=configuration["histogram_bins"],
            color=configuration["color_histogram"],
            alpha=configuration["alpha_default"],
        )
        axis.set_title(f"Class {class_id} (n={values.size})")
        axis.set_xlabel("Delta")
        axis.set_ylabel("Count")
        axis.axvline(
            x=configuration["reference_line_position"],
            color=configuration["color_reference_line"],
            ls=configuration["reference_line_style"],
            lw=configuration["reference_line_width"],
        )

        plt.tight_layout()
        plt.savefig(
            f"{output_subdirectory}/class_{class_id}_individual.png",
            dpi=configuration["dpi_individual"],
        )
        plt.close()
