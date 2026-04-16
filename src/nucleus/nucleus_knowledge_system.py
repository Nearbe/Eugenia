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
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any

import numpy as np


# ============================================================
# Core Data Structures
# ============================================================


@dataclass
class PatternNode:
    """
    Узел паттерна — единица знаний

    pattern: геометрический профиль
    correlations: связанные паттерны (node_id → strength)
    usage_count: сколько раз использован
    created_at: время создания
    """

    node_id: str
    pattern: np.ndarray  # Геометрический профиль
    correlations: Dict[str, float] = field(default_factory=dict)  # node_id -> strength
    usage_count: int = 0
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)


# ============================================================
# Geometric Pattern Extractor
# ============================================================


class GeometricExtractor:
    """
    Извлекает геометрические паттерны

    Метод:
    1. Бинарный sweep — разные пороги
    2. Jump events — критические изменения
    3. Betti signature — топологические инварианты
    """

    def __init__(self, n_thresholds: int = 64):
        self.n_thresholds = n_thresholds

    def extract(self, data: Any) -> np.ndarray:
        """
        Извлечь паттерн из ЛЮБЫХ данных

        data: может быть текст, изображение, аудио, числа...
        """
        # Конвертируем в массив
        arr = self._normalize(data)

        # Бинарный sweep
        thresholds = np.linspace(0, 1, self.n_thresholds)
        binary_profile = np.array([np.mean(arr > t) for t in thresholds])

        # Jump events (изменения между порогами)
        jumps = np.abs(np.diff(binary_profile))

        # Простейшая топология: connected regions
        # (упрощено для скорости)
        topology = np.array([np.sum(arr[arr > t] > 0) for t in thresholds[::4]])

        # Комбинируем
        pattern = np.concatenate(
            [
                binary_profile,
                jumps * 10,  # Масштабируем
                topology[:16] / max(np.max(topology), 1),  # Нормализуем
            ]
        )

        return pattern.astype(np.float32)

    def _normalize(self, data: Any) -> np.ndarray:
        """Нормализовать к [0, 1]"""
        if isinstance(data, str):
            # Текст → хеши символов
            arr = np.array([ord(c) for c in data])
            arr = arr - arr.min()
            arr = arr / (arr.max() + 1e-10)
            return arr

        elif hasattr(data, "flatten"):
            # Изображение, массив
            arr = data.flatten().astype(float)
            arr = arr - arr.min()
            arr = arr / (arr.max() + 1e-10)
            return arr

        else:
            # Числа и т.д.
            arr = np.array([float(data)])
            arr = arr - arr.min()
            arr = arr / (max(arr.max(), 1e-10))
            return arr

    def similarity(self, p1: np.ndarray, p2: np.ndarray) -> float:
        """Косинусное сходство паттернов"""
        norm1 = np.linalg.norm(p1)
        norm2 = np.linalg.norm(p2)

        if norm1 < 1e-10 or norm2 < 1e-10:
            return 0.0

        return np.dot(p1, p2) / (norm1 * norm2)


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
        ПОГЛОЩЕНИЕ данных — создаёт новый паттерн

        data: что угодно (текст, изображение, числа...)
        label: опциональная метка

        Returns: node_id нового узла
        """
        # Извлекаем паттерн
        pattern = self.extractor.extract(data)

        # Генерируем ID
        node_id = label or f"node_{self._node_counter}"
        self._node_counter += 1

        # Создаём узел
        node = PatternNode(
            node_id=node_id,
            pattern=pattern,
        )

        self.nodes[node_id] = node

        # Автоматически связываем с существующими
        self._auto_relate(node_id)

        return node_id

    def _auto_relate(self, node_id: str):
        """
        Автоматическое связывание с существующими паттернами

        Ключевая функция: система САМА находит связи!
        """
        if not self.nodes:
            return

        new_node = self.nodes[node_id]
        new_pattern = new_node.pattern

        for existing_id, existing_node in self.nodes.items():
            if existing_id == node_id:
                continue

            # Вычисляем сходство
            sim = self.extractor.similarity(new_pattern, existing_node.pattern)

            # Если достаточно похоже — связываем
            if sim > self.similarity_threshold:
                # Добавляем корреляцию в обе стороны
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
