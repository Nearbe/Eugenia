#!/usr/bin/env python3
"""
ЕВГЕНИЯ — Unified entry point.
Usage:
    python3 generate.py              # ALL sources → output/{source}/
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

VENV_PY = os.path.join(SCRIPT_DIR, "venv", "bin", "python3")
PYTHON = VENV_PY if os.path.exists(VENV_PY) else sys.executable

SOURCES = ["mnist", "png", "cmyk"]


def run_source(source, source_file=""):
    t0 = time.time()
    print(f"\n[{time.strftime('%H:%M:%S')}] === {source.upper()} ===")

    out_dir = os.path.join(SCRIPT_DIR, "output", source)
    os.makedirs(out_dir, exist_ok=True)

    code = f"""
import sys
import os
sys.path.insert(0, '{SCRIPT_DIR}')
sys.path.insert(0, os.path.join('{SCRIPT_DIR}', 'script'))
os.environ['VIZ_SOURCE'] = '{source}'
os.environ['VIZ_OUT_DIR'] = '{out_dir}'
os.environ['VIZ_SOURCE_FILE'] = '{source_file}'
from script.common import run_all_visualizations
run_all_visualizations()
"""

    result = subprocess.run(
        [PYTHON, "-c", code], cwd=SCRIPT_DIR, capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"  Error: {result.stderr[:300]}")
        return False

    print(f"  done in {time.time() - t0:.0f}s")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate Δ-field visualizations")
    parser.add_argument("--source", choices=SOURCES + ["all"], default="all")
    parser.add_argument(
        "--file", default="", help="Source file (e.g., latin, cyrillic)"
    )
    args = parser.parse_args()

    sources = SOURCES if args.source == "all" else [args.source]

    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output", exist_ok=True)

    t0 = time.time()
    for src in sources:
        run_source(src, args.file)

    print(f"\n{'=' * 60}")
    print(f"Total: {time.time() - t0:.0f}s")
    print(f"Outputs:")
    for src in sources:
        out_dir = os.path.join("output", src)
        png = len([f for f in os.listdir(out_dir) if f.endswith(".png")])
        gif = len([f for f in os.listdir(out_dir) if f.endswith(".gif")])
        print(f"  {src}: {png} PNG, {gif} GIF → {out_dir}/")


if __name__ == "__main__":
    main()
