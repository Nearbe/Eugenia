#!/usr/bin/env python3
"""
Scatter plot of mean vs standard deviation by class.

Visualizes the distribution of delta field values for each class
by plotting mean (x-axis) vs standard deviation (y-axis).

========================================
WHAT DOES THIS VISUALIZE?
========================================

This scatter plot shows each class as a single point in
a 2D space defined by:

    X-axis: Mean (μ) of delta values
    Y-axis: Standard Deviation (σ) of delta values

Each class is represented by ONE point:
    - Position = (μ_class, σ_class)

========================================
MATHEMATICAL DEFINITIONS
========================================

MEAN (μ) - Average delta value:

    μ = (1/N) Σ δᵢ
        where δᵢ is the delta value of pixel i

Interpretation:
    - μ < 0: Image is predominantly dark
    - μ > 0: Image is predominantly bright
    - μ ≈ 0: Balanced light/dark distribution

STANDARD DEVIATION (σ) - Spread of delta values:

    σ = √[(1/N) Σ (δᵢ - μ)²]

Interpretation:
    - σ large: Wide range of contrast (both very dark and very bright)
    - σ small: Uniform contrast (mostly mid-tones)
    - σ ≈ 0: Entire image has same value

VARIANCE (σ²) - The squared standard deviation:
    Measures "energy" in the contrast distribution

========================================
WHY IS THIS USEFUL?
========================================

This plot reveals PATTERNS in digits based on their
contrast distribution, not their shape:

QUADRANT ANALYSIS:

    High σ, High μ (top-right):
        Bright AND high contrast - possibly bold digits
        Example: "8", "9", "0"

    High σ, Low μ (bottom-right):
        Dark AND high contrast - possibly filled digits
        Example: "1", "4", "7"

    Low σ, High μ (top-left):
        Bright AND low contrast - possibly sparse digits
        Example: "7" (thin stroke)

    Low σ, Low μ (bottom-left):
        Dark AND low contrast - possibly noisy/artifact

CLUSTERING:
    - Digits with similar stroke width → similar (μ, σ)
    - This provides a "contrast-based fingerprint"
    - Different from shape-based classification

Example for MNIST:
    "0": Low μ (dark), High σ (ring structure)
    "1": Near 0 μ (minimal area), Low σ (thin line)
    "8": Low μ, High σ (two circles with holes)
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
