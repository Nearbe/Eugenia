#!/usr/bin/env python3
"""
Data loading and sweep computation for all visualization sources.

This module handles loading data from different sources (MNIST, PNG images, CMYK images),
computes the delta field transformation, and runs the threshold sweep to generate
binary masks at various threshold levels.

Main functions:
- load_data(): Loads and preprocesses data from the configured source
- compute_sweep(): Runs threshold sweep and detects jump events
- run_all_visualizations(): Executes all visualization scripts in sequence
"""

import os
import sys
import time
from typing import Dict, List, Tuple, Optional

import numpy as np
import torch
from PIL import Image
from scipy import ndimage
from dataclasses import asdict

from params import CONFIG


# Environment variables for source selection
SOURCE_NAME = os.environ.get("VIZ_SOURCE", "mnist")
SOURCE_FILE = os.environ.get("VIZ_SOURCE_FILE", "")


# Global cache for loaded data and computed sweep
_cached_data: Optional[Dict] = None
_cached_sweep: Optional[Dict] = None


def _get_script_directory() -> str:
    """Get the directory containing this script."""
    return os.path.dirname(os.path.abspath(__file__))


def _get_parent_directory() -> str:
    """Get the parent directory of the script directory."""
    return os.path.dirname(_get_script_directory())


def load_mnist_data() -> Tuple[torch.Tensor, torch.Tensor, int, int, int]:
    """
    Load one sample per class from MNIST dataset.

    Returns:
        Tuple of (images, labels, height, width, channels)
        - images: Tensor of shape (n_classes, height, width)
        - labels: Tensor of class indices
        - height, width: Image dimensions
        - channels: Number of channels (1 for grayscale)
    """
    script_dir = _get_script_directory()
    data_dir = os.path.join(script_dir, "..", "..", "eugenia_data")
    mnist_path = os.path.join(data_dir, "mnist.npz")

    data_file = np.load(mnist_path)
    all_labels = data_file["y_train"]

    # Select one sample per class
    class_indices = []
    for class_id in range(CONFIG.number_of_classes):
        indices = np.where(all_labels == class_id)[0]
        class_indices.append(indices[0])

    class_indices = np.array(class_indices)
    images = torch.from_numpy(data_file["x_train"][class_indices].astype(np.float32))
    labels = torch.arange(CONFIG.number_of_classes, dtype=torch.int32)

    height = CONFIG.image_height
    width = CONFIG.image_width
    channels = CONFIG.image_channels

    return images, labels, height, width, channels


def load_png_image() -> Tuple[torch.Tensor, torch.Tensor, int, int, int]:
    """
    Load PNG image and extract symbols via connected components.

    Returns:
        Tuple of (images, labels, height, width, channels)
    """
    script_dir = _get_script_directory()
    parent_dir = _get_parent_directory()

    # Try to find the image file
    filename = SOURCE_FILE if SOURCE_FILE else "cyrillic.png"

    for search_dir in [script_dir, parent_dir]:
        path = os.path.join(search_dir, filename)
        if os.path.exists(path):
            break
    else:
        path = os.path.join(script_dir, filename)

    # Try .jpeg if .png not found
    if not os.path.exists(path):
        path = path.replace(".png", ".jpeg")

    # Load and preprocess image
    image = Image.open(path).convert("L")  # Convert to grayscale
    image_array = np.array(image).astype(np.float32)
    height, width = image_array.shape

    # Invert: white background becomes black, symbols become white
    images = torch.from_numpy(255.0 - image_array)

    # Extract symbols using connected components on delta field
    threshold_value = -4.0
    images_cpu = images.numpy()
    binary_mask = (images_cpu > threshold_value).astype(np.uint8)
    labeled_array, num_components = ndimage.label(binary_mask)

    extracted_symbols = []
    for component_id in range(1, num_components + 1):
        coords = np.where(labeled_array == component_id)
        row_min = coords[0].min()
        row_max = coords[0].max() + 1
        col_min = coords[1].min()
        col_max = coords[1].max() + 1
        extracted_symbols.append(images[row_min:row_max, col_min:col_max])

    # Use first symbol or full image if no symbols found
    if extracted_symbols:
        images = extracted_symbols[0]
        labels = torch.arange(len(extracted_symbols))
        height = extracted_symbols[0].shape[0]
        width = extracted_symbols[0].shape[1]
    else:
        labels = torch.tensor([0])
        images = images.view(1, height, width)

    return images.unsqueeze(0), labels, height, width, 1


def load_cmyk_image() -> Tuple[torch.Tensor, torch.Tensor, int, int, int]:
    """
    Load CMYK image and treat each channel as a separate symbol.

    Returns:
        Tuple of (images, labels, height, width, channels)
    """
    script_dir = _get_script_directory()
    parent_dir = _get_parent_directory()

    filename = SOURCE_FILE if SOURCE_FILE else "Eugene_cmyk.tiff"

    for search_dir in [script_dir, parent_dir]:
        path = os.path.join(search_dir, filename)
        if os.path.exists(path):
            break
    else:
        path = os.path.join(script_dir, filename)

    # Create from JPEG if TIFF doesn't exist
    if not os.path.exists(path):
        jpeg_path = os.path.join(parent_dir, "Eugene.jpeg")
        if os.path.exists(jpeg_path):
            image = Image.open(jpeg_path).convert("CMYK")
            image.save(path)

    # Load CMYK image
    image = Image.open(path).convert("CMYK")
    image_array = np.array(image).astype(np.float32)
    height, width, channels = image_array.shape

    images = torch.from_numpy(image_array)
    labels = torch.arange(channels)

    return images, labels, height, width, channels


def load_data() -> Dict:
    """
    Load data from the configured source and compute delta field.

    Returns:
        Dictionary containing:
        - device: torch device (MPS or CPU)
        - original_data: original input tensor
        - delta_field: computed delta field tensor
        - labels: class labels tensor
        - height, width, channels: image dimensions
        - number_of_classes: count of symbols/classes
        - symbol_delta_fields: list of delta fields per symbol
        - is_color: whether data is color (CMYK)
        - color_space: "CMYK" or "RGB"
        - symbol_names: list of channel names for color data
        - delta_min, delta_max: range of delta field values
        - config: visualization configuration
    """
    global _cached_data
    if _cached_data is not None:
        return _cached_data

    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] Loading {SOURCE_NAME}...", flush=True)

    # Select loader based on source
    if SOURCE_NAME == "mnist":
        images, labels, height, width, channels = load_mnist_data()
    elif SOURCE_NAME == "png":
        images, labels, height, width, channels = load_png_image()
    elif SOURCE_NAME == "cmyk":
        images, labels, height, width, channels = load_cmyk_image()
    else:
        raise ValueError(f"Unknown source: {SOURCE_NAME}")

    # Use GPU if available (Apple MPS)
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    images = images.to(device)

    # Compute delta field: D = log(X + 1) - log(256 - X)
    delta_field = torch.log(images + 1.0) - torch.log(256.0 - images)

    # Extract individual symbol delta fields
    if SOURCE_NAME == "cmyk":
        symbol_delta_fields = [
            delta_field[:, :, channel] for channel in range(channels)
        ]
    else:
        symbol_delta_fields = [
            delta_field[index] for index in range(delta_field.shape[0])
        ]

    number_of_classes = len(symbol_delta_fields)

    print(
        f"[{time.strftime('%H:%M:%S')}] Data: {images.shape}, "
        f"Delta=[{delta_field.min():.2f}, {delta_field.max():.2f}] "
        f"({time.time() - start_time:.1f}s)"
    )

    # Determine color properties
    is_color = SOURCE_NAME == "cmyk"
    color_space = "CMYK" if is_color else "Grayscale"
    symbol_names = ["Cyan", "Magenta", "Yellow", "Key"] if is_color else None

    _cached_data = {
        "device": device,
        "original_data": images,
        "delta_field": delta_field,
        "labels": labels,
        "height": height,
        "width": width,
        "channels": channels,
        "number_of_classes": number_of_classes,
        "n_classes": number_of_classes,  # backward compatibility
        "symbol_delta_fields": symbol_delta_fields,
        "symbols_delta": symbol_delta_fields,  # backward compatibility
        "is_color": is_color,
        "color_space": color_space,
        "symbol_names": symbol_names,
        "delta_min": delta_field.min().item(),
        "delta_max": delta_field.max().item(),
        "config": asdict(CONFIG),
        "viz": asdict(CONFIG),  # backward compatibility
    }

    return _cached_data


def compute_sweep() -> Dict:
    """
    Compute threshold sweep across the delta field.

    For each threshold value, computes the percentage of pixels above threshold
    for each symbol/class. Also detects significant "jump" events where
    occupancy changes dramatically between adjacent thresholds.

    Returns:
        Dictionary containing:
        - thresholds: array of threshold values
        - occupancy_rates: tensor of shape (n_thresholds, n_classes)
          with percentage of pixels above threshold per class
        - jump_events: list of (threshold, class, before, after, change) tuples
        - jump_count: total number of detected jumps
    """
    global _cached_sweep
    if _cached_sweep is not None:
        return _cached_sweep

    data = load_data()
    device = data["device"]
    symbol_delta_fields = data["symbol_delta_fields"]
    number_of_classes = data["number_of_classes"]

    print(f"[{time.strftime('%H:%M:%S')}] Computing sweep...", flush=True)
    start_time = time.time()

    # Generate threshold values
    thresholds = np.arange(CONFIG.sweep_min, CONFIG.sweep_max, CONFIG.sweep_step)
    num_thresholds = len(thresholds)

    # Compute occupancy rates for each class
    occupancy_rates = torch.zeros(num_thresholds, number_of_classes, device=device)

    for class_id in range(number_of_classes):
        symbol = symbol_delta_fields[class_id].cpu().numpy().flatten()

        # Create histogram and compute cumulative distribution
        histogram, bin_edges = np.histogram(
            symbol,
            bins=np.linspace(CONFIG.sweep_min, CONFIG.sweep_max, num_thresholds + 1),
        )
        # Reverse cumulative sum: what percentage is above each threshold
        cumulative = np.cumsum(histogram[::-1])[::-1]
        occupancy_rates[:, class_id] = torch.from_numpy(cumulative / len(symbol) * 100)

    # Detect jump events: significant changes in occupancy
    jump_events = []
    occupancy_change = torch.abs(occupancy_rates[1:] - occupancy_rates[:-1])
    jump_mask = occupancy_change > CONFIG.jump_threshold
    jump_indices = torch.where(jump_mask)

    for idx, class_id in zip(jump_indices[0].tolist(), jump_indices[1].tolist()):
        threshold_value = round(thresholds[idx + 1], 4)
        before = occupancy_rates[idx, class_id].item()
        after = occupancy_rates[idx + 1, class_id].item()
        change = abs(after - before)
        jump_events.append((threshold_value, class_id, before, after, change))

    _cached_sweep = {
        "thresholds": thresholds,
        "occupancy_rates": occupancy_rates,
        "bits_tr_all": occupancy_rates,  # backward compatibility
        "jump_events": jump_events,
        "jump_count": len(jump_events),
    }

    print(
        f"  {num_thresholds} thresholds, {len(jump_events)} jumps "
        f"({time.time() - start_time:.1f}s)"
    )

    return _cached_sweep


def run_all_visualizations() -> None:
    """
    Execute all visualization scripts in sequence.

    Loads data, computes sweep, then iterates through all visualization modules
    and calls their render() function with the data and sweep results.
    """
    data = load_data()
    sweep = compute_sweep()

    output_directory = os.environ.get("VIZ_OUTPUT_DIR", _get_script_directory())
    script_directory = _get_script_directory()

    # List of visualization modules to execute
    visualization_modules = [
        "delta_histograms_by_class",
        "individual_delta_histograms",
        "horizon_heatmap",
        "horizon_animation",
        "scatter_mean_std",
        "jumps_analysis",
        "tsne_binary_profiles",
        "surface_3d",
        "cdf_by_class",
        "entropy_analysis",
        "original_vs_binary",
        "betti0_components",
        "betti1_holes",
        "euler_persistence",
        "persistence_landscape",
        "stress_map",
        "phase_volume",
    ]

    print(f"\n{'=' * 60}")
    print(
        f"[{time.strftime('%H:%M:%S')}] Rendering {len(visualization_modules)} visualizations"
    )
    print(f"{'=' * 60}")

    start_time = time.time()

    for index, module_name in enumerate(visualization_modules):
        module_path = os.path.join(script_directory, f"{module_name}.py")

        if not os.path.exists(module_path):
            print(f"  Warning: {module_name}.py not found")
            continue

        # Dynamically import module
        import importlib.util

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        render_function = getattr(module, "render", None)

        if not render_function:
            print(f"  Error: {module_name} missing render() function")
            continue

        print(
            f"\n[{time.strftime('%H:%M:%S')}] ({index + 1}/{len(visualization_modules)}) {module_name}"
        )

        try:
            render_function(data=data, sweep=sweep, out_dir=output_directory)
            print(f"  Success")
        except Exception as error:
            print(f"  Error: {error}")

    print(f"\n{'=' * 60}")
    print(f"Total: {time.time() - start_time:.0f}s")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    run_all_visualizations()
