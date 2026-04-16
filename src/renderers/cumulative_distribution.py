#!/usr/bin/env python3
"""
Cumulative distribution function (CDF) by class.

Displays the cumulative distribution function of delta field values
for each class, showing what percentage of pixels are below each threshold.

========================================
WHAT IS CDF?
========================================

The Cumulative Distribution Function (CDF) shows:
    "What percentage of pixels are <= a given threshold?"

Mathematically:
    CDF(t) = (1/N) × Σ [δᵢ <= t]
           = P(δ <= t)
           = Fraction of pixels with delta value <= t

This is the INTEGRAL of the probability density function (PDF).

If PDF is histogram, CDF is the cumulative histogram.

========================================
INTERPRETATION
========================================

CDF curve properties:

START (at t = -5.546):
    CDF ≈ 0 (almost no pixels are this dark)

END (at t = +5.546):
    CDF ≈ 1 (almost all pixels are this bright)

MIDDLE (at t = 0):
    CDF = 0.5: Exactly half the pixels are <= mid-gray
    CDF > 0.5: More than half the pixels are dark
    CDF < 0.5: More than half the pixels are bright

SLOPE:
    - Steep slope: Many pixels at that exact value
    - Flat slope: Few pixels at that value
    - Slope = 1/N at uniform distribution

SHAPE:
    - Sigmoid (S-curve): Balanced dark and bright
    - Shifted left: Primarily dark
    - Shifted right: Primarily bright

========================================
CDF VS PDF (HISTOGRAM)
========================================

PDF (histogram):
    - Shows density at each value
    - Local information
    - Can be noisy

CDF (cumulative):
    - Shows accumulation up to value
    - Global information
    - Always smooth (monotonically increasing)

CDF is more robust because:
    - No binning required
    - Always valid (monotone)
    - Easy to compute percentiles

Example:
    Median = value where CDF = 0.5
    P10 = value where CDF = 0.1 (10th percentile)
    P90 = value where CDF = 0.9 (90th percentile)

========================================
WHAT CAN WE LEARN?
========================================

Compare digit "0" vs digit "1":

Digit "0":
    - CDF crosses 0.5 at negative value (more dark than bright)
    - Steeper slope in middle (sharp contrast boundary)

Digit "1":
    - CDF crosses 0.5 near 0 (balanced)
    - Possibly gentler slope (sparser image)

The CDF provides a complete description of the
distribution in a single smooth curve.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils.viz_utils import save_visualization, get_symbol_label


def _plot_cdf_curves(ax, data, threshold_values, occupancy_rates, number_of_classes):
    """Plot the CDF curves for each class."""
    for class_id in range(number_of_classes):
        # Compute CDF: % of pixels <= threshold
        # Using pre-computed occupancy rates (% of pixels > threshold)
        cumulative_distribution = 1.0 - (occupancy_rates[:, class_id].cpu().numpy() / 100.0)

        ax.plot(
            threshold_values,
            cumulative_distribution,
            label=get_symbol_label(class_id, data),
            linewidth=1.5,
        )


def _setup_cdf_plot(ax, configuration, number_of_classes):
    """Configure the axes for CDF plot."""
    ax.set_xlabel("Threshold Value (Delta)")
    ax.set_ylabel("Cumulative Probability (CDF)")
    ax.set_title("Cumulative Distribution Function (CDF) by Class")
    ax.legend(fontsize=8, loc="lower right", ncol=2 if number_of_classes > 5 else 1)
    ax.grid(alpha=configuration["alpha_grid"])


def render(data, sweep, out_dir):
    """
    Render CDF visualization for each class.

    Args:
        data: VisualizationData containing loaded data and configuration
        sweep: SweepResults containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    number_of_classes = data.number_of_classes
    threshold_values = sweep.thresholds
    occupancy_rates = sweep.occupancy_rates

    fig, ax = plt.subplots(figsize=configuration["figure_cdf"])

    _plot_cdf_curves(ax, data, threshold_values, occupancy_rates, number_of_classes)
    _setup_cdf_plot(ax, configuration, number_of_classes)

    description = (
        "Cumulative Distribution Function (CDF) showing the percentage of pixels below each Delta threshold. "
        "Steep sections indicate high pixel density at those values. "
        "Crossing the 0.5 probability level (median) reveals the overall brightness balance of each symbol."
    )
    save_visualization("07_cdf_by_class.png", out_dir, configuration, "dpi_default", description=description)
