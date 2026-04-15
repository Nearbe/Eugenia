#!/usr/bin/env python3
"""
Holes detection analysis (Betti-1).

Tracks the number of holes (loops) in the binary mask at different
threshold levels. Uses morphological operations to detect enclosed
regions that are not connected to the boundary.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage


def render(data, sweep, out_dir):
    """
    Render holes detection visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    symbols = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]

    # Generate thresholds for topology analysis
    topology_thresholds = np.linspace(
        configuration["topology_threshold_min"],
        configuration["topology_threshold_max"],
        configuration["topology_num_thresholds"],
    )

    # Compute holes for each class and threshold
    holes_count = {class_id: [] for class_id in range(number_of_classes)}

    for class_id in range(number_of_classes):
        symbol = symbols[class_id].cpu().numpy()

        for threshold_value in topology_thresholds:
            binary_mask = (symbol > threshold_value).astype(np.uint8)

            # Pad to detect holes (regions not connected to boundary)
            padded_mask = np.pad(
                binary_mask, configuration["topology_padding"], mode="constant"
            )

            # Invert and label connected components (holes)
            inverted_mask = 1 - padded_mask
            labeled_holes, hole_count = ndimage.label(inverted_mask)

            # Remove holes connected to boundary
            boundary_pixels = (
                set(labeled_holes[0, :])
                | set(labeled_holes[-1, :])
                | set(labeled_holes[:, 0])
                | set(labeled_holes[:, -1])
            )
            boundary_pixels.discard(0)

            actual_holes = max(
                configuration["topology_holes_min"], hole_count - len(boundary_pixels)
            )
            holes_count[class_id].append(actual_holes)

    # Create figure
    figure, axis = plt.subplots(figsize=configuration["figure_betti"])

    for class_id in range(number_of_classes):
        axis.plot(
            topology_thresholds, holes_count[class_id], "s-", ms=2, label=str(class_id)
        )

    axis.set_xlabel("Threshold Value")
    axis.set_ylabel("Number of Holes")
    axis.legend(fontsize=8)
    axis.grid(alpha=configuration["alpha_grid"])

    plt.tight_layout()
    plt.savefig(f"{out_dir}/betti1_holes.png", dpi=configuration["dpi_high"])
    plt.close()
