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

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from utils.viz_utils import save_visualization, get_symbol_label


def render(data, sweep, out_dir):
    """
    Render scatter plot of mean vs std for each class.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    # Calculate mean and standard deviation for each class
    means = []
    stds = []

    for class_id in range(number_of_classes):
        values = symbols[class_id].cpu().numpy().flatten()
        means.append(values.mean())
        stds.append(values.std())

    plt.figure(figsize=configuration["figure_scatter"])

    # Use a colormap to distinguish classes
    colors = np.arange(number_of_classes)
    plt.scatter(
        means,
        stds,
        c=colors,
        s=100,
        cmap="tab10" if number_of_classes <= 10 else "tab20",
        edgecolors="black",
        alpha=0.8,
    )

    # Add class labels near the points
    for class_id in range(number_of_classes):
        label = get_symbol_label(class_id, data)
        plt.annotate(
            label,
            (means[class_id], stds[class_id]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
        )

    plt.xlabel("Mean Delta (\u03bc)")
    plt.ylabel("Standard Deviation (\u03c3)")
    plt.title(f"Contrast Profile Scatter: Mean vs. Std Dev ({number_of_classes} symbols)")
    plt.grid(alpha=configuration["alpha_grid"])

    # Add quadrant lines at mean of all classes
    plt.axvline(np.mean(means), color="gray", ls="--", alpha=0.3)
    plt.axhline(np.mean(stds), color="gray", ls="--", alpha=0.3)

    save_visualization("03_scatter_mean_std.png", out_dir, configuration, "dpi_default")
