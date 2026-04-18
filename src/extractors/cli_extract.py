#!/usr/bin/env python3
"""
CLI tool for extracting weight tensors from GGUF model files.

Usage:
    # Extract all weights matching "*.weight" pattern
    python -m extractors.cli_extract --gguf path/to/model.gguf

    # Extract specific tensor
    python -m extractors.cli_extract --gguf model.gguf --name "model.layers.0.self_attn.q_proj.weight"

    # Extract with custom pattern
    python -m extractors.cli_extract --gguf model.gguf --pattern "*.k_proj.weight"

    # Save extracted weights to NPZ
    python -m extractors.cli_extract --gguf model.gguf --output weights.npz

    # Save extracted weights to NumPy .npy files (one per tensor)
    python -m extractors.cli_extract --gguf model.gguf --output-dir extracted_weights/

    # Show model info only
    python -m extractors.cli_extract --gguf model.gguf --info-only

    # Show tensor names only
    python -m extractors.cli_extract --gguf model.gguf --list-tensors

    # Limit to first N tensors
    python -m extractors.cli_extract --gguf model.gguf --limit 10

    # Extract specific layers
    python -m extractors.cli_extract --gguf model.gguf --layer-range 0-5
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add src/ to path so nucleus imports work when running as:
#   python -m extractors.cli_extract  (from project root)
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import numpy as np

from .gguf_extractor import GGUFExtractor


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract weight tensors from GGUF model files.")
    parser.add_argument("--gguf", "-g", required=True, help="Path to the .gguf model file.")
    parser.add_argument("--name", "-n", default=None, help="Extract a single tensor by name.")
    parser.add_argument(
        "--pattern",
        "-p",
        default="*.weight",
        help="Glob pattern for tensor names (default: *.weight).",
    )
    parser.add_argument("--output", "-o", default=None, help="Save extracted weights to .npz file.")
    parser.add_argument(
        "--output-dir", "-d", default=None, help="Save each tensor as a separate .npy file."
    )
    parser.add_argument("--info-only", "-i", action="store_true", help="Print model info and exit.")
    parser.add_argument(
        "--list-tensors", "-l", action="store_true", help="List all tensor names and exit."
    )
    parser.add_argument(
        "--limit", "-L", type=int, default=None, help="Limit extraction to first N tensors."
    )
    parser.add_argument(
        "--layer-range",
        "-r",
        default=None,
        help="Extract tensors from specific layer range (e.g., 0-5).",
    )

    args = parser.parse_args()

    # Initialize extractor
    try:
        extractor = GGUFExtractor(args.gguf)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Info-only mode
    if args.info_only:
        info = extractor.get_model_info()
        print(json.dumps(info, indent=2, default=str))
        return

    # List tensors mode
    if args.list_tensors:
        for name in extractor.tensor_names:
            info = extractor.get_tensor_info(name)
            shape_str = " x ".join(str(d) for d in info.shape) if info.shape else "0"
            print(f"{name:80s} {info.dtype.name:10s} {shape_str}")
        return

    # Determine which tensors to extract
    if args.name:
        tensor_names = [args.name]
    elif args.layer_range:
        # Parse layer range like "0-5" or "3" (single layer)
        parts = args.layer_range.split("-")
        if len(parts) == 1:
            start_layer = int(parts[0])
            end_layer = start_layer + 1
        else:
            start_layer = int(parts[0])
            end_layer = int(parts[1]) + 1

        tensor_names = []
        for layer_idx in range(start_layer, end_layer):
            tensor_names.extend(extractor.get_layer_tensors(layer_idx))
    else:
        # Use pattern matching
        tensor_names = extractor.get_weight_keys(args.pattern)

    # Limit extraction
    if args.limit is not None:
        tensor_names = tensor_names[: args.limit]

    print(f"Extracting {len(tensor_names)} tensors from {extractor.path}...")

    # Extract tensors
    extracted: dict[str, np.ndarray] = {}
    for name in tensor_names:
        try:
            tensor = extractor.extract_tensor(name)
            if tensor is not None:
                extracted[name] = tensor
        except Exception as e:
            print(f"  Warning: failed to extract '{name}': {e}", file=sys.stderr)

    print(f"Successfully extracted {len(extracted)} tensors.")

    # Save results
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save as NPZ (compressed archive of .npy files)
        np.savez_compressed(str(output_path), **extracted)
        print(f"Saved to {output_path} ({output_path.stat().st_size / 1024 / 1024:.1f} MB)")

    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for name, tensor in extracted.items():
            # Sanitize tensor name for filename (replace dots and slashes)
            safe_name = name.replace(".", "_").replace("/", "_")
            file_path = output_dir / f"{safe_name}.npy"
            np.save(str(file_path), tensor)

        total_size = sum(f.stat().st_size for f in output_dir.glob("*.npy"))
        print(f"Saved to {output_dir} ({total_size / 1024 / 1024:.1f} MB total)")

    # Also print summary to stdout
    if not args.output and not args.output_dir:
        for name, tensor in list(extracted.items())[:20]:  # limit output
            shape_str = " x ".join(str(d) for d in tensor.shape) if tensor.shape else "0"
            print(f"  {name:80s} {tensor.dtype.name:10s} {shape_str}")
        if len(extracted) > 20:
            print(f"  ... and {len(extracted) - 20} more tensors")


if __name__ == "__main__":
    main()
