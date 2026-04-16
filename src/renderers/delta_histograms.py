#!/usr/bin/env python3
"""
Delta histograms by class.

Displays histogram of delta field values for each class in a grid layout.

========================================
WHAT DOES THIS VISUALIZE?
========================================

Each histogram shows the DISTRIBUTION of delta values
within a single symbol/class.

For each class c:
    - X-axis: Delta value (-5.546 to 5.546)
    - Y-axis: Number of pixels with that delta value

This is essentially the probability density function (PDF)
of the delta field for each digit.

========================================
INTERPRETATION
========================================

Left-tailed distribution (more negative values):
    - Darker image overall
    - More filled/bold strokes

Right-tailed distribution (more positive values):
    - Lighter/smaller strokes

Centered around 0:
    - Balanced contrast
    - Roughly equal dark and light regions

The RED VERTICAL LINE (reference_line_position = 0.0)
indicates the "mid-gray" threshold.

Pixels to the LEFT of 0 are darker than mid-gray
Pixels to the RIGHT of 0 are brighter than mid-gray

This histogram reveals the "contrast profile" of each
digit - how it's constructed from light and dark parts.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils.viz_utils import save_visualization, get_symbol_label


def render(data, sweep, out_dir):
    """
    Render delta field histograms for all classes.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    columns = configuration["grid_columns"]
    rows = (number_of_classes + columns - 1) // columns

    # Calculate figure size based on grid
    fig_w, fig_h = configuration["figure_wide"]
    fig_h = max(fig_h, rows * configuration["grid_row_height"])

    plt.figure(figsize=(fig_w, fig_h))

    for class_id in range(number_of_classes):
        values = symbols[class_id].cpu().numpy().flatten()

        plt.subplot(rows, columns, class_id + 1)
        plt.hist(
            values,
            bins=configuration["histogram_bins"],
            color=configuration["color_histogram"],
            alpha=configuration["alpha_default"],
        )

        plt.title(
            f"{get_symbol_label(class_id, data)} (n={values.size})",
            fontsize=configuration["figure_title_fontsize"],
        )
        plt.xlabel("Delta Value")
        plt.ylabel("Pixel Count")

        plt.axvline(
            x=configuration["reference_line_position"],
            color=configuration["color_reference_line"],
            ls=configuration["reference_line_style"],
            lw=configuration["reference_line_width"],
        )
        plt.grid(alpha=configuration["alpha_grid"])

    description = (
        "Distribution of Delta values for each class. Values < 0 indicate darker pixels, values > 0 indicate brighter pixels. "
        "The red line at 0 marks the 'mid-gray' threshold. The shape of these histograms reveals the unique contrast "
        "profile and stroke characteristics of each digit/symbol."
    )
    save_visualization("00a_delta_histograms_by_class.png", out_dir, configuration, "dpi_default",
                       description=description)
