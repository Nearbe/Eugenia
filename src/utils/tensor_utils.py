#!/usr/bin/env python3
"""
Utilities for PyTorch tensor manipulations.
"""

from typing import List

import torch


def pad_tensors(tensors: List[torch.Tensor], padding_value: float = 0.0) -> torch.Tensor:
    """
    Pad a list of 2D tensors to the same maximum height and width.

    Args:
        tensors: List of 2D PyTorch tensors
        padding_value: Value to use for padding

    Returns:
        3D tensor of shape (len(tensors), max_h, max_w)
    """
    if not tensors:
        return torch.empty(0)

    max_h = max(t.shape[0] for t in tensors)
    max_w = max(t.shape[1] for t in tensors)

    padded_tensors = []
    for t in tensors:
        h, w = t.shape
        # Calculate padding: (left, right, top, bottom)
        pad_h = max_h - h
        pad_w = max_w - w

        # In torch.nn.functional.pad, padding is (padding_left, padding_right, padding_top, padding_bottom)
        padding = (0, pad_w, 0, pad_h)
        padded = torch.nn.functional.pad(t, padding, mode="constant", value=padding_value)
        padded_tensors.append(padded)

    return torch.stack(padded_tensors)
