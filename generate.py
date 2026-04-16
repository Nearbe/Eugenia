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
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor

# Determine script directory and Python interpreter
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

VENV_PYTHON = os.path.join(SCRIPT_DIRECTORY, "venv", "bin", "python3")
PYTHON_INTERPRETER = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

# Available data sources
AVAILABLE_SOURCES = ["mnist", "png", "cmyk"]


def run_source(source_name: str, source_file: str = "") -> bool:
    """
    Run visualization generation for a specific source.

    Args:
        source_name: Name of the data source (mnist, png, cmyk)
        source_file: Optional specific file to use (e.g., latin, cyrillic)

    Returns:
        True if successful, False otherwise
    """
    start_time = time.time()
    print(f"\n[{time.strftime('%H:%M:%S')}] === {source_name.upper()} ===")

    output_directory = os.path.join(SCRIPT_DIRECTORY, "output", source_name)
    os.makedirs(output_directory, exist_ok=True)

    # Set up environment for the subprocess
    env = os.environ.copy()
    env["VIZ_SOURCE"] = source_name
    env["VIZ_OUTPUT_DIR"] = output_directory
    env["VIZ_SOURCE_FILE"] = source_file

    # Run the common orchestration script
    script_path = os.path.join(SCRIPT_DIRECTORY, "script", "common.py")
    result = subprocess.run(
        [PYTHON_INTERPRETER, script_path],
        cwd=SCRIPT_DIRECTORY,
        env=env
    )

    if result.returncode != 0:
        print(f"  Error: {source_name} failed with return code {result.returncode}")
        return False

    print(f"  Completed in {time.time() - start_time:.0f}s")
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
    parser.add_argument(
        "--file", default="", help="Specific file to use (e.g., latin, cyrillic)"
    )
    parser.add_argument(
        "--parallel", action="store_true", help="Run sources in parallel"
    )
    arguments = parser.parse_args()

    # Determine which sources to process
    sources_to_process = (
        AVAILABLE_SOURCES if arguments.source == "all" else [arguments.source]
    )

    # Clean only the specific source directories
    for source in sources_to_process:
        output_dir = os.path.join(SCRIPT_DIRECTORY, "output", source)
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)

    # Process each source
    start_time = time.time()

    if arguments.parallel and len(sources_to_process) > 1:
        print(f"[{time.strftime('%H:%M:%S')}] Running {len(sources_to_process)} sources in parallel...")
        with ProcessPoolExecutor(max_workers=len(sources_to_process)) as executor:
            futures = [executor.submit(run_source, source, arguments.file) for source in sources_to_process]
            for future in futures:
                future.result()
    else:
        for source in sources_to_process:
            run_source(source, arguments.file)

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"Total time: {time.time() - start_time:.0f}s")
    print(f"Outputs:")
    for source in sources_to_process:
        output_dir = os.path.join("output", source)
        png_count = len([f for f in os.listdir(output_dir) if f.endswith(".png")])
        gif_count = len([f for f in os.listdir(output_dir) if f.endswith(".gif")])
        print(f"  {source}: {png_count} PNG, {gif_count} GIF -> {output_dir}/")


if __name__ == "__main__":
    main()
