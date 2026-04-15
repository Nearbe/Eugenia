#!/usr/bin/env python3
"""
Connected components analysis (Betti-0).

Tracks the number of connected components in the binary mask
at different threshold levels. This measures how many distinct
regions exist as the threshold varies.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage


def render(data, sweep, out_dir):
    """
    Render connected components visualization.

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

    # Compute connected components for each class and threshold
    connected_components = {class_id: [] for class_id in range(number_of_classes)}

    for class_id in range(number_of_classes):
        symbol = symbols[class_id].cpu().numpy()

        for threshold_value in topology_thresholds:
            binary_mask = (symbol > threshold_value).astype(np.uint8)
            _, component_count = ndimage.label(binary_mask)
            connected_components[class_id].append(component_count)

    # Create figure
    figure, axis = plt.subplots(figsize=configuration["figure_betti"])

    for class_id in range(number_of_classes):
        axis.plot(
            topology_thresholds,
            connected_components[class_id],
            "o-",
            ms=2,
            label=str(class_id),
        )

    axis.set_xlabel("Threshold Value")
    axis.set_ylabel("Number of Connected Components")
    axis.legend(fontsize=8)
    axis.grid(alpha=configuration["alpha_grid"])

    plt.tight_layout()
    plt.savefig(f"{out_dir}/betti0_components.png", dpi=configuration["dpi_high"])
    plt.close()
