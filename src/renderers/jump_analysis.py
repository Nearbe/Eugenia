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

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from utils.viz_utils import save_visualization, add_reference_line


def _compute_jump_histogram(threshold_values, jump_events):
    """Count jumps at each threshold."""
    jump_histogram = np.zeros(len(threshold_values))

    # Thresholds are evenly spaced, so we can calculate indices
    t_min = threshold_values[0]
    t_step = threshold_values[1] - threshold_values[0]

    for t_val, _, _, _, _ in jump_events:
        idx = int((t_val - t_min) / t_step + 0.5)
        if 0 <= idx < len(jump_histogram):
            jump_histogram[idx] += 1
    return jump_histogram


def _plot_jump_distribution(ax, threshold_values, jump_histogram, configuration, jump_count):
    """Plot the jump distribution on the given axes."""
    ax.plot(
        threshold_values,
        jump_histogram,
        color="crimson",
        linewidth=configuration.get("marker_size", 2),
    )
    ax.fill_between(
        threshold_values,
        0,
        jump_histogram,
        alpha=configuration["alpha_default"],
        color="crimson",
    )

    ax.set_xlabel("Threshold Value (Delta)")
    ax.set_ylabel("Jump Density (Count)")
    ax.set_title(f"Jump Analysis (Total Jumps: {jump_count})")

    # Add reference line at delta = 0
    add_reference_line(ax, configuration)
    ax.grid(alpha=configuration["alpha_grid"])


def render(data, sweep, out_dir):
    """
    Render jump analysis visualization.

    Args:
        data: VisualizationData containing loaded data and configuration
        sweep: SweepResults containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    threshold_values = sweep.thresholds
    jump_events = sweep.jump_events
    jump_count = sweep.jump_count

    # Count jumps at each threshold
    jump_histogram = _compute_jump_histogram(threshold_values, jump_events)

    fig, ax = plt.subplots(figsize=configuration["figure_jumps"])
    _plot_jump_distribution(ax, threshold_values, jump_histogram, configuration, jump_count)

    description = (
        "A 'jump' occurs when the occupancy rate changes by > 1% between adjacent thresholds. "
        "Peaks indicate major topological transitions (features appearing or merging). "
        "Threshold 0 (red line) marks the balance between dark and bright regions."
    )
    save_visualization(
        "04_jumps_analysis.png", out_dir, configuration, "dpi_default", description=description
    )
