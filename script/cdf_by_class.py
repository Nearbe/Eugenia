#!/usr/bin/env python3
"""
Cumulative distribution function (CDF) by class.

Displays the cumulative distribution function of delta field values
for each class, showing what percentage of pixels are below each threshold.
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
