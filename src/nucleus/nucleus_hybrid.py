#!/usr/bin/env python3
"""Nucleus — Hybrid Mode System without external math libraries."""

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
import hashlib
import random
from dataclasses import dataclass
from enum import Enum
from typing import List


class Mode(Enum):
    """Режим работы системы."""

    DET = "deterministic"
    RND = "random"
    HYBRID = "hybrid"


@dataclass
class HybridProcessor:
    """Гибридный процессор DET/RND/HYBRID."""

    mode: Mode = Mode.HYBRID
    seed_value: int = 42

    def __init__(self, mode: Mode = Mode.HYBRID, seed: int = 42):
        self.mode = mode
        self.seed_value = seed
        self._rng = random.Random(seed)

    def set_mode(self, mode: Mode):
        """Переключить режим."""
        self.mode = mode

    def compute_correlation(self, a: str, b: str) -> float:
        """Вычислить корреляцию с учётом режима."""
        digest = hashlib.sha256((a + b).encode()).digest()
        base = (int.from_bytes(digest[:4], "big") % 1000) / 1000.0

        if self.mode == Mode.DET:
            return base
        if self.mode == Mode.RND:
            return max(0.0, min(1.0, base + self._rng.uniform(-0.1, 0.1)))
        if self._rng.random() > 0.5:
            return max(0.0, min(1.0, base + self._rng.uniform(-0.05, 0.05)))
        return base

    def find_path(self, from_node: str, to_node: str, max_hops: int = 3) -> List[str]:
        """Найти путь между узлами."""
        if self.mode == Mode.DET:
            return [from_node, to_node]
        if self.mode == Mode.RND:
            path = [from_node]
            for _ in range(max_hops):
                path.append(f"intermediate_{self._rng.randrange(0, 100)}")
            path.append(to_node)
            return path
        if self._rng.random() > 0.5:
            return [from_node, to_node]
        return [from_node, "bridge_a", "bridge_b", to_node]

    def evaluate(self, node: str) -> float:
        """Оценить узел."""
        digest = hashlib.sha256(node.encode()).digest()
        base_score = (int.from_bytes(digest[:4], "big") % 100) / 100.0
        if self.mode == Mode.DET:
            return base_score
        return max(0.0, min(1.0, base_score + self._rng.gauss(0.0, 0.1)))


def demo_modes():
    """Демонстрация режимов."""
    print("=" * 60)
    print("DET vs RND vs HYBRID")
    print("=" * 60)
    for mode in [Mode.DET, Mode.RND, Mode.HYBRID]:
        processor = HybridProcessor(mode)
        print(f"{mode.value}: {processor.compute_correlation('dog', 'cat'):.4f}")


def creative_example():
    """Короткий пример гибридного решения."""
    processor = HybridProcessor(Mode.HYBRID)
    print(processor.find_path("point", "sphere", max_hops=2))


if __name__ == "__main__":
    demo_modes()
    creative_example()
