#!/usr/bin/env python3
r"""
Shared utilities for visualization scripts.

This module provides common helper functions used across multiple
visualization scripts to reduce code duplication.
"""

import os
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import torch

# Цветовые схемы для различных цветовых пространств.
# CMYK_COLORS соответствуют стандартным цветам полиграфических красок.
CMYK_COLORS = ["#00FFFF", "#FF00FF", "#FFFF00", "#808080"]
RGB_COLORS = ["#FF0000", "#00FF00", "#0000FF"]
CMYK_COLORMAPS = ["Blues", "Purples", "YlOrBr", "Greys"]
RGB_COLORMAPS = ["Reds", "Greens", "Blues"]


def _get_script_directory() -> str:
    """Get the directory containing this script."""
    return os.path.dirname(os.path.abspath(__file__))


def _get_parent_directory() -> str:
    """Get the parent directory of the script directory."""
    return os.path.dirname(_get_script_directory())


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
    # Вычисление величины градиента как корня из суммы квадратов производных по осям.
    # Это позволяет оценить скорость изменения дельта-поля в каждой точке.
    vertical_gradient, horizontal_gradient = np.gradient(image)
    return np.sqrt(horizontal_gradient ** 2 + vertical_gradient ** 2)


def normalize_image(image: np.ndarray, epsilon: float = 1e-10) -> np.ndarray:
    """
    Normalize image values to [0, 1] range.

    Args:
        image: Input numpy array
        epsilon: Small value to prevent division by zero

    Returns:
        Normalized array with values in [0, 1]
    """
    # Линейное масштабирование значений в диапазон [0, 1].
    # Это необходимо для большинства функций отрисовки matplotlib и сохранения в изображения.
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
        filename: str, out_dir: str, configuration: Dict, dpi: str = "dpi_high", description: str = None
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
            bbox={"boxstyle": "round", "facecolor": "whitesmoke", "alpha": 0.8, "edgecolor": "silver"},
            wrap=True
        )

    plt.tight_layout(rect=[0, 0.03, 1, 0.97] if description else None)
    path = os.path.join(out_dir, filename)
    plt.savefig(path, dpi=configuration.get(dpi, 150))
    plt.close()


# Добавление пустых полей (padding) вокруг тензоров для приведения их к максимальному
# размеру в группе. Это позволяет объединить изображения разного размера в один батч.
def pad_tensors(tensors: List[torch.Tensor], padding_value: float = 0.0) -> torch.Tensor:
    """
    Pad a list of 2D tensors to the same maximum height and width.

    Args:
        tensors: List of 2D PyTorch tensors
        padding_value: Value to use for padding

    Returns:
        3D tensor of shape (len(tensors), max_h, max_w)
    """
    if not tensors:
        return torch.empty(0)

    max_h = max(t.shape[0] for t in tensors)
    max_w = max(t.shape[1] for t in tensors)

    padded_tensors = []
    for t in tensors:
        h, w = t.shape
        # Calculate padding: (left, right, top, bottom)
        pad_h = max_h - h
        pad_w = max_w - w

        # In torch.nn.functional.pad, padding is (padding_left, padding_right, padding_top, padding_bottom)
        padding = (0, pad_w, 0, pad_h)
        padded = torch.nn.functional.pad(t, padding, value=padding_value)
        padded_tensors.append(padded)

    return torch.stack(padded_tensors)
