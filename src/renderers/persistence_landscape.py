#!/usr/bin/env python3
"""
Persistence landscape visualization.

Displays the "skeleton" of each delta field by filtering out low-persistence
regions. Shows only the most significant topological features as a 3D surface.

========================================
WHAT IS A PERSISTENCE LANDSCAPE?
========================================

In Topological Data Analysis (TDA), we study how features (components, holes)
"persist" across different scales (thresholds).

A "Persistence Landscape" is a way to represent these topological
features as functions. While this script provides a simplified
geometric version, it captures the core idea:

1. FILTRATION: We sweep through thresholds (the filtration process).
2. BIRTH & DEATH: A feature is "born" at threshold $b$ and "dies" at $d$.
3. PERSISTENCE: The lifetime of a feature is $p = d - b$.

========================================
THE "SKELETON" APPROACH
========================================

This visualization creates a "topological skeleton" by applying
a persistence threshold (line 49):

    persistence_mask = normalized_delta > persistence_threshold

By masking out all values below this threshold, we effectively:
- Remove "noise" (short-lived features)
- Keep only the most robust topological structures (long-lived features)

The resulting 3D surface shows ONLY the parts of the image that are
topologically significant.

========================================
WHY IS THIS USEFUL?
========================================

1. NOISE REDUCTION:
   - Standard delta fields contain many small fluctuations (noise).
   - This approach filters them out, leaving only the "true" shape.

2. FEATURE HIGHLIGHTING:
   - Makes the core structure of a digit immediately obvious.
   - For example, in an '8', it will highlight the two main loops
     while ignoring small texture variations.

3. ROBUSTNESS:
   - Provides a representation that is invariant to small
     perturbations or noise in the original image.

========================================
VISUALIZATION DETAILS
========================================

The script plots several "skeletons" side-by-side.
Each surface shows the delta values of the most persistent regions,
allowing for direct comparison of structural robustness between classes.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from utils.viz_utils import save_visualization, get_symbol_label
from utils.image_utils import normalize_image


def _plot_skeleton(ax, delta_image, data, idx, configuration):
    """Plot the topological skeleton for a single class on the given axes."""
    h, w = delta_image.shape

    # Normalize and filter by persistence threshold
    normalized = normalize_image(delta_image)
    persistence_mask = normalized > configuration["persistence_threshold"]

    # Create mesh grid
    x, y = np.meshgrid(np.arange(w), np.arange(h))

    # Apply mask (set filtered values to NaN to hide them in 3D plot)
    filtered_surface = np.where(persistence_mask, delta_image, np.nan)

    ax.plot_surface(
        x, y, filtered_surface,
        cmap=configuration["colormap_3d"],
        alpha=configuration.get("colormap_3d_alpha", 0.9),
        edgecolor="none",
    )

    ax.set_title(f"{get_symbol_label(idx, data)} (Skeleton)")
    ax.set_zlim(delta_image.min(), delta_image.max())
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("\u0394")


def render(data, sweep, out_dir):
    """
    Render persistence landscape visualization.

    Args:
        data: VisualizationData containing loaded data and configuration
        sweep: SweepResults containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    # Limit number of displayed classes
    display_count = min(configuration["surface_samples"], number_of_classes)

    fig = plt.figure(figsize=(display_count * 4, 5))

    # Pre-convert symbols to numpy to avoid redundant .cpu().numpy() calls
    symbol_numpy = [s.cpu().numpy() for s in symbols[:display_count]]

    for idx in range(display_count):
        delta_image = symbol_numpy[idx]
        ax = fig.add_subplot(1, display_count, idx + 1, projection="3d")
        _plot_skeleton(ax, delta_image, data, idx, configuration)

    description = (
        "Persistence Landscape 'Skeletons' showing only significant topological features. "
        "Features with persistence below threshold (noise) are filtered out. "
        "Highlights the core structural components of each class in 3D."
    )
    save_visualization("13_persistence_landscape.png", out_dir, configuration, "dpi_default",
                       description=description)
