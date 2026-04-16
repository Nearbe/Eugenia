#!/usr/bin/env python3
r"""
Phase volume visualization.

Displays multiple binary threshold layers stacked in 3D, showing how the
volume occupied by the delta field changes as the threshold increases.
Each layer represents a different threshold level.

========================================
WHAT IS A PHASE VOLUME?
========================================

This visualization creates a "topological stack" of the image.
Instead of looking at one binary mask, we look at several layers
simultaneously, where each layer corresponds to a different
threshold level.

The Z-axis represents the "phase" or threshold level.

========================================
HOW IT WORKS
========================================

1. SELECT KEY THRESHOLDS:
   We pick representative levels from the sweep range:
   [-5.0, -2.0, 0.0, 2.0, 4.0]

2. STACKING (line 51-63):
   For each threshold $t_i$:
   - Create a binary mask where $\delta > t_i$.
   - Elevate this mask to height $z = i + 1$ in the 3D space.
   - This creates a "layer" of the foreground at that specific level.

3. VISUALIZING THE VOLUME:
   By stacking these layers, we can see how the "volume" of the
   foreground grows as we lower the threshold (or shrinks as we raise it).

========================================
WHY IS THIS USEFUL?
========================================

1. DYNAMIC STRUCTURE:
   - It shows not just *what* is there, but *when* it appears.
   - You can see the "growth" of a digit's structure in 3D.

2. TOPOLOGICAL EVOLUTION:
   - Observe how components merge or holes form as you move
     up through the layers (the filtration process).
   - It provides a direct visual intuition for Persistent Homology.

3. CONTRAST GRADIENTS:
   - The "thickness" of the stack at any $(x, y)$ location tells you
     about the local contrast gradient.
   - A steep slope in the stack indicates a sharp edge.
   - A wide/gradual transition indicates a soft/blurry boundary.

========================================
INTERPRETATION
========================================

- **Tall stacks**: Regions that are present across many thresholds
  (robust, high-contrast features).
- **Short/Thin stacks**: Regions that only appear at very specific
  thresholds (transient, low-contrast noise or fine details).
- **Empty space**: Areas that never exceed the chosen thresholds.

This is essentially a "3D slice" of the filtration process used in
Topological Data Analysis (TDA).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from utils.viz_utils import save_visualization, get_symbol_label


def render(data, sweep, out_dir):
    """
    Render phase volume visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    # Create folder for individual phase volume images
    phase_dir = os.path.join(out_dir, "15_phase_volumes")
    os.makedirs(phase_dir, exist_ok=True)

    # Выбор ключевых пороговых значений ("фаз"), которые равномерно покрывают
    # диапазон дельта-поля и показывают основные этапы эволюции структуры.
    key_thresholds = [-5.0, -2.5, 0.0, 2.5, 5.0]

    for idx in range(number_of_classes):
        delta_image = symbols[idx].cpu().numpy()
        h, w = delta_image.shape

        plt.figure(figsize=(6, 5))

        ax = plt.subplot(1, 1, 1, projection="3d")
        x, y = np.meshgrid(np.arange(w), np.arange(h))

        # Plot each threshold level as a stacked layer
        for layer_idx, t_val in enumerate(key_thresholds):
            binary_mask = (delta_image > t_val).astype(float)

            if binary_mask.sum() > 0:
                # Размещение каждого слоя на своей высоте по оси Z.
                # Значения np.nan используются для того, чтобы matplotlib не отрисовывал
                # пустые области, где пиксели не прошли порог.
                z_layer = np.where(binary_mask > 0, layer_idx + 1, np.nan)

                ax.plot_surface(  # type: ignore[attr-defined]
                    x, y, z_layer, cmap="viridis", alpha=0.4, vmin=0, vmax=len(key_thresholds)
                )

        label = get_symbol_label(idx, data)
        ax.set_title(f"{label} Phase Volume")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Phase")  # type: ignore[attr-defined]

        description = (
            f"Phase Volume for class {label}: Shows stacked binary occupancy layers at key thresholds "
            f"{-5.0, -2.5, 0.0, 2.5, 5.0}, visualizing the topological filtration process."
        )
        save_visualization(
            f"{idx}_{label}.png",
            phase_dir,
            configuration,
            "dpi_default",
            description=description,
        )
        plt.close()
