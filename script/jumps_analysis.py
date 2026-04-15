#!/usr/bin/env python3
"""
Jump analysis.

Visualizes the distribution of significant threshold changes ("jumps")
across the threshold sweep. Shows where the occupancy rate changes
dramatically between adjacent thresholds.

========================================
WHAT IS A "JUMP"?
========================================

A "jump" is when the occupancy rate (percentage of pixels
above threshold) changes by more than 1% between adjacent
thresholds.

Mathematically:
    jump = |occupancy[t+1] - occupancy[t]|

If jump > 1.0% (configurable via jump_threshold):
    → Significant change detected!

This is analogous to finding "critical points" in the
threshold sweep where the topology changes rapidly.

========================================
WHY ARE JUMPS IMPORTANT?
========================================

Jumps indicate TOPOLOGICAL TRANSITIONS where:

1. NEW FEATURES EMERGE:
   - A threshold was crossed that reveals new structure
   - Example: When threshold = 0, the "hole" in digit "0" appears

2. FEATURES MERGE:
   - Previously separate regions become connected
   - Example: Two strokes join at a certain threshold

3. FEATURES DISAPPEAR:
   - A region shrinks below visibility
   - Example: Thin stroke disappears at high threshold

Location of jumps reveals:
   - Characteristic contrast levels of each digit
   - Stroke widths and spacing
   - Presence of holes

Example for digit "8":
    - Jump at T ≈ -3: Outer contour appears
    - Jump at T ≈ 0: Top hole becomes visible
    - Jump at T ≈ 0: Bottom hole becomes visible
    - Jump at T ≈ +2: Inner regions merge
    - Multiple jumps → complex structure

Example for digit "1":
    - Single simple jump
    - One stroke with consistent width
    - No holes → fewer jumps

========================================
WHAT DOES THE PLOT SHOW?
========================================

X-axis: Threshold value (-5.546 to +5.546)
Y-axis: Number of jumps at each threshold

The histogram shows where in the threshold space
the significant changes occur.

PEAKS in the histogram:
    - Many topological transitions at that threshold
    - A major feature boundary exists

FLAT regions:
    - Smooth transitions
    - No major structure changes

The vertical RED LINE at threshold = 0 divides:
    - Left side: Dark-dominant pixels
    - Right side: Bright-dominant pixels
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(data, sweep, out_dir):
    """
    Render jump analysis visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    threshold_values = sweep["thresholds"]
    jump_events = sweep["jump_events"]
    jump_count = sweep["jump_count"]

    # Count jumps at each threshold
    jump_histogram = np.zeros(len(threshold_values))
    for threshold, _, _, _, _ in jump_events:
        index = np.argmin(np.abs(threshold_values - threshold))
        jump_histogram[index] += 1

    # Create figure
    figure, axis = plt.subplots(figsize=configuration["figure_jumps"])

    axis.plot(
        threshold_values,
        jump_histogram,
        color="crimson",
        linewidth=configuration["marker_size"],
    )
    axis.fill_between(
        threshold_values,
        0,
        jump_histogram,
        alpha=configuration["alpha_default"],
        color="crimson",
    )

    axis.set_xlabel("Threshold Value")
    axis.set_ylabel("Number of Jumps (>1%)")
    axis.set_title(
        f"Total Jumps: {jump_count}",
        fontsize=configuration["figure_title_fontsize"] + 2,
    )

    axis.axvline(
        x=0,
        color=configuration["color_reference_line"],
        ls=configuration["reference_line_style"],
    )
    axis.grid(alpha=configuration["alpha_grid"])

    plt.tight_layout()
    plt.savefig(f"{out_dir}/jumps_analysis.png", dpi=configuration["dpi_default"])
    plt.close()
