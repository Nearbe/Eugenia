#!/usr/bin/env python3
"""
Euler characteristic analysis.

Computes and visualizes the Euler characteristic (topological invariant)
across different threshold levels. Shows how the topology of the binary
mask changes as the threshold varies, including the derivative of the
Euler characteristic to highlight rapid topological changes.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage


def render(data, sweep, out_dir):
    """
    Render Euler characteristic visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    symbols = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]

    # Use sweep thresholds for analysis
    analysis_thresholds = np.linspace(
        configuration["sweep_min"],
        configuration["sweep_max"],
        configuration["topology_num_thresholds"],
    )

    # Compute Euler characteristic (equal to connected components for binary masks)
    euler_characteristic = np.zeros(len(analysis_thresholds))
    betti_zero = np.zeros(len(analysis_thresholds))

    for threshold_index, threshold_value in enumerate(analysis_thresholds):
        for class_id in range(number_of_classes):
            symbol = symbols[class_id].cpu().numpy()
            binary_mask = (symbol > threshold_value).astype(np.uint8)
            _, component_count = ndimage.label(binary_mask)
            euler_characteristic[threshold_index] += component_count
            betti_zero[threshold_index] += component_count

    # Average across classes
    euler_characteristic /= number_of_classes
    betti_zero /= number_of_classes

    # Create figure with three subplots
    figure, axes = plt.subplots(1, 3, figsize=configuration["figure_euler"])

    # Plot 1: Euler characteristic
    axes[0].plot(
        analysis_thresholds,
        euler_characteristic,
        color="purple",
        lw=configuration["marker_size"],
    )
    axes[0].set_xlabel("Delta Value")
    axes[0].set_ylabel("Euler Characteristic")
    axes[0].grid(alpha=configuration["alpha_grid"])

    # Plot 2: Betti-0 (connected components)
    axes[1].plot(
        analysis_thresholds,
        betti_zero,
        color="steelblue",
        lw=configuration["marker_size"],
    )
    axes[1].set_xlabel("Delta Value")
    axes[1].set_ylabel("Betti-0 (Connected Components)")
    axes[1].grid(alpha=configuration["alpha_grid"])

    # Plot 3: Derivative of Euler characteristic
    euler_derivative = np.abs(np.gradient(euler_characteristic, analysis_thresholds))
    axes[2].plot(
        analysis_thresholds,
        euler_derivative,
        color="darkorange",
        lw=configuration["marker_size"],
    )
    axes[2].set_xlabel("Delta Value")
    axes[2].set_ylabel("|dX/dDelta|")
    axes[2].grid(alpha=configuration["alpha_grid"])

    plt.tight_layout()
    plt.savefig(f"{out_dir}/euler_persistence.png", dpi=configuration["dpi_default"])
    plt.close()
