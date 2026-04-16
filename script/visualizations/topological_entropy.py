#!/usr/bin/env python3
r"""
Information field scales analysis.

Computes and visualizes four different measures (I, Q, rho, M) of the
occupancy rates across different threshold levels.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from utils import save_visualization, add_reference_line


def compute_moment(occupancy_rates: np.ndarray, power: int) -> np.ndarray:
    """
    Compute the sum of occupancy rates raised to a specific power.

    Args:
        occupancy_rates: Array of shape (n_thresholds, n_classes)
        power: The exponent to raise each rate to

    Returns:
        Array of shape (n_thresholds,) containing the sums.
    """
    return np.sum(occupancy_rates ** power, axis=1)


def _plot_moment(ax, threshold_values, values, params, configuration):
    """Plot a single moment measure on the given axes."""
    color = params["color"]
    ax.plot(threshold_values, values, color=color, lw=1.5)
    ax.fill_between(
        threshold_values,
        0,
        values,
        alpha=configuration["alpha_default"],
        color=color,
    )

    ax.set_title(params["title"], fontsize=10)
    ax.set_ylabel(params["ylabel"], fontsize=8)
    ax.set_xlabel("Threshold Value (Delta)", fontsize=8)

    # Add reference line at delta = 0
    add_reference_line(ax, configuration)
    ax.grid(alpha=configuration["alpha_grid"])


def render(data, sweep, out_dir):
    r"""
    Render information field scales visualization.

    ========================================
    MATHEMATICAL FOUNDATION: MOMENTS OF OCCUPANCY
    ========================================

    This module analyzes the "Information Field" by calculating different
    moments of the occupancy rates across all threshold levels.

    Let $p_{t,c}$ be the occupancy rate (percentage) of class $c$ at
    threshold $t$. We compute:

    $M_k(t) = \sum_{c=1}^{N} (p_{t,c})^k$

    where $k$ is the order of the moment.

    Args:
        data: VisualizationData containing loaded data and configuration
        sweep: SweepResults containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    occupancy_rates = sweep.occupancy_rates.cpu().numpy()
    threshold_values = sweep.thresholds

    # Pre-calculate all moments to avoid redundant computation in plotting loop
    measures = [
        {
            "title": "I - Information Capacity (k=1)",
            "power": 1,
            "color": "green",
            "ylabel": "Sum of occupancy rates",
        },
        {
            "title": "Q - Structural Complexity (k=2)",
            "power": 2,
            "color": "blue",
            "ylabel": "Sum of occupancy rates squared",
        },
        {
            "title": "rho - State Density (k=3)",
            "power": 3,
            "color": "red",
            "ylabel": "Sum of occupancy rates cubed",
        },
        {
            "title": "M - Field Measure (k=4)",
            "power": 4,
            "color": "purple",
            "ylabel": "Sum of occupancy rates to 4th power",
        },
    ]

    fig, axes = plt.subplots(2, 2, figsize=configuration["figure_entropy"])
    axes_flat = axes.flatten()

    for i, params in enumerate(measures):
        values = compute_moment(occupancy_rates, params["power"])
        _plot_moment(axes_flat[i], threshold_values, values, params, configuration)

    plt.tight_layout()

    description = (
        "Information Field Scales analysis using moments of occupancy (M_k = Σ p^k). "
        "I (k=1) measures total capacity, Q (k=2) represents structural complexity, "
        "rho (k=3) is state density, and M (k=4) is the field measure. "
        "These metrics capture the higher-order statistical properties of the topological filtration."
    )
    save_visualization("08_entropy_analysis.png", out_dir, configuration, "dpi_default", description=description)
