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

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    """
    Render CDF visualization for each class.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    symbols = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]
    threshold_values = sweep["thresholds"]

    figure, axis = plt.subplots(figsize=configuration["figure_cdf"])

    for class_id in range(number_of_classes):
        values = symbols[class_id].cpu().numpy().flatten()

        # Compute CDF: percentage of values <= threshold
        cumulative_distribution = np.array(
            [np.mean(values <= threshold) for threshold in threshold_values]
        )

        axis.plot(
            threshold_values,
            cumulative_distribution,
            label=str(class_id),
            linewidth=1.5,
        )

    axis.set_xlabel("Delta Value")
    axis.set_ylabel("Cumulative Probability")
    axis.legend(fontsize=8, ncol=(number_of_classes + 4) // 5)
    axis.grid(alpha=configuration["alpha_grid"])

    plt.tight_layout()
    plt.savefig(f"{out_dir}/cdf_by_class.png", dpi=configuration["dpi_default"])
    plt.close()
