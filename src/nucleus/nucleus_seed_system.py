#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nucleus — Seed-Based Knowledge System on Eugenia core math."""

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
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from core.linear_algebra import CoreVector, cosine_similarity, normalize


@dataclass
class Seed:
    """Базовое семя — начало всех паттернов."""

    seed_id: str
    representation: CoreVector
    description: str
    basic: bool = True


BASE_SEEDS = {
    "point": CoreVector([1.0, 0.0, 0.0, 0.0]),
    "line": CoreVector([0.0, 1.0, 0.0, 0.0]),
    "angle": CoreVector([0.0, 0.0, 1.0, 0.0]),
    "plane": CoreVector([0.0, 0.0, 0.0, 1.0]),
    "circle": CoreVector([1.0, 1.0, 0.0, 0.0]),
    "square": CoreVector([1.0, 0.5, 0.5, 0.0]),
    "triangle": CoreVector([0.0, 1.0, 1.0, 0.0]),
    "sphere": CoreVector([1.0, 1.0, 1.0, 0.0]),
    "chain": CoreVector([0.0, 0.5, 0.5, 1.0]),
    "tree": CoreVector([0.0, 0.0, 0.0, 0.5]),
    "ring": CoreVector([1.0, 1.0, 0.0, 0.5]),
    "net": CoreVector([0.0, 0.0, 1.0, 1.0]),
}


class CorrelationEngine:
    """Детерминированный движок корреляций между паттернами."""

    def __init__(self, base_dim: int = 4):
        self.base_dim = base_dim
        self.seeds: Dict[str, Seed] = {}
        for name, vector in BASE_SEEDS.items():
            self.seeds[name] = Seed(
                seed_id=name,
                representation=vector,
                description=self._describe_seed(name),
                basic=True,
            )

    def _describe_seed(self, name: str) -> str:
        descriptions = {
            "point": "Нульмерный объект, начало координат",
            "line": "Одномерный объект, связь двух точек",
            "angle": "Два луча из одной точки",
            "plane": "Двумерная поверхность",
            "circle": "Замкнутая кривая, центр = все точки равноудалены",
            "square": "4 стороны, 4 угла 90°",
            "triangle": "3 стороны, 3 угла",
            "sphere": "Трехмерная сфера",
            "chain": "Последовательность связанных элементов",
            "tree": "Иерархия с ветвлением",
            "ring": "Цикл без начала и конца",
            "net": "Переплетение многих линий",
        }
        return descriptions.get(name, name)

    def get_correlation(self, a: str, b: str) -> float:
        """Вычислить косинусное сходство между двумя паттернами."""
        vec_a = self._get_vector(a)
        vec_b = self._get_vector(b)
        length = min(len(vec_a), len(vec_b))
        if length == 0:
            return 0.0
        return float(cosine_similarity(vec_a[:length], vec_b[:length]))

    def _get_vector(self, pattern_id: str) -> CoreVector:
        """Получить или детерминированно вывести вектор паттерна."""
        if pattern_id in self.seeds:
            return self.seeds[pattern_id].representation

        digest = hashlib.sha256(pattern_id.encode()).digest()
        values = [float(byte) for byte in digest[:16]]
        vector = normalize(values)
        total_dim = self.base_dim + 12
        if len(vector) >= total_dim:
            return CoreVector(vector[:total_dim])
        return CoreVector(list(vector) + [0.0] * (total_dim - len(vector)))

    def expand_seed(self, base_seed_id: str, depth: int = 3) -> List[Tuple[str, float]]:
        """Раскрыть все значимые корреляции из семени."""
        results = []
        for seed_name in self.seeds:
            if seed_name == base_seed_id:
                continue
            corr = self.get_correlation(base_seed_id, seed_name)
            if abs(corr) > 0.1:
                results.append((seed_name, corr))
        results.sort(key=lambda item: abs(item[1]), reverse=True)
        return results[: depth * 3]

    def find_bridges(self, from_seed: str, to_seed: str, max_hops: int = 3) -> Dict:
        """Найти мосты между двумя паттернами."""
        from_expanded = self.expand_seed(from_seed, max_hops)
        to_expanded = self.expand_seed(to_seed, max_hops)
        bridges = {name for name, _ in from_expanded} & {name for name, _ in to_expanded}
        bridge_correlations = []
        for bridge in bridges:
            c1 = self.get_correlation(from_seed, bridge)
            c2 = self.get_correlation(bridge, to_seed)
            bridge_correlations.append((bridge, c1 * c2))
        return {
            "from": from_seed,
            "to": to_seed,
            "bridges": list(bridges),
            "strength": [corr for _, corr in bridge_correlations],
            "common_count": len(bridges),
        }


class Explorer:
    """Система открывает связи, а не обучается."""

    def __init__(self):
        self.engine = CorrelationEngine()
        self.found_correlations: Dict[Tuple[str, str], float] = {}
        self.explored_seeds: Set[str] = set()

    def explore_from(self, seed_id: str, depth: int = 2) -> Dict:
        if seed_id not in self.explored_seeds:
            self.explored_seeds.add(seed_id)
        expanded = self.engine.expand_seed(seed_id, depth)
        results = {}
        for target, corr in expanded:
            self.found_correlations[(seed_id, target)] = corr
            results[target] = {"correlation": corr, "is_seed": target in self.engine.seeds}
        return results

    def discover_path(self, from_id: str, to_id: str) -> List[Tuple[str, float]]:
        direct = self.engine.get_correlation(from_id, to_id)
        if abs(direct) > 0.5:
            return [(to_id, direct)]
        bridge_result = self.engine.find_bridges(from_id, to_id)
        if not bridge_result["bridges"]:
            return []
        path = [(from_id, 1.0)]
        for bridge in bridge_result["bridges"]:
            path.append((bridge, self.engine.get_correlation(from_id, bridge)))
        strength = bridge_result["strength"][-1] if bridge_result["strength"] else 0.0
        path.append((to_id, strength))
        return path

    def query(self, concept: str) -> Dict:
        results = {"concept": concept, "correlations": {}, "seed_bridges": [], "path_to": {}}
        for seed_name in BASE_SEEDS:
            corr = self.engine.get_correlation(concept, seed_name)
            if abs(corr) > 0.2:
                results["seed_bridges"].append((seed_name, corr))
        results["seed_bridges"].sort(key=lambda item: abs(item[1]), reverse=True)
        return results


def demo():
    """Демонстрация."""
    explorer = Explorer()
    print(explorer.query("ml"))


if __name__ == "__main__":
    demo()
