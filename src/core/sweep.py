#!/usr/bin/env python3
"""
Threshold sweep algorithm for delta field analysis.

This module implements the core sweep algorithm that measures pixel occupancy
across a range of threshold values in the delta field.
"""

from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from time import time

from numpy import arange, array, linspace, ndarray, round
from torch import abs, cumsum, float32, histc, where, zeros
from tqdm import tqdm

from .config import CONFIG
from .types import SweepResults, VisualizationData

logger = getLogger(__name__)


# ============================================================
# Solenoid encoding per Essentials [23_Соленоид.md]
# ============================================================


def encode_solenoid_trajectory(delta_value: float, depth: int = 30) -> list:
    """
    Кодирование траектории точки на соленоиде.

    Согласно Essentials [23_Соленоид.md]:
    Точка соленоида — это вся траектория масштабирований:
    z₀ = D(z₁) = D²(z₂) = ... = Dⁿ(zₙ)

    Каждая точка кодируется двоичной дробью:
    ξ = 0.ε₀ε₁ε₂… где εₙ ∈ {Ω, D(Id)}

    "Происхождение важнее текущего вида" — точки близки,
    если их двоичные истории совпадают на многих первых шагах.

    Args:
        delta_value: Значение дельта-поля
        depth: Глубина кодирования (количество бит)

    Returns:
        Список битов [ε₀, ε₁, ..., εₙ₋₁] — двоичная история
    """
    binary = []
    current = abs(delta_value)

    for _ in range(depth):
        # Compare current with branching threshold D(Id) = 2
        if current >= 2.0:
            binary.append(1)  # D(Id) branch
            current = current / 2.0
        else:
            binary.append(0)  # Ω branch (compression)
            current = current * 2.0

    return binary


def solenoid_distance(traj_a: list, traj_b: list) -> float:
    """
    Расстояние на соленоиде — по совпадению начальных битов.

    Согласно Essentials [23_Соленоид.md, XI. Метрика Близости]:
    Две точки близки, если их двоичные истории
    совпадают на многих первых шагах.

    Если истории расходятся рано — точки далеки,
    даже если текущие значения близки.
    "Происхождение важнее текущего вида."

    Args:
        traj_a: Первая траектория (список битов)
        traj_b: Вторая траектория (список битов)

    Returns:
        Близость: 2^(-k) где k — первый различающийся бит
    """
    k = 0
    for a, b in zip(traj_a, traj_b):
        if a != b:
            break
        k += 1
    return 2.0 ** (-k)


# ============================================================
# Renormalization Group sweep per Essentials [28_Масштабная_инвариантность.md]
# ============================================================


def rg_aware_sweep(sweep_min: float, sweep_max: float, n_levels: int = 160000) -> ndarray:
    """
    RG-aware threshold sweep — пороговая развертка с ренормгруппой.

    Согласно Essentials [28_Масштабная_инвариантность.md]:
    Операция :Ω = D(x) = 2x — это дискретный шаг Ренормализационной Группы.
    β(g) = D(g) ⊖ g = g — линейный поток.
    g_{n+1} = D(g_n) — экспоненциальный рост.

    Вместо uniform spacing (t + step):
    - На уровнях Хребта: t_{n+1} = D(t_n) = 2·t_n (ветвление)
    - Между уровнями: t_{n+1} = H(t_n) = t_n/2 (сжатие)
    - Это даёт фрактальное распрежение, согласованное с branching structure

    Args:
        sweep_min: Минимальный порог
        sweep_max: Максимальный порог
        n_levels: Количество порогов

    Returns:
        Массив порогов с RG-aware распределением
    """
    thresholds = []

    # Generate thresholds at each branching level
    for level in range(int(sweep_min), int(sweep_max) + 1):
        base = 2**level  # Dⁿ(Id)
        if sweep_min <= base <= sweep_max:
            thresholds.append(base)

            # Add p-adic refined thresholds around each branching point
            for k in range(-4, 5):
                refined = base * (2**k)
                if sweep_min <= refined <= sweep_max and refined not in thresholds:
                    thresholds.append(refined)

    thresholds = sorted(set(thresholds))

    # If too few, interpolate; if too many, sample
    if len(thresholds) < n_levels:
        # Interpolate with RG-aware spacing
        extra = linspace(sweep_min, sweep_max, n_levels)
        combined = sorted(set(thresholds) | set(round(extra, 6)))
        return array(combined)[:n_levels]
    else:
        # Sample uniformly
        indices = linspace(0, len(thresholds) - 1, n_levels).astype(int)
        return array(thresholds)[indices]


# ============================================================
# Inverse jump analysis per Essentials [20_Инверсия_Гёделя-Тьюринга.md]
# ============================================================


def inverse_jump_analysis(jump_events: list, n_back: int = 10) -> list:
    """
    Обратный анализ прыжков — от следствия к причине.

    Согласно Essentials [20_Инверсия_Гёделя-Тьюринга.md]:
    H(D(a)) = a — инверсия позволяет идти назад от эффекта к причине.
    "Невозможность — это тупик для тех, кто ходит только вперед.
    Для тех, кто умеет ходить назад, тупиков нет."

    Для каждого прыжка при пороге t, вычисляем H^k(t) = t/2^k
    чтобы проследить до структурного происхождения.

    Args:
        jump_events: Список прыжков [(threshold, class_id, before, after, change), ...]
        n_back: Количество шагов назад (H^k)

    Returns:
        Список обратных траекторий для каждого прыжка
    """
    inverse_traces = []

    for t_val, class_id, before, after, change in jump_events:
        trace = []
        current = t_val

        for k in range(n_back):
            trace.append(
                {
                    "step": k,
                    "threshold": current,
                    "compression": f"H^{k}(t) = {current:.4f}",
                }
            )
            current = current / 2.0  # H(x) = x/2

        inverse_traces.append(
            {
                "jump_threshold": t_val,
                "class_id": class_id,
                "magnitude": change,
                "inverse_trace": trace,
                "origin": trace[-1]["threshold"],
            }
        )

    return inverse_traces


# ============================================================
# Binomial probability baseline per Essentials [27_Вероятность.md]
# ============================================================


def binomial_probability(k: int, n: int) -> float:
    """
    Биномиальная вероятность: P(X=k) = C(n,k) / 2ⁿ.

    Согласно Essentials [27_Вероятность.md]:
    P(A) = (Число ветвей A) : (Все ветви)
    При n Актах (:Ω) с равным выбором: P(k) = C(n,k) : Dⁿ(Id)

    Args:
        k: Количество успехов
        n: Количество испытаний

    Returns:
        Вероятность P(X=k)
    """
    from math import comb

    total_branches = 2**n
    favorable_branches = comb(n, k)
    return favorable_branches / total_branches


def theoretical_occupancy(n_pixels: int, threshold_fraction: float) -> float:
    """
    Теоретическая occupancy как биномиальная вероятность.

    Если каждый пиксель — это результат бинарного акта (:Ω),
    то occupancy = P(пиксель > порог) = fraction of branches above threshold.

    При равномерном распределении:
    P(δ > t) ≈ 1 - CDF(t) ≈ binomial CDF complement

    Args:
        n_pixels: Количество пикселей
        threshold_fraction: Доля пикселей выше порога (эмпирическая)

    Returns:
        Теоретическая биномиальная вероятность
    """
    k = int(n_pixels * threshold_fraction)
    n = n_pixels
    prob = binomial_probability(k, n)

    # Cumulative: P(X >= k)
    from math import comb

    cumulative = sum(comb(n, i) / (2**n) for i in range(k, n + 1))
    return cumulative


def compute_sweep(data: VisualizationData) -> SweepResults:
    """
    Compute threshold sweep across the delta field.

    Step 1: Generate thresholds
        Creates ~160,000 threshold values from -8 to 8 (log2-based delta field range).
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
    start_time = time()

    # Генерация сетки пороговых значений. Диапазон и шаг подобраны так, чтобы
    # охватить все значимые значения дельта-поля с достаточной детализацией для
    # обнаружения резких переходов (прыжков).
    thresholds = arange(CONFIG.sweep_min, CONFIG.sweep_max, CONFIG.sweep_step)
    num_thresholds = len(thresholds)

    # Вычисление доли "активных" пикселей для каждого класса. Для оптимизации вместо
    # прямого сравнения каждого пикселя с каждым порогом используется гистограммный метод.
    occupancy_rates = zeros(num_thresholds, number_of_classes, device=device)

    def process_class(class_id):
        symbol = symbol_delta_fields[class_id]

        # Вычисление гистограммы на CPU, так как реализация torch.histc для MPS
        # может работать некорректно или быть менее эффективной для большого числа бинов.
        symbol_cpu = symbol.cpu()
        # Использование обратной кумулятивной суммы позволяет за O(N) получить количество
        # пикселей выше каждого порога. Это ключевая оптимизация алгоритма развертки.
        histogram = histc(
            symbol_cpu, bins=num_thresholds, min=CONFIG.sweep_min, max=CONFIG.sweep_max
        )
        # Преобразование гистограммы в долю пикселей (в процентах), превышающих порог.
        cumulative = cumsum(histogram.flip(0), dim=0).flip(0)
        return class_id, (cumulative / symbol.numel() * 100.0).to(float32)

    # Использование ThreadPoolExecutor для параллельной обработки классов.
    # Так как операции PyTorch освобождают GIL, это эффективно даже для CPU-вычислений.
    # Однако для MPS (Apple Silicon) последовательная обработка часто оказывается быстрее
    # из-за исключения накладных расходов на переключение контекста GPU-ядер.
    if device.type == "mps":
        results = [
            process_class(i)
            for i in tqdm(range(number_of_classes), desc="Sweep (MPS)", leave=False)
        ]
    else:
        with ThreadPoolExecutor(max_workers=min(number_of_classes, 8)) as executor:
            results = list(
                tqdm(
                    executor.map(process_class, range(number_of_classes)),
                    total=number_of_classes,
                    desc="Sweep (CPU/CUDA)",
                    leave=False,
                )
            )

    for class_id, rates in results:
        occupancy_rates[:, class_id] = rates.to(device)

    # Детекция "прыжков" — моментов резкого изменения заполненности (более 1%).
    # Такие события обычно соответствуют важным топологическим или структурным
    # изменениям в анализируемых образах при изменении порога фильтрации.
    jump_events = []
    occupancy_change = abs(occupancy_rates[1:] - occupancy_rates[:-1])
    jump_mask = occupancy_change > CONFIG.jump_threshold
    jump_indices = where(jump_mask)

    for threshold_idx, class_id in zip(jump_indices[0].tolist(), jump_indices[1].tolist()):
        threshold_value = round(float(thresholds[threshold_idx + 1]), 4)
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
        f"  {num_thresholds} thresholds, {len(jump_events)} jumps ({time() - start_time:.1f}s)"
    )

    return sweep_results
