"""
Fractal dimension from Betti scaling — фрактальная размерность через Бетти.

Согласно Essentials [22_Геометрия.md]:
- При Ветвлении (:Ω) объём в k-мерном пространстве масштабируется как Dᵏ(Id) = 2ᵏ
- Размерность пространства проявляется в степени масштабирования
- D_f = lim (log β₀(t) / log β₀(t/2)) — фрактальная размерность из скейлинга Бетти

Применение в Eugenia:
- Измеряем как β₀ и β₁ масштабируются с порогом
- Фрактальная размерность показывает "сложность" топологии
- D_f ≈ 1 для простых кривых, D_f ≈ 2 для заполненных областей
"""

import math
from typing import Sequence, Union

Number = Union[int, float]


def _find_closest_index(arr: list[float], target: float) -> int:
    """Find index of element closest to target in a sorted list."""
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def _label_binary_mask_2d(mask: list[list[int]]) -> list[list[int]]:
    """
    Pure Python connected-component labeling for 2D binary mask.
    Uses Union-Find (disjoint set) algorithm.

    Args:
        mask: 2D list of 0/1 values.

    Returns:
        Labeled mask with component IDs starting from 1.
    """
    if not mask or not mask[0]:
        return []
    rows = len(mask)
    cols = len(mask[0])
    labeled = [[0] * cols for _ in range(rows)]
    parent = {}
    comp_id = 0

    def find(x):
        while parent.get(x, x) != x:
            parent[x] = parent.get(parent[x], parent.get(parent[parent[x]], x))
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for r in range(rows):
        for c in range(cols):
            if mask[r][c] == 0:
                continue
            neighbors = []
            if r > 0 and labeled[r - 1][c] > 0:
                neighbors.append(labeled[r - 1][c])
            if c > 0 and labeled[r][c - 1] > 0:
                neighbors.append(labeled[r][c - 1])
            if neighbors:
                root = min(neighbors)
                labeled[r][c] = root
                for n in neighbors:
                    union(n, root)
            else:
                comp_id += 1
                labeled[r][c] = comp_id
                parent[comp_id] = comp_id

    # Path compression pass
    for r in range(rows):
        for c in range(cols):
            if labeled[r][c] > 0:
                labeled[r][c] = find(labeled[r][c])

    return labeled


def fractal_dimension_from_betti(
    betti_values: Sequence[float],
    thresholds: Sequence[float],
    reference_threshold: float = 0.0,
) -> float:
    """
    Вычисление фрактальной размерности из скейлинга Бетти.

    D_f = lim (log β₀(t) / log β₀(t/2))

    Согласно Essentials [22_Геометрия.md]:
    Размерность — это не константа среды, а показатель того,
    как объект реагирует на Акт (:Ω).

    Args:
        betti_values: Список значений Бетти β₀(t) для каждого порога
        thresholds: Список порогов
        reference_threshold: Референсный порог для нормализации

    Returns:
        Фрактальная размерность D_f
    """
    thresh_list: list[float] = list(thresholds)
    betti_list: list[float] = list(betti_values)

    ref_idx = min(range(len(thresh_list)), key=lambda i: abs(thresh_list[i] - reference_threshold))  # type: ignore[arg-type]
    ref_betti = betti_list[ref_idx]

    if ref_betti <= 0:
        return 0.0

    half_threshold = reference_threshold / 2.0
    half_idx = min(range(len(thresh_list)), key=lambda i: abs(thresh_list[i] - half_threshold))  # type: ignore[arg-type]
    half_betti = betti_list[half_idx]

    if half_betti <= 0:
        return 0.0

    d_f = math.log(ref_betti) / math.log(half_betti) if half_betti > 0 else 0.0

    return float(d_f)


def fractal_dimension_from_multiple_scales(
    betti_values: Sequence[float],
    thresholds: Sequence[float],
    n_scales: int = 5,
) -> list:
    """
    Вычисление фрактальной размерности на нескольких масштабах.

    Вместо одного значения D_f, вычисляем локальную D_f(t)
    для каждого порога, используя соседние пороги.

    D_f(t) = log(β₀(t + Δ) / β₀(t - Δ)) / log((t + Δ) / (t - Δ))

    Это даёт "фрактальный профиль" — как размерность меняется
    в зависимости от масштаба наблюдения.

    Args:
        betti_values: Список значений Бетти β₀(t)
        thresholds: Список порогов
        n_scales: Количество масштабов для анализа

    Returns:
        Список (threshold, D_f) для каждого масштаба
    """
    results = []
    thresh_list = list(thresholds)
    betti_list = list(betti_values)

    step = max(1, len(thresh_list) // n_scales)

    for i in range(step, len(thresh_list) - step, step):
        t = thresh_list[i]
        beta = betti_list[i]

        if beta <= 0:
            continue

        delta = abs(thresh_list[i + step] - thresh_list[i - step])
        if delta == 0:
            continue

        beta_plus = betti_list[i + step]
        beta_minus = betti_list[i - step]

        if beta_plus > 0 and beta_minus > 0:
            d_f = (
                math.log(beta_plus / beta_minus) / math.log((t + delta) / (t - delta))
                if (t - delta) != 0
                else 0.0
            )
            results.append((t, float(d_f)))

    return results


def compute_betti_scaling_exponent(
    betti_values: Sequence[float],
    thresholds: Sequence[float],
) -> float:
    """
    Вычисление показателя скейлинга Бетти.

    β₀(t) ~ t^α  ⟹  log(β₀) ~ α · log(t)

    α — показатель скейлинга, связанный с фрактальной размерностью:
    D_f = d - α где d — топологическое пространство (2 для изображений)

    Согласно Essentials [22_Геометрия.md]:
    При Ветвлении объём в k-мерном пространстве масштабируется как Dᵏ(Id).
    """
    betti_list = list(betti_values)
    thresh_list = list(thresholds)

    log_beta = []
    log_t = []
    for beta, t in zip(betti_list, thresh_list):
        if beta > 0:
            log_beta.append(math.log(beta))
            log_t.append(math.log(abs(t) + 1e-10))

    n = len(log_beta)
    if n < 2:
        return 0.0

    sum_x = sum(log_t)
    sum_y = sum(log_beta)
    sum_xy = sum(x * y for x, y in zip(log_t, log_beta))
    sum_x2 = sum(x**2 for x in log_t)

    denom = n * sum_x2 - sum_x**2
    if abs(denom) < 1e-10:
        return 0.0

    alpha = (n * sum_xy - sum_x * sum_y) / denom
    return float(alpha)


def fractal_volume_scaling(
    binary_masks: list,
    thresholds: Sequence[float],
) -> list:
    """
    Вычисление фрактального масштабирования объёма.

    V(t) = count(δ > t) — объём переднего плана при пороге t

    При Ветвлении: V(t:Ω) = Dᵏ(Id) · V(t) где k — размерность.

    Для 2D изображений:
    - Если V(t) ~ t^α, то α ≈ 2 для заполненных областей
    - Если V(t) ~ t^α, то α ≈ 1 для кривых/линий
    - α < 1 указывает на фрактальную структуру

    Args:
        binary_masks: Список бинарных масок для разных порогов
        thresholds: Список порогов

    Returns:
        Список (threshold, volume, log_volume)
    """
    results = []
    thresh_list = list(thresholds)

    for i, mask in enumerate(binary_masks):
        volume = sum(1 for pixel in mask if pixel)
        threshold = thresh_list[i] if i < len(thresh_list) else 0.0

        results.append(
            {
                "threshold": threshold,
                "volume": volume,
                "log_volume": math.log(volume) if volume > 0 else float("-inf"),
                "fraction": volume / len(mask) if mask else 0.0,
            }
        )

    return results


def fractal_similarity_score(mask_a, mask_b) -> float:
    """
    Фрактальное сходство двух бинарных масок.

    Согласно Essentials [23_Соленоид.md]:
    Две точки на соленоиде близки, если их двоичные истории
    совпадают на многих первых шагах.

    Мы используем это для измерения сходства структур:
    - Если маски имеют схожую фрактальную размерность → схожая структура
    - Если маски имеют схожее Betti scaling → схожая топология

    Args:
        mask_a: Первая бинарная маска (list or list of lists)
        mask_b: Вторая бинарная маска (list or list of lists)

    Returns:
        Сходство: 0 (разные) до 1 (идентичные)
    """
    # Flatten masks if 2D
    if mask_a and isinstance(mask_a[0], list):
        flat_a = [pixel for row in mask_a for pixel in row]
    else:
        flat_a = list(mask_a)
    if mask_b and isinstance(mask_b[0], list):
        flat_b = [pixel for row in mask_b for pixel in row]
    else:
        flat_b = list(mask_b)

    set_a = set(flat_a)
    set_b = set(flat_b)

    intersection = len(set_a & set_b)
    union = len(set_a | set_b)

    if union == 0:
        return 1.0 if intersection == 0 else 0.0

    jaccard = intersection / union

    # Compute Betti-0 (number of connected components) via simple labeling
    def count_components(mask):
        if not mask or not mask[0]:
            return 0
        labeled = _label_binary_mask_2d(mask)
        rows = len(labeled)
        cols = len(labeled[0])
        components = set()
        for r in range(rows):
            for c in range(cols):
                if labeled[r][c] > 0:
                    components.add(labeled[r][c])
        return len(components)

    b0_a = count_components(mask_a) if mask_a and isinstance(mask_a[0], list) else 0
    b0_b = count_components(mask_b) if mask_b and isinstance(mask_b[0], list) else 0

    betti_diff = abs(b0_a - b0_b) / max(b0_a, b0_b, 1)
    betti_similarity = 1.0 - betti_diff

    return 0.7 * jaccard + 0.3 * betti_similarity


def solenoid_similarity(traj_a: list, traj_b: list) -> float:
    """
    Сходство на основе соленоида per Essentials [23_Соленоид.md].

    Две точки близки, если их двоичные истории
    совпадают на многих первых шагах.

    Близость = 2^(-k) где k — первый различающийся бит.

    Args:
        traj_a: Первая траектория (список битов).
        traj_b: Вторая траектория (список битов).

    Returns:
        Близость: 0 (разные) до 1 (идентичные).
    """
    k = 0
    for a, b in zip(traj_a, traj_b):
        if a != b:
            break
        k += 1
    return 2.0 ** (-k)


def solenoid_distance_from_masks(mask_a, mask_b, depth: int = 20) -> float:
    """
    Расстояние между масками через соленоид.

    Преобразует маски в двоичные траектории и вычисляет
    соленоидное расстояние per Essentials [23_Соленоид.md].

    Args:
        mask_a: Первая бинарная маска.
        mask_b: Вторая бинарная маска.
        depth: Глубина двоичного кодирования.

    Returns:
        Близость: 2^(-k) где k — первый различающийся бит.
    """
    if isinstance(mask_a[0], list) if mask_a else False:
        seq_a = [1 if pixel else 0 for row in mask_a for pixel in row]
    else:
        seq_a = [1 if pixel else 0 for pixel in mask_a]
    if isinstance(mask_b[0], list) if mask_b else False:
        seq_b = [1 if pixel else 0 for row in mask_b for pixel in row]
    else:
        seq_b = [1 if pixel else 0 for pixel in mask_b]

    max_len = max(len(seq_a), len(seq_b), depth)
    seq_a = seq_a + [0] * (max_len - len(seq_a))
    seq_b = seq_b + [0] * (max_len - len(seq_b))

    return solenoid_similarity(seq_a[:depth], seq_b[:depth])
