# ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║─Документация модуля──────────────────────────────────────────────────────────────────────────────║
# ║────────────────────────────────────────────────────────────────────────────────────────────────────║
"""
Orchestration for visualization data loading and sweep computation.

This module coordinates loading data from various sources (MNIST, PNG, CMYK)
using specialized loaders and running the core threshold sweep algorithm.
"""
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║─Импорт зависимостей──────────────────────────────────────────────────────────────────────────────║
# ║────────────────────────────────────────────────────────────────────────────────────────────────────║
import argparse
import logging
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from pathlib import Path
from typing import Optional

import torch
from tqdm import tqdm

from core.sweep import compute_sweep as compute_sweep_internal
from data.loaders import load_cmyk_image, load_fashion_data, load_mnist_data, load_png_image
from models.config import CONFIG
from models.types import SweepResults, VisualizationData
from utils.path_utils import get_script_directory

# ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║─Функции и методы: get_source_name────────────────────────────────────────────────────────────────║
# ║────────────────────────────────────────────────────────────────────────────────────────────────────║
def get_source_name() -> str:
    """Get the current data source name from environment variables."""
    return os.environ.get("VIZ_SOURCE", "mnist")

# ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║─Функции и методы: load_data──────────────────────────────────────────────────────────────────────║
# ║────────────────────────────────────────────────────────────────────────────────────────────────────║
def load_data(
    source_name: Optional[str] = None, source_file: Optional[str] = None
) -> VisualizationData:
    """
    Load data from the configured source and compute delta field.

    Args:
        source_name: Name of the data source (mnist, png, cmyk).
                     If None, reads from VIZ_SOURCE env var.
        source_file: Specific file to use. If None, reads from VIZ_SOURCE_FILE env var.

    Returns:
        VisualizationData object containing loaded data, delta fields, and metadata.
    """
    global _cached_data
    if _cached_data is not None:
        return _cached_data

    start_time = time.time()
    if source_name is None:
        source_name = get_source_name()
    if source_file is None:
        source_file = os.environ.get("VIZ_SOURCE_FILE", "")

    logger.info(f"Loading {source_name} (file: {source_file or 'default'})...")

    # Выбор загрузчика в зависимости от источника: MNIST для стандартных наборов,
    # PNG для произвольных изображений или CMYK для специфических цветовых каналов.
    if source_name == "mnist":
        images, labels, height, width, channels = load_mnist_data()
    elif source_name == "fashion":
        images, labels, height, width, channels = load_fashion_data()
    elif source_name == "png":
        images, labels, height, width, channels = load_png_image(source_file)
    elif source_name == "cmyk":
        images, labels, height, width, channels = load_cmyk_image(source_file)
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

    # Precompute delta if requested (CLI mode only)
    precompute_flag = os.environ.get("EUGENIA_PRECOMPUTE_DELTA", "false") == "true"
    if precompute_flag and Path("delta.npy").exists():
        delta_field = torch.load("delta.npy")
        logger.info("Using precomputed delta from file")
    else:
        # Вычисление дельта-поля: D = log(X + 1) - log(256 - X)
        # Это преобразование симметризует диапазон интенсивностей [0, 255] в логарифмическую шкалу,
        # центрированную вокруг 0. Это необходимо для корректного анализа пороговых переходов.
        delta_field = torch.log(images + 1.0) - torch.log(256.0 - images)

    # Разделение общего дельта-поля на индивидуальные поля для каждого символа или канала.
    # Это позволяет параллельно обрабатывать каждый класс в скриптах визуализации.
    if source_name == "cmyk":
        symbol_delta_fields = [delta_field[:, :, channel] for channel in range(channels)]
    else:
        symbol_delta_fields = [delta_field[index] for index in range(delta_field.shape[0])]

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
        config=asdict(CONFIG),
    )

    return _cached_data

# ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║─Функции и методы: compute_sweep──────────────────────────────────────────────────────────────────║
# ║────────────────────────────────────────────────────────────────────────────────────────────────────║
def compute_sweep(data: Optional[VisualizationData] = None) -> SweepResults:
    """
    Compute threshold sweep across the delta field.

    Args:
        data: VisualizationData object. If None, loads data using load_data().

    Returns:
        SweepResults object containing sweep results.
    """
    global _cached_sweep
    if _cached_sweep is not None:
        return _cached_sweep

    if data is None:
        data = load_data()
    _cached_sweep = compute_sweep_internal(data)
    return _cached_sweep

# ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║─Функции и методы: _render_single_visualization───────────────────────────────────────────────────║
# ║────────────────────────────────────────────────────────────────────────────────────────────────────║
def _render_single_visualization(
    module_name: str,
    viz_directory: Path,
    data: VisualizationData,
    sweep: SweepResults,
    output_directory: str,
):
    """
    Helper function to render a single visualization module in a separate process.
    """
    import importlib.util
    import sys
    import traceback
    from pathlib import Path

    # Добавление основной директории исходного кода (src) в пути поиска Python.
    # Это необходимо для того, чтобы подгружаемые модули визуализации могли
    # находить пакет eugenia и все его подмодули через абсолютный импорт.
    src_root = Path(viz_directory).parent.parent
    if str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))

    module_path = Path(viz_directory) / f"{module_name}.py"

    if not module_path.exists():
        return module_name, False, f"Module {module_name}.py not found"

    try:
        spec = importlib.util.spec_from_file_location(module_name, str(module_path))
        if spec is None or spec.loader is None:
            return module_name, False, f"Could not load module {module_name}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        render_function = getattr(module, "render", None)
        if not render_function:
            return module_name, False, "Missing render() function"

        render_function(data=data, sweep=sweep, out_dir=output_directory)
        return module_name, True, None
    except Exception as error:
        return module_name, False, str(error) + "\n" + traceback.format_exc()

# ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║─Функции и методы: run_all_visualizations─────────────────────────────────────────────────────────║
# ║────────────────────────────────────────────────────────────────────────────────────────────────────║
def run_all_visualizations(
    source_name: Optional[str] = None,
    output_directory: Optional[str] = None,
    source_file: Optional[str] = None,
    num_workers: Optional[int] = None,
    renderers: Optional[str] = None,
) -> None:
    """
    Execute all visualization scripts in sequence or parallel.

    Args:
        source_name: Name of the data source.
        output_directory: Directory to save visualizations.
        source_file: Specific file to use.
        num_workers: Number of parallel workers for rendering.
                     If None, defaults to min(cpu_count, 8).
        renderers: Comma-separated list of renderers to run.
                   If None, runs all available renderers.
    """
    data = load_data(source_name, source_file)
    sweep = compute_sweep(data)

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
            return obj.__class__(**{str(k): v for k, v in new_values.items()})  # type: ignore[arg-type]
        return obj

    data_cpu = to_cpu(data)  # type: ignore[arg-type]
    sweep_cpu = to_cpu(sweep)  # type: ignore[arg-type]

    if output_directory is None:
        output_directory = os.environ.get("VIZ_OUTPUT_DIR", str(get_script_directory()))

    script_directory = get_script_directory()
    viz_directory = script_directory / "renderers"

    # Автоматическое обнаружение всех модулей визуализации в директории script/visualizations.
    # Это позволяет отделить логику визуализации от ядра алгоритма и загрузчиков данных.
    visualization_modules = sorted(
        [f.stem for f in viz_directory.glob("*.py") if not f.name.startswith("__")]
    )

    # Фильтрация модулей, если указан список конкретных рендереров.
    if renderers:
        requested_renderers = [r.strip() for r in renderers.split(",")]
        visualization_modules = [m for m in visualization_modules if m in requested_renderers]

        if not visualization_modules:
            logger.warning(f"No matching renderers found for: {renderers}")
            return

    logger.info(f"{'=' * 60}")
    logger.info(f"Rendering {len(visualization_modules)} visualizations")

    start_time = time.time()

    # Использование ProcessPoolExecutor позволяет задействовать все ядра процессора
    # для рендеринга графиков. Ограничение в 8 воркеров предотвращает чрезмерное
    # потребление памяти при работе с большими наборами данных.
    if num_workers is None:
        num_workers = min(os.cpu_count() or 4, 8)
    logger.info(f"Using {num_workers} parallel workers")

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(
                _render_single_visualization,
                module_name,
                viz_directory,
                data_cpu,  # type: ignore[arg-type]
                sweep_cpu,  # type: ignore[arg-type]
                str(output_directory) if output_directory else "",
            )
            for module_name in visualization_modules
        ]

        # Use tqdm for progress tracking
        for i, future in enumerate(tqdm(futures, desc="Rendering", unit="module")):
            module_name, success, error = future.result()
            if not success:
                logger.error(f"{module_name} failed: {error}")

    logger.info(f"{'=' * 60}")
    logger.info(f"Total Rendering Time: {time.time() - start_time:.1f}s")
    logger.info(f"{'=' * 60}")

# ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║─Точка входа──────────────────────────────────────────────────────────────────────────────────────║
# ║────────────────────────────────────────────────────────────────────────────────────────────────────║
if __name__ == "__main__":
    import os

    print(f"CWD: {os.getcwd()}")
    # Test
    from PIL import Image

    print(f"PIL test: {Image.open('Eugene.jpeg')}")
    parser = argparse.ArgumentParser(description="Run visualizations for a specific source")
    parser.add_argument("--source", type=str, help="Source name (mnist, png, cmyk)")
    parser.add_argument("--output", type=str, help="Output directory")
    parser.add_argument("--file", type=str, help="Source file")
    parser.add_argument("--workers", type=int, help="Number of parallel workers")
    parser.add_argument("--sweep-min", type=float, help="Minimum threshold for sweep")
    parser.add_argument("--sweep-max", type=float, help="Maximum threshold for sweep")
    parser.add_argument("--sweep-step", type=float, help="Step size for sweep")
    parser.add_argument("--jump-threshold", type=float, help="Jump detection threshold (%%)")
    parser.add_argument("--renderers", type=str, help="Comma-separated list of renderers to run")
    parser.add_argument(
        "--precompute-delta",
        action="store_true",
        help="Generate and save delta.npy from current image",
    )

    args = parser.parse_args()

    # Precompute delta if requested
    if args.precompute_delta:
        from utils.delta_precompute import compute_and_save_delta

        compute_and_save_delta(args.file or "Eugene.jpeg", "delta.npy")
        sys.exit(0)

    # Update global config with command line arguments
    if args.sweep_min is not None:
        CONFIG.sweep_min = args.sweep_min
    if args.sweep_max is not None:
        CONFIG.sweep_max = args.sweep_max
    if args.sweep_step is not None:
        CONFIG.sweep_step = args.sweep_step
    if args.jump_threshold is not None:
        CONFIG.jump_threshold = args.jump_threshold

    # Pass precompute flag to load_data via environment variable
    if args.precompute_delta:
        os.environ["EUGENIA_PRECOMPUTE_DELTA"] = "true"

    run_all_visualizations(
        source_name=args.source,
        output_directory=args.output,
        source_file=args.file,
        num_workers=args.workers,
        renderers=args.renderers,
    )

# ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ║─Константы и конфигурация─────────────────────────────────────────────────────────────────────────║
# ║────────────────────────────────────────────────────────────────────────────────────────────────────║
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)
_cached_data: Optional[VisualizationData] = None
_cached_sweep: Optional[SweepResults] = None
# ╚════════════════════════════════════════════════════════════════════════════════════════════════════╝
