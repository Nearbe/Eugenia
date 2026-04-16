#!/usr/bin/env python3
r"""
Individual delta histograms per class.

Creates separate histogram files for each class, stored in a subdirectory.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils.viz_utils import get_symbol_label


def render(data, sweep, out_dir):
    """
    Render individual histogram for each class.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    output_subdirectory = os.path.join(out_dir, "individual_hists")
    os.makedirs(output_subdirectory, exist_ok=True)

    # Calculate figure size with scaling factors
    base_w, base_h = configuration["figure_individual_histogram"]
    scale_w, scale_h = configuration["figure_individual_histogram_factor"]
    fig_size = (base_w * scale_w, base_h * scale_h)

    for class_id in range(number_of_classes):
        values = symbols[class_id].cpu().numpy().flatten()
        label = get_symbol_label(class_id, data)

        plt.figure(figsize=fig_size)
        plt.hist(
            values,
            bins=configuration["histogram_bins"],
            color=configuration["color_histogram"],
            alpha=configuration["alpha_default"],
        )

        plt.title(f"Delta Distribution: {label} (n={values.size})")
        plt.xlabel("Delta Value")
        plt.ylabel("Pixel Count")

        plt.axvline(
            x=configuration["reference_line_position"],
            color=configuration["color_reference_line"],
            ls=configuration["reference_line_style"],
            lw=configuration["reference_line_width"],
        )
        plt.grid(alpha=configuration["alpha_grid"])

        # Save manually since it's in a subdirectory
        plt.tight_layout()
        filename = f"class_{class_id}_individual.png"
        plt.savefig(
            os.path.join(output_subdirectory, filename),
            dpi=configuration["dpi_individual"]
        )
        plt.close()
