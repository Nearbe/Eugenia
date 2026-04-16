#!/usr/bin/env python3
"""
Jump Footprint Analysis.

Visualizes the specific pixels in the Delta field that trigger
significant jumps in the occupancy rate during the threshold sweep.
"""

import logging

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
    major_jumps = {}
    for t, class_idx, mag, prev_occ, curr_occ in jump_events:
        if class_idx not in major_jumps or mag > major_jumps[class_idx][2]:
            major_jumps[class_idx] = (t, class_idx, mag)

    if not major_jumps:
        logger.info("  No major jumps found for footprint analysis")
        return

    num_to_show = min(num_classes, 5)
    fig, axes = plt.subplots(1, num_to_show, figsize=(4 * num_to_show, 5))
    if num_to_show == 1:
        axes = [axes]

    # Step size
    t_step = thresholds[1] - thresholds[0]

    for i in range(num_to_show):
        class_idx = i
        label = get_symbol_label(class_idx, data)
        ax = axes[i]

        delta_field = symbols[class_idx].cpu().numpy()

        if class_idx in major_jumps:
            t_jump, _, mag = major_jumps[class_idx]
            # Identify pixels that triggered this jump
            # Occupancy is calculated as count(delta > t)
            # A jump at t means count(delta > t) vs count(delta > t-t_step)
            # Footprint: pixels x such that t-t_step < delta(x) <= t
            footprint = (delta_field > (t_jump - t_step)) & (delta_field <= t_jump)

            # Show original delta field dimmed, and footprint highlighted
            ax.imshow(delta_field, cmap='gray', alpha=0.3)
            # Overlay footprint
            if np.any(footprint):
                masked_footprint = np.ma.masked_where(~footprint, footprint)
                ax.imshow(masked_footprint, cmap='Reds', alpha=1.0)

            ax.set_title(f"{label}\nJump at T={t_jump:.2f}\n(mag={mag:.1f}%)", fontsize=12)
        else:
            ax.imshow(delta_field, cmap='gray')
            ax.set_title(f"{label}\nNo Jumps Detected")

        ax.axis('off')

    plt.tight_layout()
    description = (
        "Jump Footprints: Visualizes the pixels responsible for the most significant "
        "topology jump in each class. Red pixels indicate areas where the occupancy "
        "rate changed sharply at a specific threshold."
    )
    save_visualization("19_jump_footprints.png", out_dir, configuration, "dpi_default", description=description)
    logger.info("  Created jump footprint visualization")


if __name__ == "__main__":
    pass
