#!/usr/bin/env python3
"""
Utilities for path and directory management.
"""

from pathlib import Path


def get_script_directory() -> Path:
    """Get the 'src' directory (formerly 'script')."""
    return Path(__file__).resolve().parent.parent


def get_parent_directory() -> Path:
    """Get the project root."""
    return get_script_directory().parent
