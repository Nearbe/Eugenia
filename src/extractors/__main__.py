#!/usr/bin/env python3
"""CLI entry point for GGUF weight extraction.

Usage:
    python -m extractors.cli_extract --gguf model.gguf
"""

from .cli_extract import main

if __name__ == "__main__":
    main()
