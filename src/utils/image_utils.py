#!/usr/bin/env python3
"""
Utilities for image processing and color conversions.
"""

from typing import Tuple

import numpy as np

# Цветовые схемы для различных цветовых пространств.
# CMYK_COLORS соответствуют стандартным цветам полиграфических красок.
CMYK_COLORS = ["#00FFFF", "#FF00FF", "#FFFF00", "#808080"]
RGB_COLORS = ["#FF0000", "#00FF00", "#0000FF"]
CMYK_COLORMAPS = ["Blues", "Purples", "YlOrBr", "Greys"]
RGB_COLORMAPS = ["Reds", "Greens", "Blues"]


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
    return np.sqrt(horizontal_gradient**2 + vertical_gradient**2)  # type: ignore[no-any-return]


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

    return (image - minimum_value) / (maximum_value - minimum_value)  # type: ignore[no-any-return]


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


def create_colored_mask(binary_mask: np.ndarray, color: Tuple[float, float, float]) -> np.ndarray:
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
