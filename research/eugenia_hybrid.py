#!/usr/bin/env python3
"""
EUGENIA — Hybrid Mode System
============================

Два режима работы:
1. DET deterministic — точные вычисления, факты, логика
2. RND random — творческие вариации,探索, исследования

Комбинация = решает сложные задачи!
"""

import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Callable
import hashlib


class Mode(Enum):
    """Режим работы системы"""

    DET = "deterministic"  # Точный, воспроизводимый
    RND = "random"  # Вариативный, творческий
    HYBRID = "hybrid"  # Комбинация обоих


@dataclass
class HybridProcessor:
    """
    Гибридный процессор — работает в ДВУХ режимах

    DET (детерминированный):
    - Точные вычисления всегда дают одинаковый результат
    - Воспроизводимость
    - Факты, правила, логика

    RND ( случайный):
    - Вариативные вычисления для одного входа
    - Творчество, исследования
    - Принцип: "а что если попробовать иначе?"

    HYBRID (гибридный):
    - Случайный вызов методов когда нужно исследование
    - Детерминированный для фактов
    - Комбинация = интеллект!
    """

    mode: Mode = Mode.HYBRID
    seed_value: int = 42  # -seed для детерминированного режима

    def __init__(self, mode: Mode = Mode.HYBRID, seed: int = 42):
        self.mode = mode
        self.seed_value = seed
        self._rng = np.random.default_rng(seed)

    def set_mode(self, mode: Mode):
        """切换模式"""
        self.mode = mode

    def compute_correlation(self, a: str, b: str) -> float:
        """
        Вычислить корреляцию — с учетом режима

        DET: точное значение
        RND: значение + случайное отклонение (творчество!)
        HYBRID: 50/50
        """
        # Базовое вычисление (детерминированное)
        h = hashlib.sha256((a + b).encode()).digest()
        base = (int.from_bytes(h[:4], "big") % 1000) / 1000.0

        if self.mode == Mode.DET:
            # Точный детерминированный результат
            return base

        elif self.mode == Mode.RND:
            # Добавляем случайность — для творчества!
            random_offset = self._rng.uniform(-0.1, 0.1)
            return max(0.0, min(1.0, base + random_offset))

        else:  # HYBRID
            if self._rng.random() > 0.5:
                random_offset = self._rng.uniform(-0.05, 0.05)
                return max(0.0, min(1.0, base + random_offset))
            return base

    def find_path(self, from_node: str, to_node: str, max_hops: int = 3) -> List[str]:
        """
        Найти путь между узлами

        DET: один верный путь
        RND: разные пути каждый раз (творитчество!)
        HYBRID: случайно выбирает подход
        """
        if self.mode == Mode.DET:
            # Детерминированно: кратчайший путь
            return [from_node, to_node]

        elif self.mode == Mode.RND:
            # Случайный: разные маршруты исследования
            path = [from_node]
            for _ in range(max_hops):
                path.append(f"intermediate_{self._rng.integers(0, 100)}")
            path.append(to_node)
            return path

        else:  # HYBRID
            # Комбинация: иногда короче, иногда длиннее
            if self._rng.random() > 0.5:
                return [from_node, to_node]
            return [from_node, "bridge_a", "bridge_b", to_node]

    def evaluate(self, node: str) -> float:
        """
        Оценить узел

        DET: точная оценка
        RND: оценка + шум
        """
        h = hashlib.sha256(node.encode()).digest()
        base_score = (int.from_bytes(h[:4], "big") % 100) / 100.0

        if self.mode == Mode.DET:
            return base_score

        noise = self._rng.normal(0, 0.1)
        return max(0.0, min(1.0, base_score + noise))


# ============================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================


def demo_modes():
    """Демонстрация режимов"""
    print("=" * 60)
    print("DET vs RND vs HYBRID")
    print("=" * 60)

    # DET mode — всегда одинаково
    det = HybridProcessor(Mode.DET)
    print("\n[DET] Точный режим:")
    for i in range(3):
        result = det.compute_correlation("dog", "cat")
        print(f"  dog↔cat #{i + 1}: {result:.4f} (всегда одинаково!)")

    # RND mode — каждый раз разное
    rnd = HybridProcessor(Mode.RND)
    print("\n[RND] Случайный режим:")
    for i in range(3):
        result = rnd.compute_correlation("dog", "cat")
        print(f"  dog↔cat #{i + 1}: {result:.4f} (всегда разное!)")

    # HYBRID — комбинация
    hybrid = HybridProcessor(Mode.HYBRID)
    print("\n[HYBRID] Гибридный режим:")
    for i in range(3):
        result = hybrid.compute_correlation("dog", "cat")
        print(f"  dog↔cat #{i + 1}: {result:.4f}")

    print("\n" + "=" * 60)
    print("ПОИСК ПУТИ:")
    print("=" * 60)

    # Разные пути в разных режимах
    for mode in [Mode.DET, Mode.RND, Mode.HYBRID]:
        proc = HybridProcessor(mode)
        path = proc.find_path("point", "sphere", max_hops=2)
        print(f"  {mode.value}: {path}")


def creative_example():
    """
    Пример: решение сложной задачи

    Когда нам нужно решить НОВУЮ задачу:
    1. DET → используем известные факты
    2. RND → исследуем новые подходы
    3. HYBRID → комбинируем!
    """
    print("\n" + "=" * 60)
    print("ПРАКТИЧЕСКИЙ ПРИМЕР: Решение сложной задачи")
    print("=" * 60)

    """
    Задача: "Как добраться из точки A в точку B?"
    
    DET (детерминированный):
    -已知的最短路径 A → B
    - Используем GPS, карты
    - Быстро, надежно
    
    RND (случайный):
    - "А что если пойти через лес?"
    - "А е��ли поплыть?"
    - "А если полететь?"
    - Находим НЕОВЫДНЫЕ решения
    
    HYBRID (гибридный):
    - Сначала RND для исследования вариантов
    - Потом DET для выбора лучшего
    - Комбинация = интеллект!
    """

    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                    ДЛЯ СЛОЖНЫХ ЗАДАЧ                         ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║                                                          ║
    ║  1. RND (исследование) — найти все варианты               ║
    ║     "А что если попробовать..."                          ║
    ║                                                          ║
    ║  2. HYBRID (выбор) — оценить и отобрать                   ║
    ║     "Это работает лучше!"                                 ║
    ║                                                          ║
    ║  3. DET (фиксация) — запомнить лучший                    ║
    ║     "Запоминаем для следующего раза"                     ║
    ║                                                          ║
    ║  РЕЗУЛЬТАТ:                                              ║
    ║  - Нашли НОВЫЕ решения (RND)                              ║
    ║  - Выбрали ЛУЧШИЙ (HYBRID)                                ║
    ║  - Запомнили НАВЕКИГДА (DET)                             ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    demo_modes()
    creative_example()

    print("\n" + "=" * 60)
    print("КЛЮЧЕВОЙ ВЫВОД:")
    print("=" * 60)
    print("""
    DET + RND = ТВОРЕНИЕ!
    
    DET: для точности и воспроизводимости
    RND: для творчества и исследований  
    HYBRID: для решения сложных задач
    
    Это как:
    - Детерминированные законы физики + квантовая случайность
    - Логика + интуиция
    - Факты + творчество
    
    ВМЕСТЕ = ИНТЕЛЛЕКТ!
    """)
