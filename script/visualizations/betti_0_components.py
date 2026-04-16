#!/usr/bin/env python3
"""
Connected components analysis (Betti-0).

Tracks the number of connected components in the binary mask
at different threshold levels. This measures how many distinct
regions exist as the threshold varies.

========================================
WHAT IS BETTI-0?
========================================

Betti-0 (β₀) is a topological invariant that counts the number
of CONNECTED COMPONENTS in a space.

For a binary image:
- Each separate region = 1 connected component
- Single pixel blob = 1 component
- Two separate blobs = 2 components

Example with digits:
    Digit "1" (single stroke):   β₀ = 1 (one continuous stroke)
    Digit "0" (circle):       β₀ = 1 (outer ring connected)
    Digit "8" (two loops):   β₀ = 2 (two separate circles)
    Digit "4" (crossing):     β₀ = 1 (still connected)

========================================
WHY DOES BETTI-0 VARY WITH THRESHOLD?
========================================

As threshold changes (from negative to positive):

1. At very NEGATIVE thresholds (e.g., -5.0):
   - Only the brightest pixels exceed threshold
   - May see scattered dots → MANY components

2. At threshold = 0:
   - Mid-tone region visible
   - Components merge → FEWER components

3. At very POSITIVE thresholds (e.g., +5.0):
   - Only darkest pixels exceed threshold
   - May see holes → components break apart

The PLOT of β₀ vs. threshold shows how the image
fragments and consolidates at different scales.

This is essentially a "topological pyramid" or
"multiscale topological analysis" - studying how
topology changes with scale.

========================================
CONNECTED COMPONENTS ALGORITHM
========================================

scipy.ndimage.label() implements Union-Find:
1. Each pixel starts as its own component
2. For each pixel, check neighbors (4-connected or 8-connected)
3. If neighbor exists, merge components
4. Return total count

4-connected (default): Only up, down, left, right neighbors
8-connected: Includes diagonals

For image analysis, 4-connected is standard.
"""

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
from utils import save_visualization, get_symbol_label


def render(data, sweep, out_dir):
    """
    Render connected components visualization (Betti-0).

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    # Генерация набора пороговых значений для топологического анализа.
    # Мы используем разреженную сетку (меньше точек, чем в основной развертке), 
    # так как алгоритм поиска связных компонент (ndimage.label) вычислительно сложен.
    topology_thresholds = np.linspace(
        configuration["topology_threshold_min"],
        configuration["topology_threshold_max"],
        configuration["topology_num_thresholds"],
    )

    # Compute connected components for each class and threshold
    plt.figure(figsize=configuration["figure_betti"])

    # Перенос данных в numpy один раз перед циклом значительно ускоряет выполнение,
    # так как исключает накладные расходы на копирование данных из PyTorch в каждом шаге.
    symbol_numpy = [s.cpu().numpy() for s in symbols]

    for class_id in range(number_of_classes):
        symbol = symbol_numpy[class_id]
        component_counts = []

        for threshold_value in topology_thresholds:
            binary_mask = (symbol > threshold_value).astype(np.uint8)
            _, count = ndimage.label(binary_mask)
            component_counts.append(count)

        plt.plot(
            topology_thresholds,
            component_counts,
            "o-",
            ms=configuration.get("marker_size", 2),
            label=get_symbol_label(class_id, data),
        )

    plt.xlabel("Threshold Value (Delta)")
    plt.ylabel("Number of Connected Components (\u03b2\u2080)")
    plt.title("Connected Components (Betti-0) vs. Threshold")
    plt.legend(fontsize=8, loc="upper right", ncol=2 if number_of_classes > 5 else 1)
    plt.grid(alpha=configuration["alpha_grid"])

    description = (
        "Betti-0 (β₀) counts the number of CONNECTED COMPONENTS. "
        "As threshold increases, features merge (decreasing β₀) or fragment (increasing β₀). "
        "This plot shows the topological evolution of each class across the delta field spectrum."
    )
    save_visualization("10_betti0_components.png", out_dir, configuration, description=description)
