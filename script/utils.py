#!/usr/bin/env python3
"""Shared utilities for visualization scripts."""

import numpy as np
from typing import Dict, List, Tuple


def get_channel_config(
    data: Dict,
    v: Dict,
) -> Tuple[List[str], List[str]]:
    """Get colors and colormaps based on data type (CMYK, RGB, or grayscale).

    Returns:
        (channel_colors, channel_cmaps): colors for RGB/CMYK, colormaps for grayscale
    """
    is_color = data.get("is_color", False)
    color_space = data.get("color_space", "RGB")
    n_classes = data["n_classes"]

    if is_color:
        if color_space == "CMYK":
            return (
                ["#00FFFF", "#FF00FF", "#FFFF00", "#808080"],
                ["Blues", "Purples", "YlOrBr", "Greys"],
            )
        else:
            return (
                ["#FF0000", "#00FF00", "#0000FF"],
                ["Reds", "Greens", "Blues"],
            )
    else:
        return (
            [v["cmap_binary"]] * n_classes,
            [v["cmap_3d"]] * n_classes,
        )


def get_symbol_label(c: int, data: Dict) -> str:
    """Get label for symbol/class."""
    symbol_names = data.get("symbol_names", None)
    return symbol_names[c] if symbol_names else str(c)


def compute_gradient_magnitude(img: np.ndarray) -> np.ndarray:
    """Compute gradient magnitude of 2D image."""
    gy, gx = np.gradient(img)
    return np.sqrt(gx**2 + gy**2)


def normalize_image(img: np.ndarray, eps: float = 1e-10) -> np.ndarray:
    """Normalize image to [0, 1] range."""
    mn, mx = img.min(), img.max()
    if mx - mn < eps:
        return np.zeros_like(img)
    return (img - mn) / (mx - mn)
