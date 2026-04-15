#!/usr/bin/env python3
"""
Information field scales analysis.

Computes and visualizes four different measures (I, Q, rho, M) of the
occupancy rates across different threshold levels:
- I: Sum of occupancy rates (global information capacity)
- Q: Sum of squared occupancy rates (structural complexity)
- rho: Sum of cubed occupancy rates (state density)
- M: Sum of fourth-power occupancy rates (field measure)
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    """
    Render information field scales visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    occupancy_rates = sweep["occupancy_rates"].cpu().numpy()
    threshold_values = sweep["thresholds"]

    figure, axes = plt.subplots(2, 2, figsize=configuration["figure_entropy"])
    axes = axes.flatten()

    # I: Information capacity (sum of occupancy rates)
    information_capacity = np.sum(occupancy_rates, axis=1)
    axes[0].plot(threshold_values, information_capacity, color="green")
    axes[0].fill_between(
        threshold_values,
        0,
        information_capacity,
        alpha=configuration["alpha_default"],
        color="green",
    )
    axes[0].set_title("I - Information Capacity (Global)")
    axes[0].set_ylabel("Sum of occupancy rates")

    # Q: Structural complexity (sum of squared occupancy rates)
    structural_complexity = np.sum(occupancy_rates**2, axis=1)
    axes[1].plot(threshold_values, structural_complexity, color="blue")
    axes[1].fill_between(
        threshold_values,
        0,
        structural_complexity,
        alpha=configuration["alpha_default"],
        color="blue",
    )
    axes[1].set_title("Q - Structural Complexity (Local)")
    axes[1].set_ylabel("Sum of occupancy rates squared")

    # rho: State density (sum of cubed occupancy rates)
    state_density = np.sum(occupancy_rates**3, axis=1)
    axes[2].plot(threshold_values, state_density, color="red")
    axes[2].fill_between(
        threshold_values,
        0,
        state_density,
        alpha=configuration["alpha_default"],
        color="red",
    )
    axes[2].set_title("rho - State Density (Point)")
    axes[2].set_ylabel("Sum of occupancy rates cubed")

    # M: Field measure (sum of fourth-power occupancy rates)
    field_measure = np.sum(occupancy_rates**4, axis=1)
    axes[3].plot(threshold_values, field_measure, color="purple")
    axes[3].fill_between(
        threshold_values,
        0,
        field_measure,
        alpha=configuration["alpha_default"],
        color="purple",
    )
    axes[3].set_title("M - Field Measure (Integral)")
    axes[3].set_ylabel("Sum of occupancy rates to fourth power")

    # Common settings for all axes
    for axis in axes:
        axis.set_xlabel("Threshold Value")
        axis.axvline(
            x=0,
            color=configuration["color_reference_line"],
            ls=configuration["reference_line_style"],
        )
        axis.grid(alpha=configuration["alpha_grid"])

    plt.tight_layout()
    plt.savefig(f"{out_dir}/entropy_analysis.png", dpi=configuration["dpi_default"])
    plt.close()
