#!/usr/bin/env python3
import shutil
from pathlib import Path


def clean_output():
    project_root = Path(__file__).resolve().parent.parent.parent
    output_dir = project_root / "output"

    if output_dir.exists():
        print(f"Cleaning {output_dir}...")
        for item in output_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        print("Clean complete.")
    else:
        print("Output directory does not exist.")


if __name__ == "__main__":
    clean_output()
