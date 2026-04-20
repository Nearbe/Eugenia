#!/usr/bin/env python3
"""
Horizon animation.

Creates an animated GIF showing binary masks at different threshold values,
demonstrating how the delta field changes as the threshold varies.

========================================
WHAT IS THE ANIMATION?
========================================

This creates a "movie" showing how the binary masks
change as we sweep through threshold values.

We take 60 evenly-spaced frames (configurable):
    - Frame 0: threshold = -8 (most restrictive)
    - Frame 30: threshold = 0 (midpoint)
    - Frame 60: threshold = +8 (least restrictive)

At each frame, we show ALL classes/symbols in a grid.

========================================
WHY IS THIS USEFUL?
========================================

1. UNDERSTANDING DYNAMICS:
   - How the digit emerges from nothing
   - At what threshold each feature appears
   - How features merge/split

2. VISUAL INTUITION:
   - Build intuition for the "horizon" concept
   - See the sweep in action
   - Identify key thresholds

3. PRESENTATION:
   - GIF is easy to share and view
   - No code needed to interpret
   - Engaging for non-technical audience

The animation is particularly powerful because it shows
the dynamic nature of topological filtering -
this is essentially "watching" the topological
analysis happen in real-time.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from utils.viz_utils import get_channel_config, get_symbol_label
from utils.image_utils import hex_to_rgb, create_colored_mask


def render(data, sweep, out_dir):
    """
    Render horizon animation as GIF.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes
    is_color = data.is_color

    # Get color configuration from eugenia.utils.viz_utils
    channel_colors, _ = get_channel_config(data, configuration)

    threshold_values = sweep.thresholds
    number_of_frames = configuration["animation_frames"]

    # Create directory for animation frames
    frames_directory = os.path.join(out_dir, "anim_frames")
    os.makedirs(frames_directory, exist_ok=True)

    # Calculate grid layout
    grid_cols = min(configuration["animation_grid_columns"], number_of_classes)
    grid_rows = (number_of_classes + grid_cols - 1) // grid_cols

    # Select frame indices uniformly across threshold range
    frame_indices = np.linspace(0, len(threshold_values) - 1, number_of_frames).astype(int)

    # Generate each frame
    print(f"  Generating {number_of_frames} animation frames...", flush=True)

    for frame_idx, threshold_idx in enumerate(frame_indices):
        threshold = threshold_values[threshold_idx]

        plt.figure(figsize=configuration["figure_animation"])

        for class_id in range(number_of_classes):
            symbol = symbols[class_id].cpu().numpy()
            binary_mask = (symbol > threshold).astype(float)

            plt.subplot(grid_rows, grid_cols, class_id + 1)

            if is_color:
                color_rgb = hex_to_rgb(channel_colors[class_id])
                rgb_image = create_colored_mask(binary_mask, color_rgb)
                plt.imshow(rgb_image)
            else:
                plt.imshow(binary_mask, cmap=configuration["colormap_binary"])

            label = get_symbol_label(class_id, data)
            plt.title(f"{label} (\u0394 > {threshold:.1f})", fontsize=9)
            plt.axis("off")

        plt.tight_layout()
        plt.savefig(
            f"{frames_directory}/frame_{frame_idx:04d}.png",
            dpi=configuration["dpi_low"],
        )
        plt.close()

    # Create animated GIF from frames
    print("  Assembling GIF...", flush=True)
    try:
        frames = [
            Image.open(f"{frames_directory}/frame_{i:04d}.png") for i in range(number_of_frames)
        ]
        frames[0].save(
            f"{out_dir}/02_horizon_animation.gif",
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
        )
    except Exception as e:
        print(f"  Warning: GIF assembly failed: {e}")
