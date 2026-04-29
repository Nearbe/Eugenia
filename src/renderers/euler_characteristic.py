#!/usr/bin/env python3
"""
Euler characteristic analysis.

Computes and visualizes the Euler characteristic (topological invariant)
across different threshold levels. Shows how the topology of the binary
mask changes as the threshold varies, including the derivative of the
Euler characteristic to highlight rapid topological changes.

========================================
EULER CHARACTERISTIC
========================================

The Euler characteristic (χ, chi) is a TOPOLOGICAL INVARIANT -
a property that doesn't change under continuous deformations
(but DOES change under topological transitions).

Formula for binary images:
    χ = β₀ - β₁

Where:
    - β₀ = number of connected components (Betti-0)
    - β₁ = number of holes (Betti-1)

Simple examples:
    - Single point:     β₀=1, β₁=0, χ=1
    - Line segment:   β₀=1, β₁=0, χ=1
    - Circle:       β₀=1, β₁=1, χ=0
    - Two circles:   β₀=2, β₁=2, χ=0
    - Disc (filled): β₀=1, β₁=0, χ=1

For MNIST digits:
    - "0": χ=0 (one hole)
    - "8": χ=0 (two holes)
    - "1": χ=1 (no holes)
    - "3": χ=1 (no holes)
    - "6": χ=0 (one hole)

========================================
WHY STUDY EULER CHARACTERISTIC?
========================================

1. SIMPLICITY: Single number captures topological state
   - Much simpler than tracking β₀ and β₁ separately

2. STABILITY: Small changes in threshold cause smooth changes in χ
   - Unlike β₀/β₁ which can jump wildly

3. FEATURE EXTRACTION: Can distinguish digit types
   - χ = 0: Digits with holes (0, 6, 8, 9)
   - χ = 1: Digits without holes (1, 2, 3, 4, 5, 7)

========================================
THE DERIVATIVE PLOT
========================================

Plot 3 shows |dχ/dΔ| (absolute derivative of χ).

Key insight: When χ changes rapidly:
- Topological transition occurred
- Significant feature boundary crossed
- This is similar to jump detection in compute_sweep()

The derivative plot highlights "critical points" in the
filtration where the topology changes.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from core.linear.linear_algebra import linspace, zeros
from core.topology.label_2d import label_2d
from utils.viz_utils import save_visualization


def compute_topology(binary_mask, padding: int = 1) -> tuple:
    """
    Compute Betti-0 and Betti-1 for a binary mask.

    Returns:
        (betti_0, betti_1)
    """
    # Betti-0: Connected components
    labeled = label_2d(binary_mask)
    b0 = len(set(label for row in labeled for label in row if label > 0))

    # Betti-1: Holes
    # Pad the mask
    padded = (
        [[0] * (len(binary_mask[0]) + 2 * padding)]
        + [[0] * padding + row + [0] * padding for row in binary_mask]
        + [[0] * (len(binary_mask[0]) + 2 * padding)]
    )

    # Invert and label connected components
    inverted = [[1 - pixel for pixel in row] for row in padded]
    labeled_bg = label_2d(inverted)

    # Find regions that touch the boundary (these are not holes)
    boundary_labels = set()
    for label in labeled_bg[0]:
        boundary_labels.add(label)
    for label in labeled_bg[-1]:
        boundary_labels.add(label)
    for row in labeled_bg:
        boundary_labels.add(row[0])
        boundary_labels.add(row[-1])

    boundary_labels.discard(0)

    # Count unique internal labels (holes)
    internal_labels = set()
    for row in labeled_bg:
        for label in row:
            if label > 0 and label not in boundary_labels:
                internal_labels.add(label)

    b1 = len(internal_labels)

    return b0, b1


def gradient(values) -> list:
    """Compute gradient (derivative) of a list of values."""
    result = []
    for i in range(len(values)):
        if i == 0:
            result.append(values[1] - values[0] if len(values) > 1 else 0.0)
        elif i == len(values) - 1:
            result.append(values[-1] - values[-2])
        else:
            result.append((values[i + 1] - values[i - 1]) / 2.0)
    return result


def render(data, sweep, out_dir):
    """
    Render Euler characteristic visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    # Generate thresholds for topology analysis
    analysis_thresholds = list(
        linspace(
            configuration["topology_threshold_min"],
            configuration["topology_threshold_max"],
            configuration["topology_num_thresholds"],
        )
    )

    # Accumulators for average metrics
    avg_euler = [0.0] * len(analysis_thresholds)
    avg_b0 = [0.0] * len(analysis_thresholds)
    avg_b1 = [0.0] * len(analysis_thresholds)

    for t_idx, t_val in enumerate(analysis_thresholds):
        for class_id in range(number_of_classes):
            symbol = symbols[class_id]
            # Create binary mask
            binary_mask = [
                [1 if float(pixel) > float(t_val) else 0 for pixel in row] for row in symbol
            ]

            b0, b1 = compute_topology(binary_mask, configuration["topology_padding"])
            avg_b0[t_idx] += b0
            avg_b1[t_idx] += b1
            avg_euler[t_idx] += b0 - b1

    # Average across all classes
    n = float(number_of_classes)
    avg_euler = [v / n for v in avg_euler]
    avg_b0 = [v / n for v in avg_b0]
    avg_b1 = [v / n for v in avg_b1]

    # Create figure with three panels
    plt.figure(figsize=configuration["figure_euler"])

    # Panel 1: Euler Characteristic (chi = b0 - b1)
    plt.subplot(1, 3, 1)
    plt.plot(analysis_thresholds, avg_euler, color="purple", lw=2)
    plt.title("Avg Euler Characteristic (\u03c7)", fontsize=10)
    plt.xlabel("Threshold (Delta)")
    plt.ylabel("\u03c7 = \u03b2\u2080 - \u03b2\u2081")
    plt.grid(alpha=configuration["alpha_grid"])

    # Panel 2: Betti Numbers (b0 and b1)
    plt.subplot(1, 3, 2)
    plt.plot(
        analysis_thresholds, avg_b0, color="steelblue", lw=2, label="\u03b2\u2080 (Components)"
    )
    plt.plot(analysis_thresholds, avg_b1, color="crimson", lw=2, label="\u03b2\u2081 (Holes)")
    plt.title("Avg Betti Numbers", fontsize=10)
    plt.xlabel("Threshold (Delta)")
    plt.ylabel("Count")
    plt.legend(fontsize=8)
    plt.grid(alpha=configuration["alpha_grid"])

    # Panel 3: Topological Flux (|dchi/dDelta|)
    plt.subplot(1, 3, 3)
    chi_derivative = [abs(v) for v in gradient(avg_euler)]
    plt.plot(analysis_thresholds, chi_derivative, color="darkorange", lw=2)
    plt.title("Topological Flux |d\u03c7/d\u0394|", fontsize=10)
    plt.xlabel("Threshold (Delta)")
    plt.ylabel("Flux")
    plt.grid(alpha=configuration["alpha_grid"])

    description = (
        "Euler Characteristic (χ = β₀ - β₁) and Topological Flux. χ is a fundamental invariant: χ=1 for objects without holes, "
        "χ=0 for objects with one hole. Topological Flux highlights thresholds where major structural changes occur. "
        "Averaged across all classes to show the collective topological behavior."
    )
    save_visualization(
        "12_euler_persistence_complexity.png",
        out_dir,
        configuration,
        "dpi_default",
        description=description,
    )
