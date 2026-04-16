#!/usr/bin/env python3
"""
Horizon heatmap visualization.

Displays the occupancy rate (percentage of pixels above threshold)
for each class across all threshold values as a heatmap.

========================================
WHAT IS THE "HORIZON"?
========================================

Imagine an image as a 3D terrain where:
    - Height = delta value (contrast intensity)
    - X, Y = pixel position

Now imagine "flooding" this terrain with water:
    - At water level = -5.0: Only highest peaks visible
    - At water level = 0.0:  Mid-elevation visible
    - At water level = +5.0: Almost everything visible

The "horizon" is the boundary between:
    - SUBMERGED (below threshold, shown as dark/hot)
    - EMERGED (above threshold, shown as bright/cold)

This visualization shows:
    - X-axis: Threshold value (water level)
    - Y-axis: Class/digit
    - Color: % of pixels above threshold

========================================
WHY IS IT CALLED "HEATMAP"?
========================================

The COLORMAP ("hot" by default) makes:
    - 0% occupancy: Black/cold
    - 50% occupancy: Red/orange
    - 100% occupancy: White/hot

This creates a "heat map" showing which thresholds
are significant for each class.

Key observations:
    - Digits that are "darker" overall will turn on earlier
      (start showing occupancy at lower thresholds)
    - Digits that are "lighter" will turn on later
      (need higher thresholds)

The shape of each "row" in the heatmap reveals
the contrast profile of each digit.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils.viz_utils import save_visualization, get_symbol_label


def render(data, sweep, out_dir):
    """
    Render horizon heatmap visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    number_of_classes = data.number_of_classes
    threshold_values = sweep.thresholds
    occupancy_rates = sweep.occupancy_rates.cpu().numpy()

    plt.figure(figsize=configuration["figure_heatmap_wide"])

    # Transpose occupancy rates to have classes on Y-axis and thresholds on X-axis
    heatmap_data = occupancy_rates.T

    img = plt.imshow(
        heatmap_data,
        aspect="auto",
        cmap=configuration["colormap_heatmap"],
        origin="lower",
        extent=(threshold_values[0], threshold_values[-1], -0.5, number_of_classes - 0.5),
        vmin=configuration["heatmap_vmin"],
        vmax=configuration["heatmap_vmax"],
    )

    plt.yticks(
        range(number_of_classes), [get_symbol_label(i, data) for i in range(number_of_classes)]
    )
    plt.xlabel("Threshold Value (Delta)")
    plt.ylabel("Class / Symbol")
    plt.title("Horizon Heatmap: Occupancy Rate (%) vs. Threshold")

    cbar = plt.colorbar(img)
    cbar.set_label("Occupancy Rate (%)", rotation=270, labelpad=15)

    description = (
        "Horizon Heatmap showing the 'filling' process of each symbol. "
        "X-axis is the threshold (Delta), Y-axis is the symbol, and color is the occupancy percentage. "
        "Reveals when each symbol's structure emerges from the background as the threshold sweeps."
    )
    save_visualization(
        "01_horizon_heatmap.png", out_dir, configuration, "dpi_default", description=description
    )
