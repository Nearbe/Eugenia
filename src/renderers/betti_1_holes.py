#!/usr/bin/env python3
"""
Holes detection analysis (Betti-1).

Tracks the number of holes (loops) in the binary mask at different
threshold levels. Uses morphological operations to detect enclosed
regions that are not connected to the boundary.

========================================
WHAT IS BETTI-1?
========================================

Betti-1 (β₁) is a topological invariant that counts the
number of HOLES or LOOPS in a space.

For a binary image:
- A hole is a region completely enclosed by the foreground
- Examples of holes in digits:
    * "0": 1 hole (center of zero)
    * "8": 2 holes (top and bottom loops)
    * "9": 1 hole (tail loop)
    * "4": 0 holes (no enclosed region)
    * "6": 1 hole (bowl)

========================================
HOW TO COUNT HOLES?
========================================

The algorithm uses a clever "boundary exclusion" method:

1. PAD the binary mask with zeros (line 48-50)
   - Add a 1-pixel border of zeros around the image
   - After padding: real hole + boundary-hole are connected

2. INVERT the padded mask (line 53)
   - 0 becomes 1, 1 becomes 0
   - What was foreground becomes background

3. LABEL connected components (line 54)
   - Each region in inverted mask gets unique label
   - Both real holes and the new exterior are labeled

4. REMOVE boundary components (lines 57-63)
   - Any component touching the padding border
     is NOT a hole (it's the exterior)
   - Remove those from the count

5. The remaining components are HOLES (line 65-67)

This is a standard algorithm in computational topology,
often called "topological hole detection".

Example:
    Binary:         Inverted:         Labeled:
    1 1 1          0 0 0
    1 0 1    →     0 1 0    →     0 2 0
    1 1 1          0 0 0          0 0 0

    Component 2 is a hole (doesn't touch boundary)

========================================
EULER CHARACTERISTIC
========================================

Euler characteristic: χ = β₀ - β₁

For the digit "8":
    - Two circles → β₀ = 2 (outer contour + inner regions?)
    - Actually depends on threshold...
    - At certain threshold: χ might be 0 or negative

For simply connected regions:
    - Filled circle: β₀ = 1, β₁ = 0, χ = 1
    - Ring (donut): β₀ = 1, β₁ = 1, χ = 0

The variations in χ with threshold provide information
about topological changes in the image structure.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from core.linear.linear_algebra import linspace
from core.topology.label_2d import label_2d
from utils.viz_utils import save_visualization, get_symbol_label


def render(data, sweep, out_dir):
    """
    Render holes detection visualization (Betti-1).

    Args:
        data: VisualizationData object containing loaded data and configuration
        sweep: SweepResults object containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    # Generate thresholds for topology analysis
    topology_thresholds = linspace(
        configuration["topology_threshold_min"],
        configuration["topology_threshold_max"],
        configuration["topology_num_thresholds"],
    )

    # Compute holes for each class and threshold
    plt.figure(figsize=configuration["figure_betti"])

    for class_id in range(number_of_classes):
        symbol = symbols[class_id]
        holes_counts = []

        for threshold_value in topology_thresholds:
            # Create binary mask: 1 where value > threshold, else 0
            binary_mask = [
                [1 if float(pixel) > float(threshold_value) else 0 for pixel in row]
                for row in symbol
            ]

            # Pad to detect holes (regions not connected to boundary)
            padding = configuration.get("topology_padding", 1)
            padded_mask = (
                [[0] * (len(binary_mask[0]) + 2 * padding)]
                + [[0] * padding + row + [0] * padding for row in binary_mask]
                + [[0] * (len(binary_mask[0]) + 2 * padding)]
            )

            # Invert and label connected components
            # Padded background is 0, becomes 1 in inverted_mask
            # All background regions (including holes) are now 1s
            inverted_mask = [[1 - pixel for pixel in row] for row in padded_mask]
            labeled_background = label_2d(inverted_mask)

            # Find regions that touch the boundary (these are not holes)
            boundary_labels = set()
            # Top and bottom rows
            for label in labeled_background[0]:
                boundary_labels.add(label)
            for label in labeled_background[-1]:
                boundary_labels.add(label)
            # Left and right columns
            for row in labeled_background:
                boundary_labels.add(row[0])
                boundary_labels.add(row[-1])

            # 0 is the foreground label, discard it
            boundary_labels.discard(0)

            # Count unique labels (excluding 0 and boundary)
            unique_labels = set()
            for row in labeled_background:
                for label in row:
                    if label > 0 and label not in boundary_labels:
                        unique_labels.add(label)

            actual_holes = max(configuration.get("topology_holes_min", 0), len(unique_labels))
            holes_counts.append(actual_holes)

        plt.plot(
            list(topology_thresholds),
            holes_counts,
            "s-",
            ms=configuration.get("marker_size", 2),
            label=get_symbol_label(class_id, data),
        )

    plt.xlabel("Threshold Value (Delta)")
    plt.ylabel("Number of Holes (\u03b2\u2081)")
    plt.title("Hole Detection (Betti-1) vs. Threshold")
    plt.legend(fontsize=8, loc="upper right", ncol=2 if number_of_classes > 5 else 1)
    plt.grid(alpha=configuration["alpha_grid"])

    description = (
        "Betti-1 (β₁) counts the number of HOLES (loops). "
        "Different digits have characteristic β₁ signatures (e.g., '8' has 2 holes, '0' has 1). "
        "The number of detected holes changes as the threshold varies, revealing the stability of internal structures."
    )
    save_visualization("11_betti1_holes.png", out_dir, configuration, description=description)
