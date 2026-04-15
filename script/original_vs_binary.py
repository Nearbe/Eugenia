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

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Color schemes for different data types
CMYK_COLORS = ["#00FFFF", "#FF00FF", "#FFFF00", "#808080"]
RGB_COLORS = ["#FF0000", "#00FF00", "#0000FF"]


def render(data, sweep, out_dir):
    """
    Render original vs binary comparison visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    symbols = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]
    is_color = data.get("is_color", False)
    color_space = data.get("color_space", "Grayscale")
    symbol_names = data.get("symbol_names", None)

    # Select colors based on data type
    if is_color:
        if color_space == "CMYK":
            channel_colors = CMYK_COLORS
        else:
            channel_colors = RGB_COLORS
    else:
        channel_colors = [configuration["colormap_grayscale"]] * number_of_classes

    comparison_thresholds = configuration["comparison_thresholds"]
    number_of_columns = len(comparison_thresholds) + 1

    figure, axes = plt.subplots(
        number_of_classes,
        number_of_columns,
        figsize=(2 * number_of_columns, max(1.2 * number_of_classes, 3)),
    )

    if number_of_classes == 1:
        axes = axes.reshape(1, -1)

    for class_id in range(number_of_classes):
        delta_image = symbols[class_id].cpu().numpy()

        # First column: original delta field
        if is_color:
            axes[class_id, 0].imshow(
                delta_image,
                cmap=plt.cm.colors.LinearSegmentedColormap.from_list(
                    "channel_cmap", ["black", channel_colors[class_id]]
                ),
            )
        else:
            axes[class_id, 0].imshow(
                delta_image, cmap=configuration["colormap_grayscale"]
            )

        label = symbol_names[class_id] if symbol_names else f"#{class_id}"
        axes[class_id, 0].set_ylabel(label, rotation=0, ha="right")
        axes[class_id, 0].set_xticks([])
        axes[class_id, 0].set_yticks([])

        # Remaining columns: binary masks at different thresholds
        for threshold_index, threshold_value in enumerate(comparison_thresholds):
            binary_mask = (delta_image > threshold_value).astype(float)

            if is_color:
                rgb_image = np.zeros((binary_mask.shape[0], binary_mask.shape[1], 3))
                hex_color = channel_colors[class_id].lstrip("#")
                red_value = int(hex_color[0:2], 16) / 255
                green_value = int(hex_color[2:4], 16) / 255
                blue_value = int(hex_color[4:6], 16) / 255
                rgb_image[:, :, 0] = binary_mask * red_value
                rgb_image[:, :, 1] = binary_mask * green_value
                rgb_image[:, :, 2] = binary_mask * blue_value
                axes[class_id, threshold_index + 1].imshow(rgb_image)
            else:
                axes[class_id, threshold_index + 1].imshow(
                    binary_mask, cmap=configuration["colormap_binary"]
                )

            axes[class_id, threshold_index + 1].set_title(
                f"Threshold>{threshold_value:+.0f}", fontsize=8
            )
            axes[class_id, threshold_index + 1].axis("off")

    plt.tight_layout()
    plt.savefig(f"{out_dir}/original_vs_binary.png", dpi=configuration["dpi_high"])
    plt.close()
