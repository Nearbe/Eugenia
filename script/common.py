#!/usr/bin/env python3
"""
Orchestration for visualization data loading and sweep computation.

This module coordinates loading data from various sources (MNIST, PNG, CMYK)
using specialized loaders and running the core threshold sweep algorithm.
"""

import logging
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from typing import Optional

import torch
from tqdm import tqdm

from loaders import load_mnist_data, load_png_image, load_cmyk_image
from models import VisualizationData, SweepResults
from params import CONFIG
from sweep import compute_sweep as compute_sweep_internal


# Environment variables for source selection
def get_source_name() -> str:
    """Get the current data source name from environment variables."""
    return os.environ.get("VIZ_SOURCE", "mnist")


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Глобальный кэш для предотвращения повторной загрузки данных и вычисления развертки в рамках одного сеанса
_cached_data: Optional[VisualizationData] = None
_cached_sweep: Optional[SweepResults] = None


def _get_script_directory() -> str:
    """Get the directory containing this script."""
    return os.path.dirname(os.path.abspath(__file__))


def load_data() -> VisualizationData:
    """
    Load data from the configured source and compute delta field.

    Returns:
        Dictionary containing loaded data, delta fields, and metadata.
    """
    global _cached_data
    if _cached_data is not None:
        return _cached_data

    start_time = time.time()
    source_name = get_source_name()
    logger.info(f"Loading {source_name}...")

    # Выбор загрузчика в зависимости от источника: MNIST для стандартных наборов, 
    # PNG для произвольных изображений или CMYK для специфических цветовых каналов.
    if source_name == "mnist":
        images, labels, height, width, channels = load_mnist_data()
    elif source_name == "png":
        images, labels, height, width, channels = load_png_image()
    elif source_name == "cmyk":
        images, labels, height, width, channels = load_cmyk_image()
    else:
        raise ValueError(f"Unknown source: {source_name}")

    # Использование GPU (CUDA или Apple MPS) для ускорения тензорных вычислений.
    # Если GPU недоступен, автоматически переходим на CPU.
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    images = images.to(device)

    # Вычисление дельта-поля: D = log(X + 1) - log(256 - X)
    # Это преобразование симметризует диапазон интенсивностей [0, 255] в логарифмическую шкалу,
    # центрированную вокруг 0. Это необходимо для корректного анализа пороговых переходов.
    delta_field = torch.log(images + 1.0) - torch.log(256.0 - images)

    # Разделение общего дельта-поля на индивидуальные поля для каждого символа или канала.
    # Это позволяет параллельно обрабатывать каждый класс в скриптах визуализации.
    if source_name == "cmyk":
        symbol_delta_fields = [
            delta_field[:, :, channel] for channel in range(channels)
        ]
    else:
        symbol_delta_fields = [
            delta_field[index] for index in range(delta_field.shape[0])
        ]

    number_of_classes = len(symbol_delta_fields)

    logger.info(
        f"Data: {images.shape}, "
        f"Delta=[{delta_field.min():.2f}, {delta_field.max():.2f}] "
        f"({time.time() - start_time:.1f}s)"
    )

    # Определение цветового пространства. CMYK обрабатывается отдельно, так как его
    # каналы (C, M, Y, K) имеют разный физический смысл по сравнению с классами MNIST.
    is_color = source_name == "cmyk"
    color_space = "CMYK" if is_color else "Grayscale"
    symbol_names = ["Cyan", "Magenta", "Yellow", "Key"] if is_color else None

    _cached_data = VisualizationData(
        device=device,
        original_data=images,
        delta_field=delta_field,
        labels=labels,
        height=height,
        width=width,
        channels=channels,
        number_of_classes=number_of_classes,
        symbol_delta_fields=symbol_delta_fields,
        is_color=is_color,
        color_space=color_space,
        symbol_names=symbol_names,
        delta_min=delta_field.min().item(),
        delta_max=delta_field.max().item(),
        config=asdict(CONFIG)
    )

    return _cached_data


def compute_sweep() -> SweepResults:
    """
    Compute threshold sweep across the delta field.

    Returns:
        SweepResults object containing sweep results.
    """
    global _cached_sweep
    if _cached_sweep is not None:
        return _cached_sweep

    data = load_data()
    _cached_sweep = compute_sweep_internal(data)
    return _cached_sweep


def _render_single_visualization(module_name: str, viz_directory: str, data: VisualizationData,
                                 sweep: SweepResults, output_directory: str):
    """
    Helper function to render a single visualization module in a separate process.
    """
    import sys
    import os
    import importlib.util
    import traceback

    # Добавление основной директории скриптов в пути поиска Python.
    # Это необходимо для того, чтобы подгружаемые модули визуализации могли
    # находить вспомогательные модули (utils, params, models) через обычный импорт.
    script_dir = os.path.dirname(viz_directory)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    module_path = os.path.join(viz_directory, f"{module_name}.py")

    if not os.path.exists(module_path):
        return module_name, False, f"Module {module_name}.py not found"

    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        render_function = getattr(module, "render", None)
        if not render_function:
            return module_name, False, "Missing render() function"

        render_function(data=data, sweep=sweep, out_dir=output_directory)
        return module_name, True, None
    except Exception as error:
        return module_name, False, str(error) + "\n" + traceback.format_exc()


def run_all_visualizations() -> None:
    """
    Execute all visualization scripts in sequence or parallel.
    """
    data = load_data()
    sweep = compute_sweep()

    # Перенос данных на CPU необходим для корректной передачи объектов между процессами
    # через pickle при использовании ProcessPoolExecutor. Кроме того, большинство
    # модулей визуализации используют numpy и matplotlib, которые работают на CPU.
    def to_cpu(obj):
        if isinstance(obj, torch.Tensor):
            return obj.cpu()
        if isinstance(obj, dict):
            return {k: to_cpu(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [to_cpu(v) for v in obj]
        if hasattr(obj, "__dataclass_fields__"):
            from dataclasses import fields
            new_values = {f.name: to_cpu(getattr(obj, f.name)) for f in fields(obj)}
            return obj.__class__(**new_values)
        return obj

    data_cpu = to_cpu(data)
    sweep_cpu = to_cpu(sweep)

    output_directory = os.environ.get("VIZ_OUTPUT_DIR", _get_script_directory())
    script_directory = _get_script_directory()
    viz_directory = os.path.join(script_directory, "visualizations")

    # Автоматическое обнаружение всех модулей визуализации в директории script/visualizations.
    # Это позволяет отделить логику визуализации от ядра алгоритма и загрузчиков данных.
    visualization_modules = sorted([
        f[:-3] for f in os.listdir(viz_directory)
        if f.endswith(".py") and not f.startswith("__")
    ])

    print(f"\n{'=' * 60}")
    logger.info(f"Rendering {len(visualization_modules)} visualizations")

    start_time = time.time()

    # Использование ProcessPoolExecutor позволяет задействовать все ядра процессора
    # для рендеринга графиков. Ограничение в 8 воркеров предотвращает чрезмерное
    # потребление памяти при работе с большими наборами данных.
    num_workers = min(os.cpu_count() or 4, 8)
    logger.info(f"Using {num_workers} parallel workers")

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(
                _render_single_visualization,
                module_name,
                viz_directory,
                data_cpu,
                sweep_cpu,
                output_directory
            )
            for module_name in visualization_modules
        ]

        # Use tqdm for progress tracking
        for i, future in enumerate(tqdm(futures, desc="Rendering", unit="module")):
            module_name, success, error = future.result()
            if not success:
                logger.error(f"{module_name} failed: {error}")

    print(f"\n{'=' * 60}")
    print(f"Total Rendering Time: {time.time() - start_time:.1f}s")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    run_all_visualizations()
