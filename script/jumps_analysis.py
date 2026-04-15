#!/usr/bin/env python3
"""
Jump analysis.

Visualizes the distribution of significant threshold changes ("jumps")
across the threshold sweep. Shows where the occupancy rate changes
dramatically between adjacent thresholds.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    """
    Render jump analysis visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    threshold_values = sweep["thresholds"]
    jump_events = sweep["jump_events"]
    jump_count = sweep["jump_count"]

    # Count jumps at each threshold
    jump_histogram = np.zeros(len(threshold_values))
    for threshold, _, _, _, _ in jump_events:
        index = np.argmin(np.abs(threshold_values - threshold))
        jump_histogram[index] += 1

    # Create figure
    figure, axis = plt.subplots(figsize=configuration["figure_jumps"])

    axis.plot(
        threshold_values,
        jump_histogram,
        color="crimson",
        linewidth=configuration["marker_size"],
    )
    axis.fill_between(
        threshold_values,
        0,
        jump_histogram,
        alpha=configuration["alpha_default"],
        color="crimson",
    )

    axis.set_xlabel("Threshold Value")
    axis.set_ylabel("Number of Jumps (>1%)")
    axis.set_title(
        f"Total Jumps: {jump_count}",
        fontsize=configuration["figure_title_fontsize"] + 2,
    )

    axis.axvline(
        x=0,
        color=configuration["color_reference_line"],
        ls=configuration["reference_line_style"],
    )
    axis.grid(alpha=configuration["alpha_grid"])

    plt.tight_layout()
    plt.savefig(f"{out_dir}/jumps_analysis.png", dpi=configuration["dpi_default"])
    plt.close()
