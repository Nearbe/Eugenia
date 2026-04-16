#!/usr/bin/env python3
"""
Utilities for matplotlib visualizations and plotting.
"""

import os
from typing import Dict, List, Tuple, Optional

import matplotlib.pyplot as plt

# Импорт констант из image_utils для использования в get_channel_config
from utils.image_utils import CMYK_COLORS, CMYK_COLORMAPS, RGB_COLORS, RGB_COLORMAPS


def get_channel_config(
    data: Dict,
    configuration: Dict,
) -> Tuple[List[str], List[str]]:
    """
    Get colors and colormaps based on data type (CMYK, RGB, or grayscale).

    Args:
        data: Dictionary containing loaded data
        configuration: Dictionary containing visualization parameters

    Returns:
        Tuple of (channel_colors, channel_colormaps)
    """
    is_color = data.get("is_color", False)
    color_space = data.get("color_space", "Grayscale")
    number_of_classes = data.get("number_of_classes", 1)

    if is_color:
        if color_space == "CMYK":
            return (CMYK_COLORS, CMYK_COLORMAPS)
        else:
            return (RGB_COLORS, RGB_COLORMAPS)
    else:
        return (
            [configuration["colormap_binary"]] * number_of_classes,
            [configuration["colormap_3d"]] * number_of_classes,
        )


def get_symbol_label(class_id: int, data: Dict) -> str:
    """
    Get display label for a symbol/class.

    Args:
        class_id: Index of the class
        data: Dictionary containing loaded data

    Returns:
        String label for the class
    """
    symbol_names = data.get("symbol_names", None)
    return symbol_names[class_id] if symbol_names else str(class_id)


def add_reference_line(ax: plt.Axes, configuration: Dict) -> None:
    """
    Add a vertical reference line to the plot based on configuration.

    Args:
        ax: Matplotlib axes object
        configuration: Dictionary containing reference line parameters
    """
    ax.axvline(
        x=configuration.get("reference_line_position", 0.0),
        color=configuration["color_reference_line"],
        ls=configuration["reference_line_style"],
    )


def save_visualization(
    filename: str, out_dir: str, configuration: Dict, dpi: str = "dpi_high",
    description: Optional[str] = None
) -> None:
    """
    Save the current matplotlib figure.

    Args:
        filename: Name of the file to save
        out_dir: Directory to save in
        configuration: Visualization configuration dictionary
        dpi: Key in configuration for DPI setting
        description: Optional description text to add to the plot
    """
    if description:
        # Add description at the bottom
        plt.figtext(
            0.5, 0.01, description,
            ha="center", fontsize=7,
            bbox={"boxstyle": "round", "facecolor": "whitesmoke", "alpha": 0.8,
                  "edgecolor": "silver"},
            wrap=True
        )

    plt.tight_layout(rect=[0, 0.03, 1, 0.97] if description else None)
    path = os.path.join(out_dir, filename)
    plt.savefig(path, dpi=configuration.get(dpi, 150))
    plt.close()
