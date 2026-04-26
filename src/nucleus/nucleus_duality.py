#!/usr/bin/env python3
"""
Nucleus — Unified Duality System
================================

Ключевой инсайт:
- Случайность — это НЕ случайность
- Это два конца ОДНОЙ струны
- DET и RND — это не противоположности, а состояния одной системы
"""

#  Copyright (c) 2026.
#  ╔═══════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═══════════════════════════════════╝
import math
from dataclasses import dataclass
from typing import Tuple

from core.linear_algebra import EPSILON


@dataclass
class DualState:
    """Состояние дуальной системы Ω ↔ Π."""

    omega: float
    pi: float

    @property
    def delta(self) -> float:
        """Relative balance Δ = ln(|Π / Ω|) with potential handling."""
        if abs(self.omega) < EPSILON and abs(self.pi) < EPSILON:
            return 0.0
        if abs(self.omega) < EPSILON:
            return float("inf") if self.pi >= 0.0 else float("-inf")
        ratio = self.pi / self.omega
        if abs(ratio) < EPSILON:
            return float("-inf")
        return math.log(abs(ratio))

    @property
    def is_deterministic(self) -> bool:
        """Детерминированный режим — когда преобладает Π."""
        return self.pi > self.omega

    @property
    def is_exploratory(self) -> bool:
        """Исследовательский режим — когда преобладает Ω."""
        return self.omega > self.pi


class UnifiedSystem:
    """Унифицированная система двух концов Ω ↔ Π."""

    def __init__(self, balance: float = 0.5):
        self.state = DualState(omega=1.0 - balance, pi=balance)
        self.transition_history = []

    def transition(self, input_data: str, exploration_factor: float = 0.1) -> Tuple[str, DualState]:
        """Переход с учётом текущего состояния системы."""
        base_result = self._compute_base(input_data)

        if self.state.is_deterministic:
            final_result = base_result
            new_balance = min(1.0, self.state.pi * 1.02)
        elif self.state.is_exploratory:
            variation = self._compute_variation(input_data, self.state.omega, exploration_factor)
            final_result = base_result + variation
            new_balance = max(0.0, self.state.pi * 0.98)
        else:
            variation = self._compute_variation(input_data, 0.5, exploration_factor * 0.3)
            final_result = base_result + variation
            new_balance = self.state.pi

        balance_before = self.state.pi
        self.state = DualState(omega=1.0 - new_balance, pi=new_balance)
        self.transition_history.append(
            {
                "input": input_data[:20],
                "balance_before": balance_before,
                "balance_after": new_balance,
                "delta": self.state.delta,
            }
        )

        return final_result, self.state

    def _compute_base(self, data: str) -> float:
        """Базовое детерминированное отображение."""
        value = sum(ord(char) * (index + 1) for index, char in enumerate(data))
        return (value % 1000) / 1000.0

    def _compute_variation(self, data: str, omega: float, factor: float) -> float:
        """Вариация как периодическое движение по струне Ω ↔ Π."""
        phase = sum(ord(char) for char in data) / 100.0
        return math.sin(phase) * omega * factor

    def measure(self) -> dict:
        """Измерить текущее состояние системы."""
        return {
            "omega": self.state.omega,
            "pi": self.state.pi,
            "delta": self.state.delta,
            "mode": (
                "DET"
                if self.state.is_deterministic
                else ("RND" if self.state.is_exploratory else "HYBRID")
            ),
            "history_length": len(self.transition_history),
        }
