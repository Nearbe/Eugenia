#!/usr/bin/env python3
"""
CLI wrapper for GGUF weight extraction.

Usage:
    python extract_weights.py --gguf model.gguf
    python extract_weights.py --gguf model.gguf --pattern "*.weight"
    python extract_weights.py --gguf model.gguf --output weights.npz

See: python extract_weights.py --help
"""

import sys
from pathlib import Path

# Add src/ to path so nucleus imports work
_project_root = Path(__file__).resolve().parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.extractors.cli_extract import main  # noqa: E402

if __name__ == "__main__":
    main()
