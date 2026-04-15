#!/usr/bin/env python3
"""
ЕВГЕНИЯ — Параметры визуализации.
Все числовые константы собраны в одном месте.
Структура кода отражает геометрию Соленоида (фазовое пространство системы).
"""

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class SolenoidVizParams:
    """
    Параметры визуализации Δ-поля.
    Структура привязана к геометрии Соленоида (фазовое пространство).
    """

    # ─── 1. ГЕОМЕТРИЯ СОЛЕНОИДА (Фазовое пространство) ─────────────────────
    # Соленоид S — пространство всех согласованных последовательностей масштабирований.
    # Каждая точка соленоида — целая история (траектория), а не одно число.
    # Двоичная координата ξ кодирует выбор ветви на каждом шаге.

    # Фокус на конкретном пороге Δ.
    # Δ = -5.5452 — нижний предел контраста (z → 0).
    # В логарифмической координате ℓ: Re(ℓ) → -∞.
    # Это "дно" соленоида, где вся информация сжата в точку (z=0).
    delta_focus: float = -5.5452

    # ─── 2. СДВИГ БЕРНУЛЛИ (Динамика системы) ──────────────────────────────
    # Действие деления на 0 в координатах (φ, ξ): φ не меняется, ξ ↦ 2ξ mod 1.
    # Это сдвиг влево по двоичной записи: 0.ε₀ε₁ε₂… ↦ 0.ε₁ε₂ε₃…
    # Визуально это проявляется как "скачки" при изменении порога Δ.

    # Диапазон сканирования порога Δ (ось сдвига).
    # От -5.546 (z=0) до +5.546 (z=∞, граница B).
    # За пределами — пустота (система не определена).
    sweep_min: float = -5.546
    sweep_max: float = 5.546

    # Шаг сканирования (разрешение по ξ).
    # 0.0001 — позволяет различить тонкие сдвиги Бернулли.
    sweep_step: float = 0.0001

    # Порог детекции скачка (%).
    # Аналог чувствительности к сдвигу Бернулли.
    # 1.0 — ловит значимые фазовые переходы, игнорирует шум канторова множества.
    jump_threshold: float = 1.0

    # ─── 3. МАСШТАБЫ ИНФОРМАЦИОННОГО ПОЛЯ (I, Q, ρ, M) ─────────────────────
    # Четыре термина для разных уровней наблюдения за соленоидом.

    # I — Информационная ёмкость (Глобальный масштаб).
    # Сколько всего "вмещает" система на данном уровне ξ.
    hist_bins_default: int = 100
    hist_bins_min: int = 20
    hist_bins_max: int = 500

    # Q — Структурная сложность (Локальный масштаб).
    # Мера плотности связей внутри слоя соленоида.
    heatmap_n_points: int = 100
    heatmap_max_samples: int = 5

    # ρ — Плотность состояния (Точечный масштаб).
    # Напряжение в конкретном узле бифуркации.
    betti_max_samples: int = 50
    betti_n_thr_default: int = 96
    betti_n_thr_min: int = 20
    betti_n_thr_max: int = 200

    # M — Мера поля (Интегральный масштаб).
    # Общий баланс потоков Re и Im.
    betti_pad: int = 1
    betti_holes_min: int = 0

    # ─── 4. КОМПАКТИФИКАЦИЯ (Граница B) ────────────────────────────────────
    # Граница соленоида B ≃ ℝ/2πℤ — окружность, параметризованная аргументом.
    # Точки на границе — это "проценты" (p% от ∞).
    # Визуализация: тепловые карты и гистограммы.

    # Число классов (10 цифр) — дискретные уровни на границе B.
    # Аналогия: 10 дискретных энергетических уровней (n=1..10).
    hist_n_classes: int = 10
    hist_rows: int = 2
    hist_cols: int = 5
    hist_title_fontsize: int = 9

    # Сетка для гистограмм и анимаций
    hist_grid_cols: int = 5
    anim_grid_cols: int = 5
    hist_row_height: float = 1.5
    individual_fig_w_factor: float = 2.5
    individual_fig_h_factor: float = 1.8

    # Позиция референсной линии (Δ = 0).
    hist_ref_line_x: float = 0.0

    # ─── 5. ВИЗУАЛЬНЫЕ МАППЕРЫ (Проекция на экран) ─────────────────────────
    # Цвета и стили.
    hist_color: str = "steelblue"
    hist_alpha: float = 0.7
    grid_alpha: float = 0.3
    marker_size: int = 2
    cmap_heatmap: str = "hot"
    cmap_3d: str = "coolwarm"
    cmap_3d_alpha: float = 0.8
    cmap_binary: str = "binary"
    cmap_gray: str = "gray"
    ref_line_color: str = "r"
    ref_line_ls: str = "--"
    ref_line_lw: float = 0.5

    # Размеры фигур.
    fig_wide_w: int = 16
    fig_wide_h: int = 6
    fig_heatmap_w: int = 12
    fig_heatmap_h: int = 5
    fig_betti_w: int = 14
    fig_betti_h: int = 4
    fig_3d_w: int = 8
    fig_3d_h: int = 6
    fig_tab1_cols: int = 9
    fig_tab1_h: int = 3

    # Алиасы
    heatmap_vmin: float = 0.0
    heatmap_vmax: float = 100.0
    hist_bins: int = 100
    anim_n_frames: int = 60
    tsne_max_samples: int = 2000
    tsne_per_class: int = 200
    tsne_perplexity: int = 30
    surface_n_samples: int = 5
    original_vs_binary: List[float] = field(
        default_factory=lambda: [-5, -3, -1, 0, 1, 2, 3, 4]
    )
    betti_n_samples: int = 100
    betti_thr_min: float = -5.0
    betti_thr_max: float = 4.5
    betti_n_thr: int = 96
    euler_n_samples: int = 500

    # DPI
    dpi_default: int = 120
    dpi_high: int = 150
    dpi_low: int = 80
    dpi_individual: int = 100

    # Размеры фигур (переопределяемые)
    fig_scatter_w: int = 10
    fig_scatter_h: int = 7
    fig_jumps_w: int = 14
    fig_jumps_h: int = 4
    fig_cdf_w: int = 10
    fig_cdf_h: int = 6
    fig_betti_w: int = 12
    fig_betti_h: int = 7
    fig_euler_w: int = 15
    fig_euler_h: int = 4
    fig_tsne_w: int = 10
    fig_tsne_h: int = 8
    fig_3d_multi_w: int = 16
    fig_3d_multi_h: int = 4
    fig_3d_grid_w: int = 20
    fig_3d_grid_h: int = 8
    fig_heatmap_wide_w: int = 16
    fig_heatmap_wide_h: int = 8
    fig_animation_w: int = 15
    fig_animation_h: int = 7
    fig_orig_binary_w_factor: int = 2
    fig_orig_binary_h: int = 12
    fig_individual_w: int = 8
    fig_individual_h: int = 4
    fig_hist_wide_w: int = 16
    fig_hist_wide_h: int = 6
    fig_entropy_w: int = 16
    fig_entropy_h: int = 10
    fig_phase_w: int = 16
    fig_phase_h: int = 10


# Экземпляр по умолчанию
VIZ = SolenoidVizParams()
