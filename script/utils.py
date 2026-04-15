#!/usr/bin/env python3
"""
Shared utilities for visualization scripts.

This module provides common helper functions used across multiple
visualization scripts to reduce code duplication.
"""

import numpy as np
from typing import Dict, List, Tuple


# Color schemes for different color spaces
CMYK_COLORS = ["#00FFFF", "#FF00FF", "#FFFF00", "#808080"]
RGB_COLORS = ["#FF0000", "#00FF00", "#0000FF"]
CMYK_COLORMAPS = ["Blues", "Purples", "YlOrBr", "Greys"]
RGB_COLORMAPS = ["Reds", "Greens", "Blues"]


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


def compute_gradient_magnitude(image: np.ndarray) -> np.ndarray:
    """
    Compute gradient magnitude of a 2D image.

    Args:
        image: 2D numpy array

    Returns:
        2D array of gradient magnitudes
    """
    vertical_gradient, horizontal_gradient = np.gradient(image)
    return np.sqrt(horizontal_gradient**2 + vertical_gradient**2)


def normalize_image(image: np.ndarray, epsilon: float = 1e-10) -> np.ndarray:
    """
    Normalize image values to [0, 1] range.

    Args:
        image: Input numpy array
        epsilon: Small value to prevent division by zero

    Returns:
        Normalized array with values in [0, 1]
    """
    minimum_value = image.min()
    maximum_value = image.max()

    if maximum_value - minimum_value < epsilon:
        return np.zeros_like(image)

    return (image - minimum_value) / (maximum_value - minimum_value)


def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """
    Convert hex color string to RGB tuple (0-1 range).

    Args:
        hex_color: Hex color string (e.g., "#FF0000")

    Returns:
        Tuple of (red, green, blue) in [0, 1] range
    """
    hex_value = hex_color.lstrip("#")
    red = int(hex_value[0:2], 16) / 255
    green = int(hex_value[2:4], 16) / 255
    blue = int(hex_value[4:6], 16) / 255
    return (red, green, blue)


def create_colored_mask(
    binary_mask: np.ndarray, color: Tuple[float, float, float]
) -> np.ndarray:
    """
    Create RGB image from binary mask with specified color.

    Args:
        binary_mask: 2D binary array
        color: RGB tuple (0-1 range)

    Returns:
        3D RGB image array
    """
    red, green, blue = color
    rgb_image = np.zeros((binary_mask.shape[0], binary_mask.shape[1], 3))
    rgb_image[:, :, 0] = binary_mask * red
    rgb_image[:, :, 1] = binary_mask * green
    rgb_image[:, :, 2] = binary_mask * blue
    return rgb_image
