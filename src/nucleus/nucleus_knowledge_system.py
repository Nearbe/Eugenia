#!/usr/bin/env python3
"""
Universal Knowledge System — Nucleus
=================================

Ядро системы, которое:
1. ПОГЛОЩАЕТ любые данные → паттерны
2. ГЕНЕРИРУЕТ данные из паттернов
3. СОЗДАЁТ корреляции во время работы
4. УСИЛИВАЕТ знакомые паттерны

Основано на RealMath:
- D(a) = создание различий
- L(M) = глубина информации
- Ω → Π = потенциал → полнота

Integration with src/core/:
- delta_field: logarithmic transformation of data values
- complex_delta_field: complex-valued delta transformation
- D(), H(): branching and compression operators
- solenoid_encode_pattern: lossless pattern encoding
- fractal_pattern_signature: topological pattern signature
- pattern_similarity_from_delta: RealMath-aware similarity
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from core.realmath import (
    delta_field,
    complex_delta_field,
    solenoid_encode_pattern,
    solenoid_pattern_distance,
    fractal_pattern_signature,
    pattern_similarity_from_delta,
    pattern_similarity_from_complex,
    pattern_distance_from_delta,
    dual_pattern_transform,
    fractal_pyramid_structure,
    pattern_spine_chain,
    pattern_pyramid_depth,
    pattern_bridge_identity,
)


# ============================================================
# Core Data Structures
# ============================================================


@dataclass
class PatternNode:
    """
    Узел паттерна — единица знаний

    pattern: геометрический профиль (RealMath-enhanced)
    correlations: связанные паттерны (node_id → strength)
    usage_count: сколько раз использован
    created_at: время создания
    solenoid: solenoid-encoded trajectory for lossless storage
    fractal_sig: fractal pattern signature
    pyramid: fractal pyramid structure for branching analysis
    spine_chain: Ω → Π spine chain for depth mapping
    bridge: bridge identity through Ω
    """

    node_id: str
    pattern: np.ndarray  # Геометрический профиль
    correlations: Dict[str, float] = field(default_factory=dict)  # node_id -> strength
    usage_count: int = 0
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
    solenoid: Optional[list[int]] = None  # Binary trajectory
    fractal_sig: Optional[dict] = None  # Fractal pattern signature
    pyramid: Optional[list[dict]] = None  # Fractal pyramid structure
    spine_chain: Optional[list[dict]] = None  # Ω → Π spine chain
    bridge: Optional[dict] = None  # Bridge identity through Ω


# ============================================================
# Geometric Pattern Extractor
# ============================================================


class GeometricExtractor:
    """
    Извлекает геометрические паттерны с RealMath интеграцией.

    Enhanced pipeline:
    1. Delta field transformation: X → log2(X+1) - log2(256-X)
    2. Complex delta field: X → complex(x, 1-x)
    3. Solenoid encoding: lossless binary trajectory
    4. Fractal pattern signature: topological invariant
    5. Dual number transform: form + growth potential
    6. Branching-aware similarity: RealMath-aware comparison
    """

    def __init__(self, n_thresholds: int = 64, solenoid_depth: int = 30, pyramid_levels: int = 10):
        self.n_thresholds = n_thresholds
        self.solenoid_depth = solenoid_depth
        self.pyramid_levels = pyramid_levels

    def extract(self, data: Any) -> np.ndarray:
        """
        Извлечь паттерн из ЛЮБЫХ данных с RealMath enhancement.

        Pipeline:
        1. Normalize to [0, 1] (or [0, 255] for pixel data)
        2. Transform through delta_field (logarithmic spine scale)
        3. Compute fractal signature
        4. Encode through solenoid
        5. Combine into unified pattern vector
        """
        # Normalize to pixel-like range [0, 255] for delta_field
        arr = self._normalize_to_delta_range(data)

        # RealMath: delta field transformation
        delta_values = delta_field(arr)

        # RealMath: fractal pattern signature
        self._last_fractal_sig = fractal_pattern_signature(arr.tolist())

        # RealMath: solenoid encoding
        self._last_solenoid = solenoid_encode_pattern(arr.tolist(), self.solenoid_depth)

        # RealMath: complex delta field
        complex_vals = complex_delta_field(arr)
        complex_real = [c.real for c in complex_vals]
        complex_imag = [c.imag for c in complex_vals]

        # RealMath: dual number transform (form + derivative)
        form, velocity = dual_pattern_transform(arr.tolist(), list(np.gradient(arr)))

        # RealMath: fractal pyramid structure
        self._last_pyramid = fractal_pyramid_structure(self.pyramid_levels)

        # RealMath: Ω → Π spine chain
        self._last_spine_chain = pattern_spine_chain(self.pyramid_levels)

        # RealMath: pyramid depth for avg value
        self._last_pyramid_depth = pattern_pyramid_depth(float(np.mean(arr)))

        # RealMath: bridge identity check
        self._last_bridge = pattern_bridge_identity(float(np.mean(arr)))

        # Combine into unified pattern vector
        components = [
            # Delta field profile (sweep)
            self._delta_sweep_profile(arr),
            # Fractal signature
            self._last_fractal_sig["profile"][: self.n_thresholds],
            # Topological jumps
            self._last_fractal_sig["top_jumps"]
            + [0.0] * (5 - len(self._last_fractal_sig["top_jumps"])),
            # Fractal dimension + spine level (scalar features)
            [
                self._last_fractal_sig["fractal_dimension"],
                self._last_fractal_sig["spine_level"],
                self._last_fractal_sig["percentage"],
                self._last_fractal_sig["avg_value"],
            ],
            # Complex delta norms
            [
                np.mean(complex_real),
                np.std(complex_real),
                np.mean(complex_imag),
                np.std(complex_imag),
            ],
            # Dual number statistics
            [np.mean(form), np.std(form), np.mean(velocity), np.std(velocity)],
            # Solenoid stats (compact representation)
            [
                sum(self._last_solenoid) / len(self._last_solenoid) if self._last_solenoid else 0.0,
                self._last_solenoid.count(1) if self._last_solenoid else 0.0,
            ],
            # Pyramid structure (bridge analysis for each level)
            [
                self._last_pyramid[i]["bridge_analysis"]["left_spine_level"]
                if self._last_pyramid
                else 0.0
                for i in range(min(5, len(self._last_pyramid) if self._last_pyramid else 0))
            ],
            # Spine chain (top 5 spine levels)
            [
                self._last_spine_chain[i]["spine_level"] if self._last_spine_chain else 0.0
                for i in range(min(5, len(self._last_spine_chain) if self._last_spine_chain else 0))
            ],
            # Pyramid depth + bridge identity
            [
                self._last_pyramid_depth if self._last_pyramid_depth else 0.0,
                1.0 if (self._last_bridge and self._last_bridge.get("bridge_identity")) else 0.0,
            ],
        ]

        pattern = np.concatenate([c for c in components if c]).astype(np.float32)
        return pattern

    def _delta_sweep_profile(self, arr: np.ndarray) -> list[float]:
        """Compute delta field sweep profile at multiple thresholds."""
        thresholds = np.linspace(0, 1, self.n_thresholds)
        return [float(np.mean(arr > t)) for t in thresholds]

    def _normalize_to_delta_range(self, data: Any) -> np.ndarray:
        """Normalize data to [0, 255] range for delta_field compatibility."""
        if isinstance(data, str):
            arr = np.array([ord(c) for c in data])
        elif hasattr(data, "flatten"):
            arr = data.flatten().astype(float)
        else:
            arr = np.array([float(data)])

        arr_min = arr.min()
        arr_max = arr.max()
        range_val = arr_max - arr_min

        if range_val < 1e-10:
            return np.full_like(arr, 127.5, dtype=float)  # Mid-gray for constant data

        # Normalize to [0, 255]
        return (arr - arr_min) / range_val * 255.0

    def similarity(self, p1: np.ndarray, p2: np.ndarray) -> float:
        """
        RealMath-aware pattern similarity.

        Uses delta-space cosine similarity when possible,
        falling back to standard cosine similarity.
        """
        # Try RealMath delta-space similarity first
        try:
            # Extract the raw values from the pattern (first portion)
            n = min(len(p1), len(p2), 64)
            vals1 = p1[:n].tolist()
            vals2 = p2[:n].tolist()
            delta_sim = pattern_similarity_from_delta(vals1, vals2)
            complex_sim = pattern_similarity_from_complex(vals1, vals2)

            # Weighted combination: delta-space is more meaningful
            return 0.6 * delta_sim + 0.4 * complex_sim
        except (ValueError, TypeError):
            pass

        # Fallback: standard cosine similarity
        norm1 = np.linalg.norm(p1)
        norm2 = np.linalg.norm(p2)

        if norm1 < 1e-10 or norm2 < 1e-10:
            return 0.0

        return float(np.dot(p1, p2) / (norm1 * norm2))

    def distance(self, p1: np.ndarray, p2: np.ndarray) -> float:
        """RealMath-aware distance between patterns."""
        n = min(len(p1), len(p2), 64)
        vals1 = p1[:n].tolist()
        vals2 = p2[:n].tolist()
        return pattern_distance_from_delta(vals1, vals2)

    def solenoid_distance(self, node_a: PatternNode, node_b: PatternNode) -> float:
        """Compute solenoid distance between two pattern nodes."""
        if node_a.solenoid and node_b.solenoid:
            return solenoid_pattern_distance(node_a.solenoid, node_b.solenoid)
        # Fallback to pattern-based solenoid distance
        return solenoid_pattern_distance(
            node_a.pattern[:64].tolist(),
            node_b.pattern[:64].tolist(),
        )


# ============================================================
# Universal Knowledge System
# ============================================================


class KnowledgeSystem:
    """
    ГЛАВНАЯ СИСТЕМА

    Функции:
    1. absorb(data) → создаёт node с паттерном
    2. generate(context) → создаёт данные из паттернов
    3. relate(new_node) → связывает с существующими
    4. strengthen(node_id) → усиливает при использовании
    """

    def __init__(self, similarity_threshold: float = 0.7):
        self.extractor = GeometricExtractor()
        self.nodes: Dict[str, PatternNode] = {}
        self.similarity_threshold = similarity_threshold
        self._node_counter = 0

    def absorb(self, data: Any, label: Optional[str] = None) -> str:
        """
        ПОГЛОЩЕНИЕ данных — создаёт новый паттерн с RealMath enhancement.

        data: что угодно (текст, изображение, числа...)
        label: опциональная метка

        Returns: node_id нового узла
        """
        # Извлекаем паттерн (with RealMath enhancement)
        pattern = self.extractor.extract(data)

        # Store solenoid encoding and fractal signature
        solenoid = self.extractor._last_solenoid
        fractal_sig = self.extractor._last_fractal_sig
        pyramid = self.extractor._last_pyramid
        spine_chain = self.extractor._last_spine_chain
        bridge = self.extractor._last_bridge

        # Генерируем ID
        node_id = label or f"node_{self._node_counter}"
        self._node_counter += 1

        # Создаём узел
        node = PatternNode(
            node_id=node_id,
            pattern=pattern,
            solenoid=solenoid,
            fractal_sig=fractal_sig,
            pyramid=pyramid,
            spine_chain=spine_chain,
            bridge=bridge,
        )

        self.nodes[node_id] = node

        # Автоматически связываем с существующими
        self._auto_relate(node_id)

        return node_id

    def _auto_relate(self, node_id: str):
        """
        Автоматическое связывание с существующими паттернами.

        Uses RealMath-aware similarity (delta-space + complex-space).
        """
        if not self.nodes:
            return

        new_node = self.nodes[node_id]
        new_pattern = new_node.pattern

        for existing_id, existing_node in self.nodes.items():
            if existing_id == node_id:
                continue

            # Compute RealMath-aware similarity
            sim = self.extractor.similarity(new_pattern, existing_node.pattern)

            # If sufficiently similar — connect
            if sim > self.similarity_threshold:
                # Add correlation in both directions
                new_node.correlations[existing_id] = sim
                existing_node.correlations[node_id] = sim

    def relate(self, source_id: str, target_id: str, strength: float = 1.0):
        """
        Созда��ь корреляцию между двумя паттернами

        source_id: откуда
        target_id: куда
        strength: сила связи (0-1)
        """
        if source_id not in self.nodes or target_id not in self.nodes:
            return

        self.nodes[source_id].correlations[target_id] = strength
        self.nodes[target_id].correlations[source_id] = strength

    def strengthen(self, node_id: str):
        """
        УСИЛЕНИЕ паттерна при использовании

        - Увеличиваем usage_count
        - Усиливаем связанные корреляции
        """
        if node_id not in self.nodes:
            return

        node = self.nodes[node_id]
        node.usage_count += 1
        node.last_used = time.time()

        # Усиливаем связанные паттерны
        for related_id in node.correlations:
            if related_id in self.nodes:
                # Корреляция немного усиливается
                node.correlations[related_id] = min(1.0, node.correlations[related_id] * 1.05)

    def generate(self, context_node_id: str, max_nodes: int = 5) -> List[str]:
        """
        ГЕНЕРАЦИЯ — находим связанные паттерны

        context_node_id: откуда начинаем
        max_nodes: сколько найти

        Returns: [node_id, ...] связанных узлов
        """
        if context_node_id not in self.nodes:
            return []

        context_node = self.nodes[context_node_id]

        # Сортируем по силе корреляции
        related = sorted(context_node.correlations.items(), key=lambda x: x[1], reverse=True)

        # Усиливаем найденные
        for node_id, _ in related[:max_nodes]:
            self.strengthen(node_id)

        return [nid for nid, _ in related[:max_nodes]]

    def find_similar(self, data: Any, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Найти похожие паттерны для новых данных

        Returns: [(node_id, similarity), ...]
        """
        query_pattern = self.extractor.extract(data)

        similarities = []
        for node_id, node in self.nodes.items():
            sim = self.extractor.similarity(query_pattern, node.pattern)
            similarities.append((node_id, sim))

        # Сортируем по убыванию
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def query(self, data: Any) -> Dict[str, Any]:
        """
        Полный запрос — найти и усилить

        1. Находим похожие паттерны
        2. Связываем новые данные с ними
        3. Усиливаем причастные узлы
        """
        # Находим похожие
        similar = self.find_similar(data, top_k=3)

        if not similar:
            # Новый паттерн — добавляем
            node_id = self.absorb(data)
            return {"status": "new", "node_id": node_id, "similar": []}

        # Используем наиболее похожий
        best_id, best_sim = similar[0]

        # Усиливаем
        self.strengthen(best_id)

        # Если очень похоже — связываем
        if best_sim > 0.95:
            new_id = self.absorb(data)
            self.relate(new_id, best_id, best_sim)

        # Генерируем связанные
        related = self.generate(best_id)

        return {
            "status": "existing",
            "best_match": best_id,
            "similarity": best_sim,
            "related": related,
        }

    def get_stats(self) -> Dict[str, Any]:
        """Статистика системы"""
        total_correlations = sum(len(n.correlations) for n in self.nodes.values())

        most_used = (
            max(self.nodes.items(), key=lambda x: x[1].usage_count)[0] if self.nodes else None
        )

        return {
            "total_nodes": len(self.nodes),
            "total_correlations": total_correlations,
            "most_used_node": most_used,
            "most_used_count": self.nodes[most_used].usage_count if most_used else 0,
        }


# ============================================================
# Demo
# ============================================================


def demo():
    """Демонстрация системы"""
    print("=" * 60)
    print("UNIVERSAL KNOWLEDGE SYSTEM — Nucleus")
    print("=" * 60)

    # Создаём систему
    system = KnowledgeSystem(similarity_threshold=0.5)

    print("\n1. ПОГЛОЩЕНИЕ данных:")

    # Поглощаем разные типы данных
    texts = [
        "собака",
        "кошка",
        "кот",
        "машинное обучение",
        "нейронная сеть",
        " transformer",
    ]

    for text in texts:
        node_id = system.absorb(text)
        print(f"  Поглощён: '{text}' → {node_id}")

    # Статистика
    stats = system.get_stats()
    print(f"\n  Всего узлов: {stats['total_nodes']}")
    print(f"  Всего связей: {stats['total_correlations']}")

    print("\n2. КОРРЕЛЯЦИИ:")

    # Показываем корреляции для "собака"
    dog_node_id = [k for k in system.nodes.keys() if "собака" in k]
    if dog_node_id:
        node = system.nodes[dog_node_id[0]]
        if node.correlations:
            print(f"  '{dog_node_id[0]}' связан с:")
            for related_id, strength in sorted(
                node.correlations.items(), key=lambda x: x[1], reverse=True
            )[:3]:
                print(f"    - {related_id}: {strength:.3f}")

    print("\n3. ГЕНЕРАЦИЯ (поиск связанных):")

    for text in texts[:3]:
        node_id = [k for k in system.nodes.keys() if text in k]
        if node_id:
            related = system.generate(node_id[0])
            print(f"  '{text}' → {related[:3]}")

    print("\n4. РАБОТА С НОВЫМИ ДАННЫМИ:")

    # Новый запрос
    result = system.query("собака это домашнее животное")
    print("  Запрос 'собака это домашнее животное':")
    print(f"    status: {result['status']}")
    if result.get("best_match"):
        print(f"    best: {result['best_match']} ({result['similarity']:.3f})")
        print(f"    related: {result['related']}")

    # Ещё один запрос
    result2 = system.query("кот мурлычет")
    print("\n  Запрос 'кот мурлычет':")
    print(f"    status: {result2['status']}")
    if result2.get("best_match"):
        print(f"    best: {result2['best_match']} ({result2['similarity']:.3f})")

    print("\n" + "=" * 60)
    print("KEY: Система учится во время работы!")
    print("=" * 60)
    print("""
    Что происходит:

    1. absorb() → Создаёт паттерн для ЛЮБЫХ данных
    2. relate() → Связывает новый с существующими
    3. generate() → Находит связанные паттерны
    4. strengthen() → Усиливает при использован

    Результат:
    - Система учится новому при каждом запросе!
    - Корреляции создаются АВТОМАТИЧЕСКИ!
    - Знакомые паттерны УСИЛИВАЮТСЯ!
    """)


if __name__ == "__main__":
    demo()
