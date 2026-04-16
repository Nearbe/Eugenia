#!/usr/bin/env python3
"""
t-SNE visualization of binary profiles.

Applies t-SNE dimensionality reduction to the binary occupancy profiles
to visualize the similarity between classes in a 2D space.

========================================
WHAT IS t-SNE?
========================================

t-SNE (t-distributed Stochastic Neighbor Embedding)
is a dimensionality reduction technique that:

1. Maps high-dimensional data to 2D/3D
2. Preserves local structure (nearby in → nearby out)
3. Reveals clusters and patterns

It was invented by Laurens van der Maaten (2008)
and has become a standard visualization tool
for high-dimensional data.

========================================
WHAT ARE "BINARY PROFILES"?
========================================

Each class has an "occupancy profile" - a vector of
111,000 values (one per threshold).

    profile[c] = [occupancy_at_t0, occupancy_at_t1, ...]

This captures the entire "horizon" of a digit
across all thresholds.

The profile is a HIGH-DIMENSIONAL representation:
    - 1D input (single image)
    - 111K dimensions (thresholds)

t-SNE reduces 111K → 2 for visualization.

========================================
WHAT DOES THIS SHOW?
========================================

When projected to 2D:

- CLOSE together: Similar "horizon" profiles
  - Same stroke widths
  - Similar contrast distribution
  - Same topological features

- FAR APART: Different profiles
  - Different digit structures

Example for MNIST:
    - 1 and 7 might be close (both simple strokes)
    - 0 and 8 might be close (both have holes)
    - 1 and 0 would be far apart

This provides a way to measure "similarity" between
digits based purely on their topological properties,
not on pixel values or neural network features.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from utils.viz_utils import save_visualization, get_symbol_label


def render(data, sweep, out_dir):
    """
    Render t-SNE visualization of binary occupancy profiles.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    occupancy_rates = sweep.occupancy_rates.cpu().numpy()
    number_of_classes = data.number_of_classes

    # Transpose to get one profile vector per class: (n_classes, n_thresholds)
    profiles = occupancy_rates.T

    plt.figure(figsize=configuration["figure_tsne"])

    # Adjust perplexity for small number of samples (must be < n_samples)
    perplexity = min(configuration.get("tsne_perplexity", 30), number_of_classes - 1)

    if number_of_classes > 1:
        # Run t-SNE reduction
        tsne = TSNE(
            n_components=2,
            perplexity=max(1, perplexity),
            random_state=42,
            init='pca',
            learning_rate='auto'
        )
        coords = tsne.fit_transform(profiles)

        # Plot 2D projection
        plt.scatter(
            coords[:, 0],
            coords[:, 1],
            c=np.arange(number_of_classes),
            s=100,
            cmap="tab10" if number_of_classes <= 10 else "tab20",
            edgecolors="black",
            alpha=0.7
        )

        # Annotate points with labels
        for i in range(number_of_classes):
            label = get_symbol_label(i, data)
            plt.annotate(
                label,
                (coords[i, 0], coords[i, 1]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=10,
                fontweight="bold"
            )

    plt.title(f"t-SNE Projection of Binary Profiles ({number_of_classes} symbols)")
    plt.xlabel("t-SNE Dimension 1")
    plt.ylabel("t-SNE Dimension 2")
    plt.grid(alpha=configuration["alpha_grid"])

    description = (
        "t-SNE projection of binary occupancy profiles. Each point represents a class's entire threshold response. "
        "Classes that are topologically similar (e.g., similar stroke thickness, number of holes) appear closer together. "
        "This reveals the structural relationships between symbols in a reduced 2D space."
    )
    save_visualization("05_tsne_binary_profiles.png", out_dir, configuration, "dpi_default", description=description)
