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
import numpy as np
from scipy import ndimage
from utils.viz_utils import save_visualization


def compute_topology(binary_mask: np.ndarray, padding: int = 1) -> tuple:
    """
    Compute Betti-0 and Betti-1 for a binary mask.

    Returns:
        (betti_0, betti_1)
    """
    # Betti-0: Connected components
    _, b0 = ndimage.label(binary_mask)

    # Betti-1: Holes
    padded = np.pad(binary_mask, padding, mode="constant")
    inverted = 1 - padded
    labeled_bg, num_bg = ndimage.label(inverted)

    # Boundary labels are not holes
    boundary_labels = (
        set(labeled_bg[0, :])
        | set(labeled_bg[-1, :])
        | set(labeled_bg[:, 0])
        | set(labeled_bg[:, -1])
    )
    boundary_labels.discard(0)

    b1 = max(0, num_bg - len(boundary_labels))

    return b0, b1


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
    analysis_thresholds = np.linspace(
        configuration["topology_threshold_min"],
        configuration["topology_threshold_max"],
        configuration["topology_num_thresholds"],
    )

    # Accumulators for average metrics
    avg_euler = np.zeros(len(analysis_thresholds))
    avg_b0 = np.zeros(len(analysis_thresholds))
    avg_b1 = np.zeros(len(analysis_thresholds))

    # Pre-convert symbols to numpy to avoid redundant .cpu().numpy() calls
    symbol_numpy = [s.cpu().numpy() for s in symbols]

    for t_idx, t_val in enumerate(analysis_thresholds):
        for class_id in range(number_of_classes):
            symbol = symbol_numpy[class_id]
            binary_mask = (symbol > t_val).astype(np.uint8)

            b0, b1 = compute_topology(binary_mask, configuration["topology_padding"])

            avg_b0[t_idx] += b0
            avg_b1[t_idx] += b1
            avg_euler[t_idx] += b0 - b1

    # Average across all classes
    avg_euler /= number_of_classes
    avg_b0 /= number_of_classes
    avg_b1 /= number_of_classes

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
    chi_derivative = np.abs(np.gradient(avg_euler, analysis_thresholds))
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
