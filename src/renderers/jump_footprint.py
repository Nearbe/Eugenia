#!/usr/bin/env python3
"""
Jump Footprint Analysis.

Visualizes the specific pixels in the Delta field that trigger
significant jumps in the occupancy rate during the threshold sweep.
"""

import logging
import os

import matplotlib.pyplot as plt
import numpy as np

from utils.viz_utils import save_visualization, get_symbol_label

logger = logging.getLogger(__name__)


def render(data, sweep, out_dir):
    """
    Render jump footprints for major events.
    """
    configuration = data["config"]
    symbols = data["symbol_delta_fields"]
    thresholds = sweep.thresholds
    jump_events = sweep.jump_events
    num_classes = data["number_of_classes"]

    # Find the largest jump for each class
    major_jumps: dict[int, tuple[float, int, float]] = {}
    for t, class_idx, mag, prev_occ, curr_occ in jump_events:
        if class_idx not in major_jumps or mag > major_jumps[class_idx][2]:
            major_jumps[class_idx] = (t, class_idx, mag)

    # Create folder for individual footprint images
    footprint_dir = os.path.join(out_dir, "19_jump_footprints")
    os.makedirs(footprint_dir, exist_ok=True)

    # Step size
    t_step = thresholds[1] - thresholds[0]

    for class_idx in range(num_classes):
        label = get_symbol_label(class_idx, data)
        delta_field = symbols[class_idx].cpu().numpy()

        plt.figure(figsize=(5, 5))

        if class_idx in major_jumps:
            t_jump, _, mag = major_jumps[class_idx]
            # Identify pixels that triggered this jump
            # Occupancy is calculated as count(delta > t)
            # A jump at t means count(delta > t) vs count(delta > t-t_step)
            # Footprint: pixels x such that t-t_step < delta(x) <= t
            footprint = (delta_field > (t_jump - t_step)) & (delta_field <= t_jump)

            # Show original delta field dimmed, and footprint highlighted
            plt.imshow(delta_field, cmap="gray", alpha=0.3)
            # Overlay footprint
            if np.any(footprint):
                masked_footprint = np.ma.masked_where(~footprint, footprint)
                plt.imshow(masked_footprint, cmap="Reds", alpha=1.0)

            plt.title(f"{label}\nJump at T={t_jump:.2f}\n(mag={mag:.1f}%)", fontsize=12)
            description = (
                f"Jump Footprint for class {label}: Visualizes the pixels responsible for the topology jump. "
                f"Red pixels indicate areas where the occupancy rate changed sharply at threshold {t_jump:.2f}."
            )
        else:
            plt.imshow(delta_field, cmap="gray")
            plt.title(f"{label}\nNo Jumps Detected")
            description = f"Delta field for class {label}: No significant jumps detected."

        plt.axis("off")

        save_visualization(
            f"{class_idx}_{label}.png",
            footprint_dir,
            configuration,
            "dpi_default",
            description=description,
        )
        plt.close()

    if not major_jumps:
        logger.info("  No major jumps found for footprint analysis")
    else:
        logger.info(
            f"  Created jump footprint visualizations for {len(major_jumps)} classes with jumps"
        )
    logger.info("  Created jump footprint visualization")


if __name__ == "__main__":
    pass
