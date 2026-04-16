#!/usr/bin/env python3
"""
Threshold sweep algorithm for delta field analysis.

This module implements the core sweep algorithm that measures pixel occupancy
across a range of threshold values in the delta field.
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import torch
from tqdm import tqdm

from models import VisualizationData, SweepResults
from params import CONFIG

logger = logging.getLogger(__name__)


def compute_sweep(data: VisualizationData) -> SweepResults:
    """
    Compute threshold sweep across the delta field.

    Step 1: Generate thresholds
        Creates ~111,000 threshold values from -5.546 to 5.546.
        Step size: 0.0001 (defined in params.py).

    Step 2: Compute histogram per class
        For each symbol/class, compute histogram of delta values.
        The bins span the entire threshold range.
        This is MUCH faster than thresholding each pixel at each threshold.

    Step 3: Reverse cumulative sum
        cumulative[i] = number of pixels above threshold[i].
        Dividing by total pixels gives percentage (0-100%).

    Jump Detection:
        A "jump" is when occupancy changes by more than 1% between
        adjacent thresholds.

    Args:
        data: Dictionary containing loaded data (delta fields).

    Returns:
        Dictionary containing:
        - thresholds: array of threshold values
        - occupancy_rates: tensor of shape (n_thresholds, n_classes)
        - jump_events: list of (threshold, class, before, after, change) tuples
        - jump_count: total number of detected jumps
    """
    device = data.device
    symbol_delta_fields = data.symbol_delta_fields
    number_of_classes = data.number_of_classes

    logger.info("Computing sweep...")
    start_time = time.time()

    # Генерация сетки пороговых значений. Диапазон и шаг подобраны так, чтобы 
    # охватить все значимые значения дельта-поля с достаточной детализацией для 
    # обнаружения резких переходов (прыжков).
    thresholds = np.arange(CONFIG.sweep_min, CONFIG.sweep_max, CONFIG.sweep_step)
    num_thresholds = len(thresholds)

    # Вычисление доли "активных" пикселей для каждого класса. Для оптимизации вместо
    # прямого сравнения каждого пикселя с каждым порогом используется гистограммный метод.
    occupancy_rates = torch.zeros(num_thresholds, number_of_classes, device=device)

    def process_class(class_id):
        symbol = symbol_delta_fields[class_id]

        # Вычисление гистограммы на CPU, так как реализация torch.histc для MPS
        # может работать некорректно или быть менее эффективной для большого числа бинов.
        symbol_cpu = symbol.cpu()
        # Использование обратной кумулятивной суммы позволяет за O(N) получить количество
        # пикселей выше каждого порога. Это ключевая оптимизация алгоритма развертки.
        histogram = torch.histc(
            symbol_cpu,
            bins=num_thresholds,
            min=CONFIG.sweep_min,
            max=CONFIG.sweep_max
        )
        # Преобразование гистограммы в долю пикселей (в процентах), превышающих порог.
        cumulative = torch.cumsum(histogram.flip(0), dim=0).flip(0)
        return class_id, (cumulative / symbol.numel() * 100.0).to(torch.float32)

    # Использование ThreadPoolExecutor для параллельной обработки классов.
    # Так как операции PyTorch освобождают GIL, это эффективно даже для CPU-вычислений.
    # Однако для MPS (Apple Silicon) последовательная обработка часто оказывается быстрее
    # из-за исключения накладных расходов на переключение контекста GPU-ядер.
    if device.type == "mps":
        results = [process_class(i) for i in tqdm(range(number_of_classes), desc="Sweep (MPS)", leave=False)]
    else:
        with ThreadPoolExecutor(max_workers=min(number_of_classes, 8)) as executor:
            results = list(tqdm(executor.map(process_class, range(number_of_classes)),
                                total=number_of_classes, desc="Sweep (CPU/CUDA)", leave=False))

    for class_id, rates in results:
        occupancy_rates[:, class_id] = rates.to(device)

    # Детекция "прыжков" — моментов резкого изменения заполненности (более 1%).
    # Такие события обычно соответствуют важным топологическим или структурным 
    # изменениям в анализируемых образах при изменении порога фильтрации.
    jump_events = []
    occupancy_change = torch.abs(occupancy_rates[1:] - occupancy_rates[:-1])
    jump_mask = occupancy_change > CONFIG.jump_threshold
    jump_indices = torch.where(jump_mask)

    for threshold_idx, class_id in zip(jump_indices[0].tolist(), jump_indices[1].tolist()):
        threshold_value = round(thresholds[threshold_idx + 1], 4)
        before = occupancy_rates[threshold_idx, class_id].item()
        after = occupancy_rates[threshold_idx + 1, class_id].item()
        change = abs(after - before)
        jump_events.append((threshold_value, class_id, before, after, change))

    sweep_results = SweepResults(
        thresholds=thresholds,
        occupancy_rates=occupancy_rates,
        jump_events=jump_events,
        jump_count=len(jump_events),
    )

    logger.info(
        f"  {num_thresholds} thresholds, {len(jump_events)} jumps "
        f"({time.time() - start_time:.1f}s)"
    )

    return sweep_results
