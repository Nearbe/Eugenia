#!/usr/bin/env python3
"""
t-SNE visualization of binary profiles.

Applies t-SNE dimensionality reduction to the binary occupancy profiles
to visualize the similarity between classes in a 2D space.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def render(data, sweep, out_dir):
    """
    Render t-SNE visualization of binary profiles.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["viz"]
    occupancy_rates = sweep["occupancy_rates"].cpu().numpy()
    labels = data["labels"].cpu().numpy()
    number_of_classes = data["number_of_classes"]

    # Transpose to get profiles (one per class)
    profiles = occupancy_rates.T

    figure, axis = plt.subplots(figsize=configuration["figure_tsne"])

    # Adjust perplexity based on number of classes
    perplexity_value = min(configuration["tsne_perplexity"], number_of_classes - 1)

    if number_of_classes >= 2:
        tsne_reducer = TSNE(
            n_components=2, perplexity=perplexity_value, random_state=42
        )
        coordinates = tsne_reducer.fit_transform(profiles)

        axis.scatter(
            coordinates[:, 0],
            coordinates[:, 1],
            c=range(number_of_classes),
            s=50,
            cmap="tab20",
        )

        for class_id in range(number_of_classes):
            axis.annotate(
                str(class_id),
                (coordinates[class_id, 0], coordinates[class_id, 1]),
                fontsize=10,
                fontweight="bold",
            )

    axis.set_title(f"t-SNE of Binary Profiles ({number_of_classes} Classes)")

    plt.tight_layout()
    plt.savefig(f"{out_dir}/tsne_binary_profiles.png", dpi=configuration["dpi_default"])
    plt.close()
