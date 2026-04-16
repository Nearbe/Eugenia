#!/usr/bin/env python3
"""
3D surface visualization.

Displays delta field values as 3D surface plots for each class,
showing the topological structure of the delta field.

========================================
WHAT IS A 3D SURFACE PLOT?
========================================

This visualization shows the delta field as a 3D surface:

    X-axis: Column (pixel position in width)
    Y-axis: Row (pixel position in height)
    Z-axis: Delta value (contrast intensity)

The surface height represents contrast:
    - Z > 0: Bright region (positive contrast)
    - Z < 0: Dark region (negative contrast)
    - Z = 0: Mid-gray

========================================
INTERPRETATION
========================================

PEAKS (Z > 0):
    - Brightest pixels in the image
    - White strokes, highlights
    - "Mountains" in the landscape

VALLEYS (Z < 0):
    - Darkest pixels in the image
    - Black strokes, shadows
    - "Canyons" in the landscape

FLAT REGIONS:
    - Uniform areas
    - Consistent contrast

The topological FEATURES are visible as peaks and valleys:
    - Stroke center = highest point (peak)
    - Stroke edge = slope
    - Background = valley floor
    - Holes = depressions surrounded by peaks

Example for digit "8":
    - TWO peaks (top and bottom loops)
    - TWO valleys (the holes inside)
    - Complex topology visible as dual peaks

Example for digit "1":
    - Single ridge (the stroke)
    - Simple, monotonic surface

========================================
WHY IS THIS USEFUL?
========================================

1. INTUITIVE VISUALIZATION:
   - Easy to understand the image structure
   - No complex math required

2. TOPOLOGY INSPECTION:
   - See holes (depressions)
   - See connectivity (ridges)
   - Visualize "shape" mathematically

3. COMPARISON:
   - Different digits have different landscapes
   - Build intuition for mathematical representation
   - Compare visually without pixel comparison

This is the "geometric" counterpart to the
"topological" analysis in betti0/betti1.
The surface shows WHAT exists, topology shows
HOW IT'S CONNECTED.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from utils.viz_utils import save_visualization, get_symbol_label, get_channel_config


def render(data, sweep, out_dir):
    """
    Render 3D surface visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    # Select colormaps based on data type from eugenia.utils.viz_utils
    _, channel_colormaps = get_channel_config(data, configuration)

    # Limit number of displayed classes
    display_count = min(configuration["surface_samples"], number_of_classes)

    plt.figure(figsize=configuration["figure_3d_multi"])

    # Pre-convert symbols to numpy to avoid redundant .cpu().numpy() calls
    symbol_numpy = [s.cpu().numpy() for s in symbols[:display_count]]

    for idx in range(display_count):
        delta_image = symbol_numpy[idx]
        h, w = delta_image.shape

        ax = plt.subplot(1, display_count, idx + 1, projection="3d")
        x, y = np.meshgrid(np.arange(w), np.arange(h))

        ax.plot_surface(
            x, y, delta_image,
            cmap=channel_colormaps[idx % len(channel_colormaps)],
            alpha=configuration.get("colormap_3d_alpha", 0.8),
            edgecolor="none"
        )

        label = get_symbol_label(idx, data)
        ax.set_title(label)

        # Set consistent z-axis range
        z_min, z_max = delta_image.min(), delta_image.max()
        if z_min == z_max:
            ax.set_zlim(z_min - 1, z_max + 1)
        else:
            ax.set_zlim(z_min, z_max)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("\u0394")

    description = (
        "3D Surface plots of the Delta field for each class. "
        "Height and color represent the Delta value (log-contrast). "
        "This reveals the 'topography' of the symbols, where peaks are bright and valleys are dark."
    )
    save_visualization("06_3d_surface.png", out_dir, configuration, "dpi_default", description=description)
