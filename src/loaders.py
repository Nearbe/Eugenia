#!/usr/bin/env python3
r"""
Data loaders for different visualization sources.

This module contains functions to load and preprocess data from MNIST,
PNG sprite sheets, and CMYK images.
"""

import os
from pathlib import Path
from typing import Tuple

import numpy as np
import torch
from PIL import Image
from scipy import ndimage

from params import CONFIG
from utils.path_utils import get_script_directory, get_parent_directory
from utils.tensor_utils import pad_tensors


def _find_source_file(filename: str) -> str:
    """
    Search for a file in the script and parent directories.

    Args:
        filename: The name of the file to find.

    Returns:
        The absolute path to the found file, or the original filename if not found.
    """
    script_dir = get_script_directory()
    parent_dir = get_parent_directory()

    # Поиск файла в текущей директории скрипта и родительской директории.
    # Это обеспечивает гибкость при запуске скрипта из разных мест и при
    # разной структуре папок с данными.
    for search_dir in [script_dir, parent_dir]:
        path = search_dir / filename
        if path.exists():
            return str(path)
    return str(script_dir / filename)


def load_mnist_data() -> Tuple[torch.Tensor, torch.Tensor, int, int, int]:
    """Load one sample per class from MNIST dataset."""
    return _load_npz_dataset("mnist.npz")


def load_fashion_data() -> Tuple[torch.Tensor, torch.Tensor, int, int, int]:
    """Load one sample per class from Fashion-MNIST dataset."""
    return _load_npz_dataset("fashion_mnist.npz")


def _load_npz_dataset(filename: str) -> Tuple[torch.Tensor, torch.Tensor, int, int, int]:
    """
    Internal helper to load one sample per class from a .npz dataset.

    Args:
        filename: Name of the .npz file (e.g., "mnist.npz", "fashion_mnist.npz").
    """
    # Поддержка переменной окружения VIZ_DATA_DIR для гибкой настройки пути к данным.
    # Если переменная не задана, используется путь по умолчанию (в соседней директории).
    # Это позволяет пользователям IDE легко менять директорию данных без изменения кода.
    default_data_dir = get_script_directory().parent.parent / "eugenia_data"
    data_dir_env = os.environ.get("VIZ_DATA_DIR")

    if data_dir_env:
        data_dir = Path(data_dir_env)
    else:
        data_dir = default_data_dir

    dataset_path = data_dir / filename

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")

    data_file = np.load(dataset_path)
    all_labels = data_file["y_train"]

    # Select one sample per class
    class_indices = []
    for class_id in range(CONFIG.number_of_classes):
        indices = np.where(all_labels == class_id)[0]
        if len(indices) == 0:
            raise ValueError(f"No samples found for class {class_id}")
        class_indices.append(indices[0])

    class_indices = np.array(class_indices)
    images = torch.from_numpy(data_file["x_train"][class_indices].astype(np.float32))
    labels = torch.arange(CONFIG.number_of_classes, dtype=torch.int32)

    height = CONFIG.image_height
    width = CONFIG.image_width
    channels = CONFIG.image_channels

    return images, labels, height, width, channels


def load_png_image(source_file: str = "") -> Tuple[torch.Tensor, torch.Tensor, int, int, int]:
    """
    Load PNG image and extract symbols via connected components.

    ========================================
    SYMBOL EXTRACTION ALGORITHM
    ========================================

    For PNG sprite sheets, we need to extract individual symbols
    (letters, digits, icons) from the combined image.

    Step 1: Invert image (line 114)
        Original: White background (255), black symbols (0)
        After invert: Black background (0), white symbols (255)
        This is because we want the symbols to be the "foreground"

    Step 2: Threshold at delta = -4.0 (line 117-119)
        This creates a binary mask where pixels above -4.0 are "active".
        The value -4.0 was chosen empirically - it's a low threshold
        that captures most of the symbol while excluding noise.

    Step 3: Connected components (line 120)
        scipy.ndimage.label() finds connected components in the
        binary mask. Each connected region gets a unique label.
        This is the "Betti-0" count at that threshold.

    Step 4: Bounding box extraction (lines 122-129)
        For each connected component, find its bounding box
        and extract that region as a separate symbol.
        This is essentially "cropping" each symbol individually.

    Why connected components works:
        - Separate symbols in a sprite sheet are typically not touching
        - Each symbol forms one connected region in the binary mask
        - The number of connected components = number of symbols

    ========================================
    ALTERNATIVE APPROACHES (for reference)
    ========================================

    1. Color-based separation: For multi-color sprites, use color as separator
    2. Contour tracing: Find external contours of each symbol
    3. Machine learning: Train a detector to find symbol bounding boxes

    The connected components approach is the simplest and fastest,
    making it ideal for this visualization pipeline.

    Returns:
        Tuple of (images, labels, height, width, channels)
    """
    filename = source_file if source_file else "cyrillic.png"
    path = _find_source_file(filename)

    # Попытка найти JPEG, если PNG отсутствует. Это позволяет работать с разными
    # форматами изображений без изменения кода загрузчика.
    if not os.path.exists(path):
        path = path.replace(".png", ".jpeg")

    # Перевод изображения в градации серого для унификации обработки всех типов данных.
    image = Image.open(path).convert("L")  # Convert to grayscale
    image_array = np.array(image).astype(np.float32)
    height, width = image_array.shape

    # Инверсия: белый фон (255) становится черным (0), а символы — белыми (255).
    # Это необходимо для того, чтобы символы считались "объектами" (foreground),
    # а фон — пустотой (background) при анализе связности.
    images = torch.from_numpy(255.0 - image_array)

    # Extract symbols using connected components on delta field
    threshold_value = -4.0
    images_cpu = images.numpy()
    binary_mask = (images_cpu > threshold_value).astype(np.uint8)
    labeled_array, num_components = ndimage.label(binary_mask)

    extracted_symbols = []
    # Вычисление координат каждого связного компонента для последующего вырезания
    # отдельных символов в самостоятельные изображения.
    for component_id in range(1, num_components + 1):
        coords = np.where(labeled_array == component_id)
        row_min = coords[0].min()
        row_max = coords[0].max() + 1
        col_min = coords[1].min()
        col_max = coords[1].max() + 1
        extracted_symbols.append(images[row_min:row_max, col_min:col_max])

    # Дополнение всех извлеченных символов до одинакового размера.
    # Это необходимо для формирования батча (единого тензора), что ускоряет
    # последующие вычисления.
    if not extracted_symbols:
        images = images.unsqueeze(0)
        labels = torch.tensor([0])
        height, width = images.shape[1], images.shape[2]
    else:
        # Pad all symbols to the same size
        images = pad_tensors(extracted_symbols)
        labels = torch.arange(len(extracted_symbols))
        height, width = images.shape[1], images.shape[2]

    return images, labels, height, width, 1


def load_cmyk_image(source_file: str = "") -> Tuple[torch.Tensor, torch.Tensor, int, int, int]:
    """
    Load CMYK image and treat each channel as a separate symbol.

    ========================================
    CMYK COLOR MODEL
    ========================================

    CMYK (Cyan, Magenta, Yellow, Key/Black) is a SUBTRACTIVE color model,
    unlike RGB which is ADDITIVE. This is used in printing because:

    - In RGB: Adding Red + Green + Blue = White (all light reflected)
    - In CMYK: Adding Cyan + Magenta + Yellow = Black (no light reflected)

    Why each channel is treated as a separate symbol:
        - Each CMYK channel represents ink density for that color
        - High values = more ink = darker in that color
        - Analyzing each channel separately reveals:
          * Contrast distribution within each ink
          * Overlapping regions between inks
          * Print quality and registration issues

    This is different from MNIST/PNG because:
        - MNIST: Each digit is a separate symbol (class)
        - PNG: Each extracted sprite is a separate symbol
        - CMYK: Each color channel IS a symbol (no extraction needed)

    ========================================
    WHY TIFF OVER JPEG FOR CMYK?
    ========================================

    JPEG uses RGB color space and loses CMYK information when converting.
    TIFF retains all CMYK channel data without compression artifacts.
    This is why line 163-168 creates a TIFF from JPEG if needed.

    Returns:
        Tuple of (images, labels, height, width, channels)
    """
    filename = source_file if source_file else "Eugene_cmyk.tiff"
    path = _find_source_file(filename)

    # Create from JPEG if TIFF doesn't exist
    if not os.path.exists(path):
        parent_dir = get_parent_directory()
        jpeg_path = parent_dir / "Eugene.jpeg"
        if jpeg_path.exists():
            image = Image.open(jpeg_path).convert("CMYK")
            image.save(path)

    # Load CMYK image
    image = Image.open(path).convert("CMYK")
    image_array = np.array(image).astype(np.float32)
    height, width, channels = image_array.shape

    images = torch.from_numpy(image_array)
    labels = torch.arange(channels)

    return images, labels, height, width, channels
