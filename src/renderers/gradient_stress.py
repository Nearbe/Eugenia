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

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from eugenia.utils.image_utils import compute_gradient_magnitude
from eugenia.utils.viz_utils import get_symbol_label, save_visualization


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

    # Create folder for individual stress map images
    stress_dir = os.path.join(out_dir, "14_stress_maps")
    os.makedirs(stress_dir, exist_ok=True)

    for idx in range(number_of_classes):
        delta_image = symbols[idx].cpu().numpy()
        h, w = delta_image.shape

        plt.figure(figsize=(6, 5))

        ax = plt.subplot(1, 1, 1, projection="3d")

        # Skip very small images that can't have a gradient
        if h < 2 or w < 2:
            ax.text(0.5, 0.5, 0.5, "Too small", transform=ax.transAxes)  # type: ignore
            ax.set_title(f"{get_symbol_label(idx, data)}")
        else:
            # Compute gradient magnitude using utility function
            stress_map = compute_gradient_magnitude(delta_image)

            # Create mesh grid
            x, y = np.meshgrid(np.arange(w), np.arange(h))

            ax.plot_surface(  # type: ignore[attr-defined]
                x,
                y,
                stress_map,
                cmap=configuration["colormap_heatmap"],
                alpha=configuration.get("colormap_3d_alpha", 0.9),
                edgecolor="none",
            )

            ax.set_title(f"{get_symbol_label(idx, data)} (Stress)")
            ax.set_zlim(0, max(0.1, stress_map.max()))  # type: ignore[attr-defined]
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("||\u2207\u0394||")  # type: ignore[attr-defined]

        label = get_symbol_label(idx, data)
        description = (
            f"3D Stress Map for class {label}: Shows the gradient magnitude (||∇Δ||) of the delta field. "
            "Higher values indicate areas of rapid change in contrast."
        )
        save_visualization(
            f"{idx}_{label}.png",
            stress_dir,
            configuration,
            "dpi_default",
            description=description,
        )
        plt.close()
