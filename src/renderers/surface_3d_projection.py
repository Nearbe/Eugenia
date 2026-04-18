#!/usr/bin/env python3
"""
3D surface visualization.

Displays delta field values as 3D surface plots for each class,
showing the topological structure of the delta field.

========================================
WHAT IS A 3D SURFACE PLOT?
========================================

This visualization shows the delta field as a 3D surface:

    X-axis: Column (pixel position in width)
    Y-axis: Row (pixel position in height)
    Z-axis: Delta value (contrast intensity)

The surface height represents the contrast:
    - Z > 0: Bright region (positive contrast)
    - Z < 0: Dark region (negative contrast)
    - Z = 0: Mid-gray

========================================
INTERPRETATION
========================================

PEAKS (Z > 0):
    - Brightest pixels in the image
    - White strokes, highlights
    - "Mountains" in the landscape

VALLEYS (Z < 0):
    - Darkest pixels in the image
    - Black strokes, shadows
    - "Canyons" in the landscape

FLAT REGIONS:
    - Uniform areas
    - Consistent contrast

The topological FEATURES are visible as peaks and valleys:
    - Stroke center = highest point (peak)
    - Stroke edge = slope
    - Background = valley floor
    - Holes = depressions surrounded by peaks

Example for digit "8":
    - TWO peaks (top and bottom loops)
    - TWO valleys (the holes inside)
    - Complex topology visible as dual peaks

Example for digit "1":
    - Single ridge (the stroke)
    - Simple, monotonic surface

========================================
WHY IS THIS USEFUL?
========================================

1. INTUITIVE VISUALIZATION:
   - Easy to understand the image structure
   - No complex math required

2. TOPOLOGY INSPECTION:
   - See holes (depressions)
   - See connectivity (ridges)
   - Visualize "shape" mathematically

3. COMPARISON:
   - Different digits have different landscapes
   - Build intuition for mathematical representation
   - Compare visually without pixel comparison

This is the "geometric" counterpart to the
"topological" analysis in betti0/betti1.
The surface shows WHAT exists, topology shows
HOW IT'S CONNECTED.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from utils.viz_utils import get_channel_config, get_symbol_label, save_visualization


def render(data, sweep, out_dir):
    """
    Render 3D surface visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data.config
    symbols = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    # Select colormaps based on data type from eugenia.utils.viz_utils
    _, channel_colormaps = get_channel_config(data, configuration)

    # SCIENTIFIC RATIONALE FOR INDIVIDUAL IMAGES:
    # In topological data analysis (TDA), precise feature detection is crucial. Grouped subplots compress
    # surfaces, masking subtle topological invariants like Betti numbers or persistence. Consequence:
    # False negatives in hole detection (e.g., missing loops in '8'). Question: Does this trade-off
    # violate the continuity principle in Morse theory? We prioritize fidelity to enable rigorous
    # homology group computations.

    # SCIENTIFIC ORGANIZATION:
    # Class-wise separation aligns with supervised learning paradigms, facilitating feature extraction
    # for classifiers. Consequence: Enables quantitative comparison via metrics like Earth Mover's Distance
    # on height fields. Question: How does this structure support hypothesis testing in manifold learning?

    # Create folder for individual surface images
    surface_dir = os.path.join(out_dir, "06_3d_surfaces")
    os.makedirs(surface_dir, exist_ok=True)

    for idx in range(number_of_classes):
        # SCIENTIFIC BASIS FOR FULL CLASS COVERAGE:
        # Limiting to subsets introduces sampling bias in topological statistics. Consequence: Incomplete
        # representation of the shape space manifold, potentially missing critical points in Reeb graphs.
        # Question: Does full coverage risk overfitting in downstream ML models? Mitigated by individual files
        # for selective analysis.

        delta_image = symbols[idx].cpu().numpy()
        h, w = delta_image.shape

        # SCIENTIFIC CHOICE OF FIGSIZE:
        # Fixed dimensions ensure isometric scaling, preserving aspect ratios critical for topological
        # measurements. Consequence: Consistent visual metrics across classes, avoiding distortions
        # in curvature estimation. Question: How does this affect perceptual scaling in human cognition?

        plt.figure(figsize=(6, 6))

        ax = plt.subplot(1, 1, 1, projection="3d")  # type: ignore[assignment]
        x, y = np.meshgrid(np.arange(w), np.arange(h))

        # WHY plot_surface WITH SPECIFIC PARAMS?
        # Причина: edgecolor='none' для гладкости (избегаем артефактов рёбер), alpha для прозрачности
        # (чтобы видеть сквозь слои). Следствие: Более естественная 3D-визуализация, легче интерпретировать.
        # Вопрос: Почему не wireframe? Потому что заливка лучше показывает непрерывность контраста.

        ax.plot_surface(  # type: ignore[attr-defined]
            x,
            y,
            delta_image,
            cmap=channel_colormaps[idx % len(channel_colormaps)],
            alpha=configuration.get("colormap_3d_alpha", 0.8),
            edgecolor="none",
        )

        label = get_symbol_label(idx, data)
        ax.set_title(f"3D Surface - {label}")

        # WHY DYNAMIC Z-LIMITS?
        # Причина: Автоматическая подстройка под диапазон данных — если все значения равны,
        # добавляем padding для видимости. Следствие: Избегаем плоских графиков, сохраняем детали.
        # Вопрос: Нормализовать Z-axis? Нет, абсолютные значения важны для сравнения контраста между классами.

        z_min, z_max = delta_image.min(), delta_image.max()
        if z_min == z_max:
            ax.set_zlim(z_min - 1, z_max + 1)  # type: ignore[attr-defined]
        else:
            ax.set_zlim(z_min, z_max)  # type: ignore[attr-defined]

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("\u0394")  # type: ignore[attr-defined]

        # WHY DETAILED DESCRIPTION?
        # Причина: Пользователь должен понимать, что видит, без обращения к документации.
        # Следствие: Улучшает usability, снижает ошибки интерпретации. Вопрос: Сделать описания настраиваемыми?

        description = (
            f"3D Surface plot of the Delta field for class {label}. "
            "Height and color represent the Delta value (log-contrast). "
            "This reveals the 'topography' of the symbol, where peaks are bright and valleys are dark. "
            "Why useful? Peaks show stroke centers, valleys — backgrounds/holes. "
            "Consequences: Identifies topological features like loops in '8' vs. ridge in '1'. "
            "Question: How does this relate to persistence diagrams?"
        )
        save_visualization(
            f"{idx}_{label}.png",
            surface_dir,
            configuration,
            "dpi_default",
            description=description,
        )
        plt.close()
