#!/usr/bin/env python3
"""
Information field scales analysis.

Computes and visualizes four different measures (I, Q, rho, M) of the
occupancy rates across different threshold levels.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


def compute_moment(occupancy_rates: np.ndarray, power: int) -> np.ndarray:
    """
    Compute the sum of occupancy rates raised to a specific power.

    Args:
        occupancy_rates: Array of shape (n_thresholds, n_classes)
        power: The exponent to raise each rate to

    Returns:
        Array of shape (n_thresholds,) containing the sums.
    """
    return np.sum(occupancy_rates**power, axis=1)


def render(data, sweep, out_dir):
    """
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

    ========================================
    THE FOUR MEASURES
    ========================================

    1. I - Information Capacity ($k=1$)
       $I(t) = \sum p_{t,c}$
       - Represents the total "amount" of foreground present at threshold $t$.
       - It is simply the sum of all occupancy rates.
       - High value: Most classes have significant presence.

    2. Q - Structural Complexity ($k=2$)
       $Q(t) = \sum p_{t,c}^2$
       - Related to Simpson's Diversity Index or Herfindahl–Hirschman Index (HHI).
       - Measures "concentration" of occupancy.
       - High value: One or few classes dominate the threshold level.
       - Low value: Occupancy is spread evenly across many classes.

    3. rho ($\rho$) - State Density ($k=3$)
       $\rho(t) = \sum p_{t,c}^3$
       - Higher order moment.
       - Increasingly sensitive to the most dominant class.
       - Acts as a "magnifying glass" for peak occupancy.

    4. M - Field Measure ($k=4$)
       $M(t) = \sum p_{t,c}^4$
       - Very high order moment.
       - Extremely sensitive to the single most dominant class.
       - Effectively tracks the "extremes" of the occupancy distribution.

    ========================================
    WHY USE MULTIPLE POWERS?
    ========================================

    By looking at $k=1, 2, 3, 4$, we perform a **MULTISCALE ANALYSIS**
    of the information field:

    - Low $k$ (e.g., $I$) gives a "global" view of all classes.
    - High $k$ (e.g., $M$) gives a "local/extreme" view, focusing
      only on the most prominent features at that threshold.

    This allows us to distinguish between:
    - A threshold where ALL classes are slightly present (Low $Q$, Low $M$)
    - A threshold where ONE class is very dominant (High $Q$, High $M$)

    ========================================
    VISUALIZATION STRATEGY
    ========================================

    We plot these four measures in a 2x2 grid to allow direct comparison.
    The vertical reference line at $\Delta = 0$ helps correlate these
    information changes with the central contrast of the images.
    """
    configuration = data["viz"]
    occupancy_rates = sweep["occupancy_rates"].cpu().numpy()
    threshold_values = sweep["thresholds"]

    # Pre-calculate all moments to avoid redundant computation in plotting loop
    measures = {
        "I - Information Capacity (Global)": {
            "power": 1,
            "color": "green",
            "ylabel": "Sum of occupancy rates",
        },
        "Q - Structural Complexity (Local)": {
            "power": 2,
            "color": "blue",
            "ylabel": "Sum of occupancy rates squared",
        },
        "rho - State Density (Point)": {
            "power": 3,
            "color": "red",
            "ylabel": "Sum of occupancy rates cubed",
        },
        "M - Field Measure (Integral)": {
            "power": 4,
            "color": "purple",
            "ylabel": "Sum of occupancy rates to 4th power",
        },
    }

    figure, axes = plt.subplots(2, 2, figsize=configuration["figure_entropy"])
    axes = axes.flatten()

    for ax, (title, params) in zip(axes, measures.items()):
        values = compute_moment(occupancy_rates, params["power"])

        ax.plot(threshold_values, values, color=params["color"], lw=1.5)
        ax.fill_between(
            threshold_values,
            0,
            values,
            alpha=configuration["alpha_default"],
            color=params["color"],
        )

        ax.set_title(title, fontsize=10)
        ax.set_ylabel(params["ylabel"], fontsize=8)
        ax.set_xlabel("Threshold Value", fontsize=8)

        # Add reference line at delta = 0
        ax.axvline(
            x=0,
            color=configuration["color_reference_line"],
            ls=configuration["reference_line_style"],
        )
        ax.grid(alpha=configuration["alpha_grid"])

    plt.tight_layout()
    plt.savefig(f"{out_dir}/entropy_analysis.png", dpi=configuration["dpi_default"])
    plt.close()
