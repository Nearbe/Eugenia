#!/usr/bin/env python3
r"""
Stress map (gradient magnitude) visualization.

Computes and displays the gradient magnitude of each delta field,
showing areas of high "stress" (rapid change) as 3D surfaces.
The gradient magnitude indicates how quickly values change,
which relates to the local complexity of the delta field.

========================================
WHAT IS A STRESS MAP?
========================================

In this context, "Stress" refers to the **Gradient Magnitude** ($\|\nabla D\|$)
of the delta field $D$.

It measures how rapidly the contrast changes at any given pixel location.

Mathematically:
    $\nabla D = \left( \frac{\partial D}{\partial x}, \frac{\partial D}{\partial y} \right)$

    Stress (Magnitude) $= \|\nabla D\| = \sqrt{\left(\frac{\partial D}{\partial x}\right)^2 + \left(\frac{\partial D}{\partial y}\right)^2}$

========================================
INTERPRETATION
========================================

The 3D surface represents the "intensity of change":

HIGH STRESS (Peaks):
    - Occurs at sharp edges and boundaries.
    - High contrast transitions (e.g., edge of a stroke).
    - Represents where the most information is concentrated.

LOW STRESS (Valleys/Plains):
    - Occurs in uniform regions.
    - Areas with constant brightness or darkness.
    - Represents "empty" space or solid interiors.

WHY IS THIS USEFUL?
========================================

1. EDGE DETECTION:
   It is essentially a visual representation of the image's edges.
   The peaks tell you exactly where the boundaries are.

2. COMPLEXITY MEASURE:
   A highly complex/textured image will have many high-stress peaks.
   A simple, smooth image (like a single line) will have fewer,
   more localized peaks.

3. TOPOLOGICAL CORRELATION:
   The stress map is closely related to the "birth" and "death" of
   topological features. Most topological changes happen at high-stress
   locations (the boundaries).

========================================
VISUALIZATION DETAILS
========================================

We plot several "stress landscapes" side-by-side.
The height of each peak corresponds to the local rate of change.
This allows us to see the "structural skeleton" of the digit's edges.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from utils.viz_utils import save_visualization, get_symbol_label
from utils.image_utils import compute_gradient_magnitude


def render(data, sweep, out_dir):
    """
    Render stress map visualization (Gradient Magnitude).

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    # Limit number of displayed classes
    display_count = min(configuration["surface_samples"], number_of_classes)

    plt.figure(figsize=(display_count * 4, 5))

    for idx in range(display_count):
        delta_image = symbols[idx].cpu().numpy()
        h, w = delta_image.shape

        ax = plt.subplot(1, display_count, idx + 1, projection="3d")

        # Skip very small images that can't have a gradient
        if h < 2 or w < 2:
            ax.text(0.5, 0.5, 0.5, "Too small", transform=ax.transAxes)
            ax.set_title(f"{get_symbol_label(idx, data)}")
            continue

        # Compute gradient magnitude using utility function
        stress_map = compute_gradient_magnitude(delta_image)

        # Create mesh grid
        x, y = np.meshgrid(np.arange(w), np.arange(h))

        ax.plot_surface(
            x, y, stress_map,
            cmap=configuration["colormap_heatmap"],
            alpha=configuration.get("colormap_3d_alpha", 0.9),
            edgecolor="none",
        )

        ax.set_title(f"{get_symbol_label(idx, data)} (Stress)")
        ax.set_zlim(0, max(0.1, stress_map.max()))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("||\u2207\u0394||")

    save_visualization("14_stress_map.png", out_dir, configuration, "dpi_default")
