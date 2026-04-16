#!/usr/bin/env python3
"""
Main entry point for generating visualizations.

========================================
OVERVIEW
========================================

This is the entry point for the entire visualization pipeline.
It coordinates data loading, sweep computation, and
visualization rendering.

Usage:
    python3 generate.py              # Generate for all sources
    python3 generate.py --source mnist
    python3 generate.py --source png
    python3 generate.py --source png --file latin
    python3 generate.py --source cmyk

========================================
PIPELINE ARCHITECTURE
========================================

1. SOURCE SELECTION (--source flag)
    - mnist: Handwritten digits (10 classes)
    - png: PNG sprites (extracted via connected components)
    - cmyk: CMYK print image (4 channels as classes)

2. DATA LOADING (in script/common.py)
    - load_data() loads and preprocesses data
    - Computes delta field transformation
    - Returns cached data dictionary

3. SWEEP COMPUTATION (in script/common.py)
    - compute_sweep() runs threshold sweep
    - Generates ~111,000 threshold levels
    - Computes occupancy rates and jump events
    - Returns cached sweep dictionary

4. VISUALIZATION RENDERING (script/*.py)
    - Each script/*.py exports render(data, sweep, out_dir)
    - 16 visualizations generated per source
    - Output saved to output/{source}/

========================================
ENVIRONMENT VARIABLES
========================================

VIZ_SOURCE:       Data source (mnist, png, cmyk)
VIZ_SOURCE_FILE:  Specific file to use
VIZ_OUTPUT_DIR:   Output directory for visualizations

These are set automatically by generate.py
when running in subprocess mode.

========================================
OUTPUT STRUCTURE
========================================

output/
├── mnist/           # MNIST visualizations
│   ├── 00_delta_histograms_by_class.png
│   ├── 01_horizon_heatmap.png
│   ├── ...
│   └── 15_phase_volume.png
├── png/             # PNG sprite visualizations
└── cmyk/           # CMYK channel visualizations

Each source gets 15 PNG files plus 1 GIF animation.
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

# Determine script directory and Python interpreter
SCRIPT_DIRECTORY = Path(__file__).resolve().parent
VENV_PYTHON = SCRIPT_DIRECTORY / "venv" / "bin" / "python3"
PYTHON_INTERPRETER = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable

# Available data sources
AVAILABLE_SOURCES = ["mnist", "png", "cmyk", "fashion"]


def run_source(
    source_name: str,
    source_file: str = "",
    num_workers: int = None,
    sweep_min: float = None,
    sweep_max: float = None,
    sweep_step: float = None,
    jump_threshold: float = None,
    renderers: str = None,
) -> bool:
    """
    Run visualization generation for a specific source.

    Args:
        source_name: Name of the data source (mnist, png, cmyk)
        source_file: Optional specific file to use (e.g., latin, cyrillic)
        num_workers: Number of parallel workers for rendering.
        sweep_min, sweep_max, sweep_step: Custom sweep parameters.
        jump_threshold: Custom jump detection threshold.
        renderers: Comma-separated list of renderers to run.

    Returns:
        True if successful, False otherwise
    """
    start_time = time.time()
    logger.info(f"{'=' * 10} {source_name.upper()} {'=' * 10}")

    output_directory = SCRIPT_DIRECTORY / "output" / source_name
    output_directory.mkdir(parents=True, exist_ok=True)

    # Run the eugenia orchestrator script
    script_path = SCRIPT_DIRECTORY / "src" / "orchestrator.py"

    env = os.environ.copy()
    # Add src to PYTHONPATH so that 'from eugenia...' imports work
    src_dir = str(SCRIPT_DIRECTORY / "src")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{src_dir}{os.pathsep}{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = src_dir
    # Set data directory
    env["VIZ_DATA_DIR"] = str(SCRIPT_DIRECTORY / "data")

    cmd = [
        PYTHON_INTERPRETER,
        str(script_path),
        "--source",
        source_name,
        "--output",
        str(output_directory),
    ]
    if source_file:
        cmd.extend(["--file", source_file])
    if num_workers:
        cmd.extend(["--workers", str(num_workers)])
    if sweep_min is not None:
        cmd.extend(["--sweep-min", str(sweep_min)])
    if sweep_max is not None:
        cmd.extend(["--sweep-max", str(sweep_max)])
    if sweep_step is not None:
        cmd.extend(["--sweep-step", str(sweep_step)])
    if jump_threshold is not None:
        cmd.extend(["--jump-threshold", str(jump_threshold)])
    if renderers:
        cmd.extend(["--renderers", renderers])

    result = subprocess.run(cmd, cwd=str(SCRIPT_DIRECTORY), env=env)

    if result.returncode != 0:
        logger.error(f"  Error: {source_name} failed with return code {result.returncode}")
        return False

    logger.info(f"  Completed in {time.time() - start_time:.0f}s")
    return True


def main() -> None:
    """Parse arguments and run visualization generation."""
    parser = argparse.ArgumentParser(description="Generate delta field visualizations")
    parser.add_argument(
        "--source",
        choices=AVAILABLE_SOURCES + ["all"],
        default="all",
        help="Data source to process",
    )
    parser.add_argument("--file", default="", help="Specific file to use (e.g., latin, cyrillic)")
    parser.add_argument("--parallel", action="store_true", help="Run sources in parallel")
    parser.add_argument(
        "--workers", type=int, default=None, help="Number of parallel workers for rendering"
    )
    parser.add_argument("--sweep-min", type=float, help="Minimum threshold for sweep")
    parser.add_argument("--sweep-max", type=float, help="Maximum threshold for sweep")
    parser.add_argument("--sweep-step", type=float, help="Step size for sweep")
    parser.add_argument("--jump-threshold", type=float, help="Jump detection threshold (%%)")
    parser.add_argument("--renderers", type=str, help="Comma-separated list of renderers to run")
    arguments = parser.parse_args()

    # Determine which sources to process
    sources_to_process = AVAILABLE_SOURCES if arguments.source == "all" else [arguments.source]

    # Clean only the specific source directories
    for source in sources_to_process:
        output_dir = SCRIPT_DIRECTORY / "output" / source
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # Process each source
    start_time = time.time()

    if arguments.parallel and len(sources_to_process) > 1:
        logger.info(f"Running {len(sources_to_process)} sources in parallel...")
        with ProcessPoolExecutor(max_workers=len(sources_to_process)) as executor:
            futures = [
                executor.submit(
                    run_source,
                    source,
                    arguments.file,
                    arguments.workers,
                    arguments.sweep_min,
                    arguments.sweep_max,
                    arguments.sweep_step,
                    arguments.jump_threshold,
                    arguments.renderers,
                )
                for source in sources_to_process
            ]
            for future in futures:
                future.result()
    else:
        for source in sources_to_process:
            run_source(
                source,
                arguments.file,
                arguments.workers,
                arguments.sweep_min,
                arguments.sweep_max,
                arguments.sweep_step,
                arguments.jump_threshold,
                arguments.renderers,
            )

    # Print summary
    logger.info(f"{'=' * 60}")
    logger.info(f"Total time: {time.time() - start_time:.0f}s")
    logger.info("Outputs:")
    for source in sources_to_process:
        output_dir = SCRIPT_DIRECTORY / "output" / source
        png_count = len(list(output_dir.glob("*.png")))
        gif_count = len(list(output_dir.glob("*.gif")))
        logger.info(f"  {source}: {png_count} PNG, {gif_count} GIF -> {output_dir}/")


if __name__ == "__main__":
    main()
