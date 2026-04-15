#!/usr/bin/env python3
"""ЕВГЕНИЯ — Run CMYK visualizations."""

import os
import sys

# Add current directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
sys.path.insert(0, os.path.join(script_dir, "script"))

from script.common_cmyk import run_all_visualizations

run_all_visualizations()
