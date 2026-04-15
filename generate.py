#!/usr/bin/env python3
"""
ЕВГЕНИЯ — Unified entry point for all Δ-field visualizations.
Usage:
    python3 generate.py              # ALL sources → separate dir per source
    python3 generate.py --source mnist
    python3 generate.py --source png
    python3 generate.py --source cmyk
"""

import argparse
import os
import shutil
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Use venv python
VENV_PY = os.path.join(SCRIPT_DIR, "venv", "bin", "python3")
if os.path.exists(VENV_PY):
    PYTHON = VENV_PY
else:
    import subprocess

    result = subprocess.run(["which", "python3"], capture_output=True, text=True)
    PYTHON = result.stdout.strip() if result.returncode == 0 else sys.executable

SOURCES = ["mnist", "png", "cmyk"]


def run_source(source):
    """Run a single source."""
    if source == "mnist":
        script = os.path.join(SCRIPT_DIR, "generate_all.py")
    elif source == "png":
        script = os.path.join(SCRIPT_DIR, "generate_all_png.py")
    elif source == "cmyk":
        script = os.path.join(SCRIPT_DIR, "generate_all_cmyk.py")

    t0 = time.time()
    print(f"\n[{time.strftime('%H:%M:%S')}] === {source.upper()} ===")

    result = subprocess.run(
        [PYTHON, script], cwd=SCRIPT_DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        # Print only first few lines of error
        err_lines = result.stderr.split("\n")[:5]
        print(f"  Warning: {'; '.join(err_lines)}")
        return None  # Skip output collection

    print(f"  done in {time.time() - t0:.0f}s")
    return True


def collect_outputs(source):
    """Move outputs to output/{source}/ directory."""
    out_dir = os.path.join(SCRIPT_DIR, "output", source)
    os.makedirs(out_dir, exist_ok=True)

    # Specific output directories to move
    output_dirs = [
        "anim_frames",
        "individual_hists",
        "animation_frames",
        "individual_delta_hists",
    ]

    for f in os.listdir(SCRIPT_DIR):
        src_path = os.path.join(SCRIPT_DIR, f)
        # Move files: PNG, GIF
        if f.endswith((".png", ".gif")) and not f.startswith("output"):
            shutil.move(src_path, out_dir)
        # Move specific output directories
        elif f in output_dirs:
            shutil.move(src_path, out_dir)

    return out_dir


def main():
    parser = argparse.ArgumentParser(description="Generate Δ-field visualizations")
    parser.add_argument("--source", choices=SOURCES + ["all"], default="all")
    parser.add_argument("--output", default=os.path.join(SCRIPT_DIR, "output"))
    args = parser.parse_args()

    sources = SOURCES if args.source == "all" else [args.source]
    out_base = args.output

    if os.path.exists(out_base):
        shutil.rmtree(out_base)
    os.makedirs(out_base, exist_ok=True)

    t0 = time.time()

    for src in sources:
        result = run_source(src)
        if result is None:
            print(f"  {src} skipped (missing data)")
            continue
        if not result:
            continue
        collect_outputs(src)

    print(f"\n{'=' * 60}")
    print(f"Total: {time.time() - t0:.0f}s")
    print(f"Outputs:")
    for src in sources:
        out_dir = os.path.join(out_base, src)
        png = len([f for f in os.listdir(out_dir) if f.endswith(".png")])
        gif = len([f for f in os.listdir(out_dir) if f.endswith(".gif")])
        print(f"  {src}: {png} PNG, {gif} GIF → {out_dir}/")


if __name__ == "__main__":
    main()
