#!/usr/bin/env python3
"""ЕВГЕНИЯ — Run MNIST visualizations."""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
sys.path.insert(0, os.path.join(script_dir, "script"))

from script.common import run_all_visualizations

run_all_visualizations()
