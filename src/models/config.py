#!/usr/bin/env python3
"""
Configuration parameters for all visualizations.

This module centralizes all numeric constants used across the visualization pipeline.
Each parameter includes a docstring explaining its purpose and effect.

========================================
KEY MATHEMATICAL CONSTANTS
========================================

DELTA FIELD TRANSFORMATION (log2-based):
    D = log2(X + 1) - log2(256 - X)

This maps pixel values X ∈ [0, 255] to real numbers D ∈ [-8, 8].

Key properties:
- log2(X + 1) is the branching depth (Хребет) for value X+1
- log2(256 - X) is the compression depth for remaining pixels
- The constants ±8 come from log2(256) = 8

    log2(256) = 8  (D⁸(Id) — 8 levels of branching)
    log2(1) = 0

256 = 2⁸ = D⁸(Id) — exactly 8 levels of the Spine (Хребет).
L(256) = 8 — information capacity per pixel per Essentials [30_Информация.md].

========================================
THRESHOLD SWEEP RANGE
========================================

sweep_min = -8
sweep_max = 8
sweep_step = 0.0001

These exactly cover the log2-based delta field range [-8, 8].
With step = 0.0001, we get ~160,000 threshold levels.

Resolution trade-off:
- More thresholds → smoother curves, more jump detection
- Fewer thresholds → faster computation

The 1% jump threshold means we detect changes that affect
at least 1% of pixels between adjacent thresholds.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class VisualizationConfig:
    """
    Central configuration for all visualizations.

    All parameters are documented with their purpose and typical values.
    Use the default instance 'CONFIG' or create custom instances as needed.
    """

    # =========================================================================
    # THRESHOLD SWEEP PARAMETERS
    # =========================================================================
    # The delta field is thresholded at many values to generate binary masks.
    # These control the range and resolution of the sweep.

    sweep_min: float = -8.0
    """Minimum threshold value for delta field sweep. Matches log2(1) - log2(256) = -8."""

    sweep_max: float = 8.0
    """Maximum threshold value for delta field sweep. Matches log2(256) - log2(1) = 8."""

    sweep_step: float = 0.0001
    """Step size between consecutive thresholds."""

    jump_threshold: float = 1.0
    """Percentage change threshold for detecting significant jumps in occupancy."""

    # =========================================================================
    # DATA LOADING PARAMETERS
    # =========================================================================

    # number_of_classes is determined dynamically from data (e.g., 10 for MNIST)
    number_of_classes: int = 10
    """Number of distinct classes/symbols in the dataset (e.g., 15 for digits)."""

    image_height: int = 28
    """Expected height of input images in pixels."""

    image_width: int = 28
    """Expected width of input images in pixels."""

    image_channels: int = 1
    """Number of color channels (1 for grayscale, 3 for RGB, 4 for CMYK)."""

    # =========================================================================
    # HISTOGRAM PARAMETERS
    # =========================================================================

    histogram_bins: int = 100
    """Default number of bins for histogram visualization."""

    histogram_bins_min: int = 20
    """Minimum allowed number of histogram bins."""

    histogram_bins_max: int = 500
    """Maximum allowed number of histogram bins."""

    reference_line_position: float = 0.0
    """Position of vertical reference line (e.g., delta = 0)."""

    # =========================================================================
    # GRID LAYOUT PARAMETERS
    # =========================================================================

    grid_columns: int = 5
    """Number of columns in grid layout for subplots."""

    grid_rows: int = 2
    """Number of rows in grid layout for subplots."""

    grid_row_height: float = 1.5
    """Height factor for each row in grid layout."""

    animation_frames: int = 60
    """Number of frames in output animation."""

    animation_grid_columns: int = 5
    """Number of columns in animation grid layout."""

    # =========================================================================
    # TOPOLOGY ANALYSIS PARAMETERS (Betti numbers)
    # =========================================================================

    topology_threshold_min: float = -5.0
    """Minimum threshold for topology analysis."""

    topology_threshold_max: float = 4.5
    """Maximum threshold for topology analysis."""

    topology_num_thresholds: int = 96
    """Number of threshold levels for topology analysis."""

    topology_padding: int = 1
    """Padding pixels for hole detection algorithm."""

    topology_holes_min: int = 0
    """Minimum holes to display (used as floor value)."""

    topology_max_samples: int = 50
    """Maximum number of samples for topology analysis."""

    # =========================================================================
    # DIMENSIONALITY REDUCTION PARAMETERS
    # =========================================================================

    tsne_max_samples: int = 2000
    """Maximum number of samples for t-SNE visualization."""

    tsne_per_class: int = 200
    """Number of samples per class for t-SNE."""

    tsne_perplexity: int = 30
    """Perplexity parameter for t-SNE algorithm."""

    # =========================================================================
    # VISUALIZATION SAMPLING
    # =========================================================================

    surface_samples: int = 5
    """Number of classes/symbols to display in surface plots."""

    persistence_threshold: float = 0.1
    """Threshold for filtering persistence diagram."""

    # =========================================================================
    # COLOR CONFIGURATION
    # =========================================================================

    color_histogram: str = "steelblue"
    """Default color for histograms."""

    color_reference_line: str = "red"
    """Color for reference lines."""

    color_grid: str = "gray"
    """Color for grid lines."""

    alpha_default: float = 0.7
    """Default transparency (alpha) for filled areas."""

    alpha_grid: float = 0.3
    """Transparency for grid lines."""

    colormap_heatmap: str = "hot"
    """Colormap for heatmap visualization."""

    colormap_3d: str = "coolwarm"
    """Colormap for 3D surface plots."""

    colormap_3d_alpha: float = 0.8
    """Transparency for 3D surface plots."""

    colormap_binary: str = "binary"
    """Colormap for binary masks."""

    colormap_grayscale: str = "gray"
    """Colormap for grayscale images."""

    reference_line_style: str = "--"
    """Line style for reference lines (e.g., '--', ':')."""

    reference_line_width: float = 0.5
    """Line width for reference lines."""

    marker_size: int = 2
    """Default marker size for scatter plots."""

    # =========================================================================
    # FIGURE SIZES (width, height in inches)
    # =========================================================================

    figure_wide: tuple = (16, 6)
    """Default wide figure size."""

    figure_heatmap: tuple = (12, 5)
    """Heatmap figure size."""

    figure_heatmap_wide: tuple = (16, 8)
    """Wide heatmap figure size."""

    figure_scatter: tuple = (10, 7)
    """Scatter plot figure size."""

    figure_jumps: tuple = (14, 4)
    """Jumps analysis figure size."""

    figure_cdf: tuple = (10, 6)
    """CDF plot figure size."""

    figure_betti: tuple = (12, 7)
    """Betti numbers figure size."""

    figure_euler: tuple = (15, 4)
    """Euler characteristic figure size."""

    figure_tsne: tuple = (10, 8)
    """t-SNE figure size."""

    figure_3d_multi: tuple = (16, 4)
    """Multi-panel 3D figure size."""

    figure_animation: tuple = (15, 7)
    """Animation frame figure size."""

    figure_individual_histogram: tuple = (8, 4)
    """Individual histogram figure size."""

    figure_individual_histogram_factor: tuple = (2.5, 1.8)
    """Scaling factors for individual histograms."""

    figure_capacity: tuple = (16, 10)
    """Capacity analysis figure size."""

    figure_fractal: tuple = (16, 8)
    """Fractal dimension analysis figure size."""

    figure_phase: tuple = (16, 10)
    """Phase volume figure size."""

    figure_original_vs_binary: tuple = (16, 12)
    """Original vs binary comparison figure size."""

    figure_title_fontsize: int = 9
    """Fontsize for subplot titles."""

    # =========================================================================
    # RESOLUTION (DPI - dots per inch)
    # =========================================================================

    dpi_default: int = 120
    """Default DPI for most visualizations."""

    dpi_high: int = 150
    """High DPI for detailed visualizations."""

    dpi_low: int = 80
    """Low DPI for animations (smaller file size)."""

    dpi_individual: int = 100
    """DPI for individual histogram files."""

    # =========================================================================
    # THRESHOLD VALUES FOR COMPARISON
    # =========================================================================

    comparison_thresholds: List[float] = field(default_factory=lambda: [-5, -3, -1, 0, 1, 2, 3, 4])
    """List of threshold values for original vs binary comparison."""

    # =========================================================================
    # HEATMAP RANGES
    # =========================================================================

    heatmap_vmin: float = 0.0
    """Minimum value for heatmap color scale."""

    heatmap_vmax: float = 100.0
    """Maximum value for heatmap color scale."""


# Default configuration instance
CONFIG = VisualizationConfig()
