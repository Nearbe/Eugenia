#!/usr/bin/env python3
"""
Original vs binary comparison.

Displays each class/symbol alongside its binary thresholded versions
at multiple threshold values, allowing visual comparison of how the
binary mask changes as the threshold varies.

========================================
WHAT IS THIS VISUALIZATION?
========================================

This module provides a direct side-by-side comparison between:

1. THE ORIGINAL DELTA FIELD (Column 0)
   - Shows the continuous contrast landscape.
   - Represents the "ground truth" of the image structure.

2. BINARY MASKS (Remaining Columns)
   - Shows the discretized version at specific thresholds.
   - Represents what is "visible" to a topological algorithm.

========================================
WHY COMPARE THEM?
========================================

The comparison helps us understand how much information is lost
during thresholding:

1. THRESHOLD SENSITIVITY:
   - How quickly do features appear or disappear as we move
     from negative to positive thresholds?
   - Does a single threshold capture the essence of the digit,
     or are multiple levels needed?

2. TOPOLOGICAL FIDELITY:
   - At which threshold does the binary mask most accurately
     represent the "shape" seen in the delta field?
   - For example, at what threshold do the holes in an '8'
     become clearly defined?

3. CONTRAST BOUNDARIES:
   - The transition from the original (continuous) to binary
     (discrete) highlights where the most critical contrast
     boundaries lie.

========================================
VISUALIZATION DETAILS
========================================

Thresholds used are defined in `params.py` under
`comparison_thresholds`.

Coloring:
- Grayscale: Uses standard grayscale colormap.
- CMYK/RGB: Each channel is colored with its characteristic color
  to make the binary mask intuitive (e.g., Cyan channel shows
  cyan binary masks).

The grid layout allows us to see the "evolution" of a digit's
topology as we sweep through the threshold range.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils.viz_utils import save_visualization, get_symbol_label, get_channel_config
from image_utils import hex_to_rgb, create_colored_mask


def render(data, sweep, out_dir):
    """
    Render original vs binary comparison visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes
    is_color = data.is_color

    # Get colors based on data type
    channel_colors, _ = get_channel_config(data, configuration)

    comparison_thresholds = configuration["comparison_thresholds"]
    num_cols = len(comparison_thresholds) + 1

    # Calculate figure size
    fig_w = 2 * num_cols
    fig_h = max(1.2 * number_of_classes, 4)
    plt.figure(figsize=(fig_w, fig_h))

    for class_id in range(number_of_classes):
        delta_image = symbols[class_id].cpu().numpy()
        label = get_symbol_label(class_id, data)

        # First column: original delta field
        plt.subplot(number_of_classes, num_cols, class_id * num_cols + 1)

        if is_color:
            # Create a custom colormap from black to the channel's color
            color_rgb = hex_to_rgb(channel_colors[class_id])
            cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
                "custom", ["black", color_rgb]
            )
            plt.imshow(delta_image, cmap=cmap)
        else:
            plt.imshow(delta_image, cmap=configuration["colormap_grayscale"])

        plt.ylabel(label, rotation=0, ha="right", fontsize=10)
        plt.xticks([])
        plt.yticks([])
        if class_id == 0:
            plt.title("Original (\u0394)", fontsize=10)

        # Remaining columns: binary masks at different thresholds
        for t_idx, t_val in enumerate(comparison_thresholds):
            plt.subplot(number_of_classes, num_cols, class_id * num_cols + t_idx + 2)
            binary_mask = (delta_image > t_val).astype(float)

            if is_color:
                color_rgb = hex_to_rgb(channel_colors[class_id])
                rgb_image = create_colored_mask(binary_mask, color_rgb)
                plt.imshow(rgb_image)
            else:
                plt.imshow(binary_mask, cmap=configuration["colormap_binary"])

            plt.axis("off")
            if class_id == 0:
                plt.title(f"\u0394 > {t_val:+.0f}", fontsize=9)

    description = (
        "Comparison between continuous Delta fields and discrete binary masks at various thresholds. "
        "Helps identify at which threshold topological features (like holes in '8' or '0') become stable. "
        "Negative thresholds capture highlights; positive thresholds capture dark regions."
    )
    save_visualization("09_original_vs_binary.png", out_dir, configuration, "dpi_high", description=description)
