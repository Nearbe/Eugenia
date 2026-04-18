#!/usr/bin/env python3
"""
Performance metrics and timing decorators for Nucleus.
"""

import logging
import time
from functools import wraps
from typing import Callable, Any, Optional

import torch

logger = logging.getLogger(__name__)


def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure execution time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        logger.info(f"{func.__name__} executed in {elapsed:.3f}s")
        return result

    return wrapper


def gpu_memory_tracker(func: Callable) -> Callable:
    """Decorator to track GPU memory usage before and after function execution."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
            mem_before = torch.cuda.memory_allocated()
            logger.info(f"GPU memory before {func.__name__}: {mem_before / 1024**2:.1f} MB")

        result = func(*args, **kwargs)

        if torch.cuda.is_available():
            mem_after = torch.cuda.memory_allocated()
            mem_peak = torch.cuda.max_memory_allocated()
            logger.info(f"GPU memory after {func.__name__}: {mem_after / 1024**2:.1f} MB")
            logger.info(f"GPU peak memory: {mem_peak / 1024**2:.1f} MB")

        return result

    return wrapper


class PerformanceMonitor:
    """Context manager for monitoring performance of code blocks."""

    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time: Optional[float] = None

    def __enter__(self) -> "PerformanceMonitor":
        self.start_time = time.time()
        logger.info(f"Starting {self.operation_name}")

        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        elapsed = time.time() - self.start_time
        logger.info(f"Completed {self.operation_name} in {elapsed:.3f}s")

        if torch.cuda.is_available():
            mem_peak = torch.cuda.max_memory_allocated()
            logger.info(f"Peak GPU memory: {mem_peak / 1024**2:.1f} MB")


def format_bytes(num_bytes: int) -> str:
    """Format bytes into human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"
