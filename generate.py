#!/usr/bin/env python3
"""
Main entry point for generating visualizations.

Usage:
    python3 generate.py              # Generate for all sources
    python3 generate.py --source mnist
    python3 generate.py --source png
    python3 generate.py --source png --file latin
    python3 generate.py --source cmyk
"""

import argparse
import os
import shutil
import subprocess
import sys
import time


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

    # Build code to execute in subprocess
    execution_code = f"""
import sys
import os
sys.path.insert(0, '{SCRIPT_DIRECTORY}')
sys.path.insert(0, os.path.join('{SCRIPT_DIRECTORY}', 'script'))
os.environ['VIZ_SOURCE'] = '{source_name}'
os.environ['VIZ_OUTPUT_DIR'] = '{output_directory}'
os.environ['VIZ_SOURCE_FILE'] = '{source_file}'
from script.common import run_all_visualizations
run_all_visualizations()
"""

    result = subprocess.run(
        [PYTHON_INTERPRETER, "-c", execution_code],
        cwd=SCRIPT_DIRECTORY,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"  Error: {result.stderr[:300]}")
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
    arguments = parser.parse_args()

    # Determine which sources to process
    sources_to_process = (
        AVAILABLE_SOURCES if arguments.source == "all" else [arguments.source]
    )

    # Clean and create output directory
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output", exist_ok=True)

    # Process each source
    start_time = time.time()
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
