#!/usr/bin/env python3
"""
Nucleus — Unified Duality System
================================

Ключевой инсайт из RealMath:
- Случайность — это НЕ случайность
- Это два конца ОДНОЙ струны!
- DET и RND — это не противоположности, а ОДНО!

Из RealMath:
- Ω (потенциал) ↔ Π (полнота) — два конца
- Re ↔ Im — две стороны одной системы
- Δ = ln|Re| - ln|Im| — отношение между ними

Случайность = переход между концами струны!
"""

from dataclasses import dataclass
from typing import Tuple

import numpy as np

from nucleus import safe_divide, is_potential


@dataclass
class DualState:
    """
    Состояние дуальной системы

    Omega (Ω) — потенциал, неопределённость, "все возможности"
    Pi (Π) — полнота, определённость, "реализация"

    Состояние = (omega, pi) где omega + pi = const
    """

    omega: float  # Неопределённость (потенциал)
    pi: float  # Определённость (реализация)

    @property
    def delta(self) -> float:
        """Relative balance - uses safe division."""
        if self.omega == 0 and self.pi == 0:
            return 0.0
        ratio = safe_divide(np.array([self.pi]), np.array([self.omega]))
        if is_potential(ratio):
            return float("inf") if self.pi > 0 else float("-inf")
        return np.log(abs(ratio[0]))

    @property
    def is_deterministic(self) -> bool:
        """Детерминированный режим — когда преобладает Π"""
        return self.pi > self.omega

    @property
    def is_exploratory(self) -> bool:
        """Исследовательский режим — когда преобладает Ω"""
        return self.omega > self.pi


class UnifiedSystem:
    """
    Унифицированная система — работает с двумя концами

    DET ↔ RND — это не разные вещи
    Это ОДНА система в разных состояниях!

    Ω (потенциал) ──────► Π (полнота)
         ↕                     ↕
       Re                     Im
         ↕                     ↕
      "все               "выбрано"
      возможности"

    Ключевое:
    - Случайность = движение по струне
    - DET = фиксация в точке Π
    - RND = движение в пространстве Ω
    - HYBRID = баланс между ними
    """

    def __init__(self, balance: float = 0.5):
        """
        balance: от 0 (полный хаос) до 1 (полная определённость)
        """
        self.state = DualState(omega=1.0 - balance, pi=balance)
        self.transition_history = []

    def transition(self, input_data: str, exploration_factor: float = 0.1) -> Tuple[str, DualState]:
        """
        Переход — вычисляет результат с учётом текущего состояния

        input_data: входные данные
        exploration_factor: насколько "исследовать" (движение по струне)

        Returns: (результат, новое состояние)
        """
        # Вычисляем "основной" результат (deterministic core)
        base_result = self._compute_base(input_data)

        # Применяем переход в зависимости от состояния
        if self.state.is_deterministic:
            # Режим Π — результат стабилен
            final_result = base_result
            new_balance = min(1.0, self.state.pi * 1.02)  # Укрепляем

        elif self.state.is_exploratory:
            # Режим Ω — добавляем "вибрацию" (случайность = движение по струне!)
            variation = self._compute_variation(input_data, self.state.omega, exploration_factor)
            final_result = base_result + variation
            new_balance = max(0.0, self.state.pi * 0.98)  # Ослабляем

        else:  # Баланс — HYBRID
            # Комбинация: стабильность + исследование
            variation = self._compute_variation(input_data, 0.5, exploration_factor * 0.3)
            final_result = base_result + variation
            # Состояние остаётся примерно тем же
            new_balance = self.state.pi

        # Обновляем состояние
        self.state = DualState(omega=1.0 - new_balance, pi=new_balance)

        # Записываем историю (сохраняем old_balance до обновления)
        old_pi = self.state.pi
        self.transition_history.append(
            {
                "input": input_data[:20],
                "balance_before": old_pi,
                "balance_after": new_balance,
                "delta": self.state.delta,
            }
        )

        return final_result, self.state

    def _compute_base(self, data: str) -> float:
        """Базовое (детерминированное) вычисление"""
        # Хеш — детерминированное отображение
        h = sum(ord(c) * (i + 1) for i, c in enumerate(data))
        return (h % 1000) / 1000.0

    def _compute_variation(self, data: str, omega: float, factor: float) -> float:
        """
        Вычислить вариацию — движение по струне

        Это НЕ случайность!
        Это проявление неопределённости Ω — "все возможности"
        """
        # Вариация зависит от omega (неопределённости)
        # и от входных данных

        h = sum(ord(c) for c in data)

        # Синусоида — периодическое движение
        # Это и есть "квантовая" природа — колебание между концами!
        phase = h / 100.0
        variation = np.sin(phase) * omega * factor

        return variation

    def measure(self) -> dict:
        """
        Измерить текущее состояние системы

        Возвращает полную картину: где мы на струне?
        """
        return {
            "omega": self.state.omega,  # Неопределённость
            "pi": self.state.pi,  # Определённость
            "delta": self.state.delta,  # Относительный баланс
            "mode": (
                "DET"
                if self.state.is_deterministic
                else ("RND" if self.state.is_exploratory else "HYBRID")
            ),
            "history_length": len(self.transition_history),
        }
