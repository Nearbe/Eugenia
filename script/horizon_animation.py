#!/usr/bin/env python3
"""
Horizon animation.

Creates an animated GIF showing binary masks at different threshold values,
demonstrating how the delta field changes as the threshold varies.
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image


# Color schemes for different data types
CMYK_COLORS = ["#00FFFF", "#FF00FF", "#FFFF00", "#808080"]
RGB_COLORS = ["#FF0000", "#00FF00", "#0000FF"]


def render(data, sweep, out_dir):
    """
    Render horizon animation as GIF.

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

    # Select color scheme based on data type
    if is_color:
        if color_space == "CMYK":
            channel_colors = CMYK_COLORS
        else:
            channel_colors = RGB_COLORS
    else:
        channel_colors = [configuration["colormap_binary"]] * number_of_classes

    threshold_values = sweep["thresholds"]
    number_of_frames = configuration["animation_frames"]

    # Create directory for animation frames
    frames_directory = os.path.join(out_dir, "animation_frames")
    os.makedirs(frames_directory, exist_ok=True)

    # Calculate grid layout
    grid_columns = min(configuration["animation_grid_columns"], number_of_classes)
    grid_rows = (number_of_classes + grid_columns - 1) // grid_columns

    # Select frame indices uniformly across threshold range
    frame_indices = np.linspace(0, len(threshold_values) - 1, number_of_frames).astype(
        int
    )

    # Generate each frame
    for frame_number, threshold_index in enumerate(frame_indices):
        threshold = threshold_values[threshold_index]

        figure, axes = plt.subplots(
            grid_rows,
            grid_columns,
            figsize=configuration["figure_animation"],
        )
        axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

        for class_id in range(number_of_classes):
            symbol = symbols[class_id].cpu().numpy()
            binary_mask = (symbol > threshold).astype(float)

            if is_color:
                # Create RGB image with color
                rgb_image = np.zeros((binary_mask.shape[0], binary_mask.shape[1], 3))
                hex_color = channel_colors[class_id].lstrip("#")
                red_value = int(hex_color[0:2], 16) / 255
                green_value = int(hex_color[2:4], 16) / 255
                blue_value = int(hex_color[4:6], 16) / 255
                rgb_image[:, :, 0] = binary_mask * red_value
                rgb_image[:, :, 1] = binary_mask * green_value
                rgb_image[:, :, 2] = binary_mask * blue_value
                axes[class_id].imshow(rgb_image)
            else:
                axes[class_id].imshow(binary_mask, cmap=channel_colors[class_id])

            label = symbol_names[class_id] if symbol_names else str(class_id)
            axes[class_id].set_title(f"{label}  Threshold>{threshold:.1f}", fontsize=9)
            axes[class_id].axis("off")

        # Hide unused axes
        for class_id in range(number_of_classes, len(axes)):
            axes[class_id].axis("off")

        plt.tight_layout()
        plt.savefig(
            f"{frames_directory}/frame_{frame_number:04d}.png",
            dpi=configuration["dpi_low"],
        )
        plt.close()

    # Create animated GIF from frames
    try:
        animation_frames = [
            Image.open(f"{frames_directory}/frame_{frame_id:04d}.png")
            for frame_id in range(number_of_frames)
        ]
        animation_frames[0].save(
            f"{out_dir}/horizon_animation.gif",
            save_all=True,
            append_images=animation_frames[1:],
            duration=100,
            loop=0,
        )
    except Exception:
        pass  # Silent failure if PIL not available
