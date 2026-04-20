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

from numpy import (
    abs,
    log,
    ndarray,
)
from scipy import ndimage


def fractal_dimension_from_betti(
    betti_values: ndarray,
    thresholds: ndarray,
    reference_threshold: float = 0.0,
) -> float:
    """
    Вычисление фрактальной размерности из скейлинга Бетти.

    D_f = lim (log β₀(t) / log β₀(t/2))

    Согласно Essentials [22_Геометрия.md]:
    Размерность — это не константа среды, а показатель того,
    как объект реагирует на Акт (:Ω).

    Args:
        betti_values: Массив значений Бетти β₀(t) для каждого порога
        thresholds: Массив порогов
        reference_threshold: Референсный порог для нормализации

    Returns:
        Фрактальная размерность D_f
    """
    # Find pairs (t, t/2) in the threshold array
    ref_idx = abs(thresholds - reference_threshold).argmin()
    ref_betti = betti_values[ref_idx]

    if ref_betti <= 0:
        return 0.0

    # Compute scaling ratio
    half_threshold = reference_threshold / 2.0
    half_idx = abs(thresholds - half_threshold).argmin()
    half_betti = betti_values[half_idx]

    if half_betti <= 0:
        return 0.0

    # D_f = log(β₀(t)) / log(β₀(t/2))
    d_f = log(ref_betti) / log(half_betti) if half_betti > 0 else 0.0

    return float(d_f)


def fractal_dimension_from_multiple_scales(
    betti_values: ndarray,
    thresholds: ndarray,
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
        betti_values: Массив значений Бетти β₀(t)
        thresholds: Массив порогов
        n_scales: Количество масштабов для анализа

    Returns:
        Список (threshold, D_f) для каждого масштаба
    """
    results = []

    # Sample at regular intervals
    step = max(1, len(thresholds) // n_scales)

    for i in range(step, len(thresholds) - step, step):
        t = thresholds[i]
        beta = betti_values[i]

        if beta <= 0:
            continue

        # Use local scaling
        delta = abs(thresholds[i + step] - thresholds[i - step])
        if delta == 0:
            continue

        beta_plus = betti_values[i + step]
        beta_minus = betti_values[i - step]

        if beta_plus > 0 and beta_minus > 0:
            d_f = (
                log(beta_plus / beta_minus) / log((t + delta) / (t - delta))
                if (t - delta) != 0
                else 0.0
            )
            results.append((t, float(d_f)))

    return results


def compute_betti_scaling_exponent(
    betti_values: ndarray,
    thresholds: ndarray,
) -> float:
    """
    Вычисление показателя скейлинга Бетти.

    β₀(t) ~ t^α  ⟹  log(β₀) ~ α · log(t)

    α — показатель скейлинга, связанный с фрактальной размерностью:
    D_f = d - α где d — топологическое пространство (2 для изображений)

    Согласно Essentials [22_Геометрия.md]:
    При Ветвлении объём в k-мерном пространстве масштабируется как Dᵏ(Id).
    """
    # Filter out zero values
    mask = betti_values > 0
    if mask.sum() < 2:
        return 0.0

    log_beta = log(betti_values[mask])
    log_t = log(abs(thresholds[mask]) + 1e-10)

    # Linear fit: log_beta = α · log_t + β
    n = len(log_beta)
    sum_x = log_t.sum()
    sum_y = log_beta.sum()
    sum_xy = (log_t * log_beta).sum()
    sum_x2 = (log_t**2).sum()

    denom = n * sum_x2 - sum_x**2
    if abs(denom) < 1e-10:
        return 0.0

    alpha = (n * sum_xy - sum_x * sum_y) / denom

    return float(alpha)


def fractal_volume_scaling(
    binary_masks: list,
    thresholds: ndarray,
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
        thresholds: Массив порогов

    Returns:
        Список (threshold, volume, log_volume)
    """
    results = []

    for i, mask in enumerate(binary_masks):
        volume = mask.sum()
        threshold = thresholds[i] if i < len(thresholds) else 0.0

        results.append(
            {
                "threshold": threshold,
                "volume": volume,
                "log_volume": log(volume) if volume > 0 else float("-inf"),
                "fraction": volume / mask.size if mask.size > 0 else 0.0,
            }
        )

    return results


def fractal_similarity_score(mask_a: ndarray, mask_b: ndarray) -> float:
    """
    Фрактальное сходство двух бинарных масок.

    Согласно Essentials [23_Соленоид.md]:
    Две точки на соленоиде близки, если их двоичные истории
    совпадают на многих первых шагах.

    Мы используем это для измерения сходства структур:
    - Если маски имеют схожую фрактальную размерность → схожая структура
    - Если маски имеют схожее Betti scaling → схошая топология

    Args:
        mask_a: Первая бинарная маска
        mask_b: Вторая бинарная маска

    Returns:
        Сходство: 0 (разные) до 1 (идентичные)
    """
    # Jaccard similarity
    intersection = (mask_a & mask_b).sum()
    union = (mask_a | mask_b).sum()

    if union == 0:
        return 1.0 if intersection == 0 else 0.0

    jaccard = intersection / union

    # Also compare Betti numbers

    _, b0_a = ndimage.label(mask_a)
    _, b0_b = ndimage.label(mask_b)

    betti_diff = abs(b0_a - b0_b) / max(b0_a, b0_b, 1)
    betti_similarity = 1.0 - betti_diff

    # Combined score
    return 0.7 * jaccard + 0.3 * betti_similarity
