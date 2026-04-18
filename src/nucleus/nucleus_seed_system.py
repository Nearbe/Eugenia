#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nucleus — Seed-Based Knowledge System
=====================================

Научное обоснование
-------------------
Данная модуль реализует концепцию семенного знания (seed-based knowledge),
где все паттерны выводятся из базового набора аксиоматических семян.

Математическая формализация:
    Пусть S = {s₁, s₂, ..., sₙ} — множество базовых семян.
    Каждое семя sᵢ ∈ ℝᵈ представляется как вектор в d-мерном пространстве.

    Корреляция между двумя паттернами определяется как косинусное сходство:

        corr(a, b) = ⟨a, b⟩ / (‖a‖ · ‖b‖)

    где ⟨·,·⟩ — скалярное произведение, ‖·‖ — евклидова норма.

Ключевые принципы:
    1. Детерминизм: корреляции вычисляются, а не обучаются
    2. Полнота: для любого семени всё связано со всем
    3. Раскрытие: система открывает существующие связи, а не создаёт новые

Атрибуты
--------
    BASE_SEEDS : Dict[str, np.ndarray]
        Словарь базовых геометрических семян с их векторными представлениями.

Классы
------
    Seed
        Структура данных для представления семени.
    CorrelationEngine
        Движок вычисления корреляций между паттернами.
    Explorer
        Система исследования и открытия связей между концептами.

Пример использования
--------------------
    >>> explorer = Explorer()
    >>> correlations = explorer.explore_from("point", depth=2)
    >>> bridges = explorer.engine.find_bridges("circle", "square")
    >>> path = explorer.discover_path("point", "sphere")

Ссылки
------
    [1] Eckart, C., & Young, G. (1936). The approximation of one matrix
        by another of lower rank. Psychometrika, 1(3), 211-218.
    [2] Golub, G. H., & Van Loan, C. F. (2013). Matrix computations.
        JHU Press. (SVD и разложения матриц)
"""

import hashlib
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import numpy as np


# ============================================================
# BASE SEEDS — фундаментальные паттерны
# ============================================================


@dataclass
class Seed:
    """
    Базовое семя — начало всех паттернов.

    Атрибуты
    --------
    seed_id : str
        Уникальный идентификатор семени.
    representation : np.ndarray
        Векторное представление семени в пространстве признаков.
    description : str
        Текстовое описание семени.
    basic : bool, optional
        Флаг базового семени (по умолчанию True).
    """

    seed_id: str
    representation: np.ndarray  # Вектор в space
    description: str
    basic: bool = True  # Это базовое семя?


# Базовые геометрические семена — ИЗ НИХ ВСЁ ВЫВОДИТСЯ!
BASE_SEEDS = {
    # Точка — нульмерная
    "point": np.array([1.0, 0.0, 0.0, 0.0]),
    # Линия — одномерная (2 точки)
    "line": np.array([0.0, 1.0, 0.0, 0.0]),
    # Угол — 2 линии под углом
    "angle": np.array([0.0, 0.0, 1.0, 0.0]),
    # Плоскость — 2 измерения
    "plane": np.array([0.0, 0.0, 0.0, 1.0]),
    # Круг — замкнутая кривая
    "circle": np.array([1.0, 1.0, 0.0, 0.0]),
    # Квадрат — 4 стороны
    "square": np.array([1.0, 0.5, 0.5, 0.0]),
    # Треугольник — 3 угла
    "triangle": np.array([0.0, 1.0, 1.0, 0.0]),
    # Сфера — 3D круг
    "sphere": np.array([1.0, 1.0, 1.0, 0.0]),
    # Цепочка — последовательность
    "chain": np.array([0.0, 0.5, 0.5, 1.0]),
    # Дерево — ветвление
    "tree": np.array([0.0, 0.0, 0.0, 0.5]),
    # Кольцо — цикл
    "ring": np.array([1.0, 1.0, 0.0, 0.5]),
    # Сеть — переплетение
    "net": np.array([0.0, 0.0, 1.0, 1.0]),
}


# ============================================================
# UNIVERSAL CORRELATION ENGINE
# ============================================================


class CorrelationEngine:
    """
    Универсальный движок вычисления корреляций.

    Научное обоснование
    -------------------
    Данный класс реализует детерминированное вычисление корреляций между
    паттернами на основе их векторных представлений. Ключевая идея заключается
    в том, что корреляции не обучаются, а вычисляются непосредственно из
    математических свойств векторов.

    Математическая формализация
    ---------------------------
    Для двух векторов a, b ∈ ℝᵈ косинусное сходство определяется как:

        cos(θ) = ⟨a, b⟩ / (‖a‖₂ · ‖b‖₂)

    где:
        ⟨a, b⟩ = Σᵢ aᵢ·bᵢ — скалярное произведение,
        ‖a‖₂ = √(Σᵢ aᵢ²) — L2-норма (евклидова длина).

    Свойства:
        • cos(θ) ∈ [-1, 1]
        • cos(θ) = 1 ⇒ векторы сонаправлены
        • cos(θ) = -1 ⇒ векторы противоположно направлены
        • cos(θ) = 0 ⇒ векторы ортогональны

    Атрибуты
    --------
    base_dim : int
        Базовая размерность пространства признаков.
    seeds : Dict[str, Seed]
        Словарь зарегистрированных семян с их векторными представлениями.

    Пример использования
    --------------------
        >>> engine = CorrelationEngine(base_dim=4)
        >>> corr = engine.get_correlation("point", "line")
        >>> print(f"Корреляция: {corr:.3f}")
    """

    def __init__(self, base_dim: int = 4):
        """
        Инициализация движка корреляций.

        Параметры
        ---------
        base_dim : int, optional
            Базовая размерность пространства (по умолчанию 4).
        """
        self.base_dim = base_dim

        # Семена — начальная база
        self.seeds: Dict[str, Seed] = {}
        for name, vector in BASE_SEEDS.items():
            self.seeds[name] = Seed(
                seed_id=name,
                representation=vector,
                description=self._describe_seed(name),
                basic=True,
            )

    def _describe_seed(self, name: str) -> str:
        """
        Получить текстовое описание базового семени.

        Параметры
        ---------
        name : str
            Имя семени.

        Возвращает
        ----------
        str
            Текстовое описание геометрического смысла семени.
        """
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
        """
        Вычислить корреляцию между двумя паттернами.

        Научное обоснование
        -------------------
        Корреляция вычисляется как косинусное сходство векторных
        представлений паттернов. Это детерминированная операция,
        не требующая обучения.

        Параметры
        ---------
        a : str
            Идентификатор первого паттерна.
        b : str
            Идентификатор второго паттерна.

        Возвращает
        ----------
        float
            Значение корреляции в диапазоне [-1, 1].

        Примечания
        ----------
        При нулевой норме одного из векторов возвращается 0.0.
        """
        # Если одно из семян — вычисляем напрямую
        vec_a = self._get_vector(a)
        vec_b = self._get_vector(b)

        # Normalize to same dimension
        min_dim = min(len(vec_a), len(vec_b))
        vec_a = vec_a[:min_dim]
        vec_b = vec_b[:min_dim]

        # Cosine similarity
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a < 1e-10 or norm_b < 1e-10:
            return 0.0

        correlation = np.dot(vec_a, vec_b) / (norm_a * norm_b)

        return float(correlation)

    def _get_vector(self, pattern_id: str) -> np.ndarray:
        """
        Получить векторное представление паттерна.

        Параметры
        ---------
        pattern_id : str
            Идентификатор паттерна.

        Возвращает
        ----------
        np.ndarray
            Векторное представление паттерна в пространстве признаков.

        Примечания
        ----------
        Для неизвестных паттернов используется детерминированное
        хеширование через SHA-256 для генерации воспроизводимого вектора.
        """
        if pattern_id in self.seeds:
            return self.seeds[pattern_id].representation

        # Хешируем для новых паттернов — детерминировано!
        h = hashlib.sha256(pattern_id.encode()).digest()
        vec = np.frombuffer(h[:16], dtype=np.uint8).astype(float)
        vec = vec / (np.linalg.norm(vec) + 1e-10)

        # Добавляем базовую размерность
        total_dim = self.base_dim + 12
        full_vec = np.zeros(total_dim)
        vec_len = min(len(vec), total_dim)
        full_vec[:vec_len] = vec[:vec_len]

        return full_vec

    def expand_seed(self, base_seed_id: str, depth: int = 3) -> List[Tuple[str, float]]:
        """
        Раскрыть все корреляции из семени

        depth — сколько уровней вложенности
        """
        # Находим все связанные паттерны
        results = []
        for seed_name in self.seeds:
            if seed_name == base_seed_id:
                continue

            corr = self.get_correlation(base_seed_id, seed_name)
            if abs(corr) > 0.1:  # Порог значимости
                results.append((seed_name, corr))

        # Сортируем по силе
        results.sort(key=lambda x: abs(x[1]), reverse=True)

        return results[: depth * 3]  # Топ результатов

    def find_bridges(self, from_seed: str, to_seed: str, max_hops: int = 3) -> Dict:
        """
        Найти мосты между двумя паттернами

        Какие общие паттерны их связывают?
        """
        # Расширяем оба конца
        from_expanded = self.expand_seed(from_seed, max_hops)
        to_expanded = self.expand_seed(to_seed, max_hops)

        from_set = set(n for n, _ in from_expanded)
        to_set = set(n for n, _ in to_expanded)

        # Пересечение — мосты
        bridges = from_set & to_set

        # С��ла ��оста — через общее
        bridge_correlations = []
        for bridge in bridges:
            c1 = self.get_correlation(from_seed, bridge)
            c2 = self.get_correlation(bridge, to_seed)
            bridge_correlations.append((bridge, c1 * c2))

        return {
            "from": from_seed,
            "to": to_seed,
            "bridges": list(bridges),
            "strength": [c for _, c in bridge_correlations],
            "common_count": len(bridges),
        }


# ============================================================
# EXPLORER — система открывает связи
# ============================================================


class Explorer:
    """
    ИССЛЕДОВАТЕЛЬ — система открывает связи

    Ключевое отличие:
    - Мы НЕ обучаемся
    - Мы ОТКРЫВАЕМ то, что УЖЕ ЕСТЬ
    """

    def __init__(self):
        self.engine = CorrelationEngine()
        self.found_correlations: Dict[Tuple[str, str], float] = {}
        self.explored_seeds: Set[str] = set()

    def explore_from(self, seed_id: str, depth: int = 2) -> Dict:
        """
        Исследовать все связи из семени

        seed_id: с чего начинаем
        depth: глубина исследования
        """
        if seed_id not in self.explored_seeds:
            self.explored_seeds.add(seed_id)

        # Раскрываем все корреляции
        expanded = self.engine.expand_seed(seed_id, depth)

        # Сохраняем найденное
        results = {}
        for target, corr in expanded:
            key = (seed_id, target)
            self.found_correlations[key] = corr

            results[target] = {
                "correlation": corr,
                "is_seed": target in self.engine.seeds,
            }

        return results

    def discover_path(self, from_id: str, to_id: str) -> List[Tuple[str, float]]:
        """
        Найти путь между двумя паттернами

        Returns: [(паттерн, корреляция), ...] по порядку
        """
        # Сначала пробуем прямой мост
        direct = self.engine.get_correlation(from_id, to_id)

        if abs(direct) > 0.5:
            return [
                (to_id, direct),
            ]

        # Ищем через мосты
        bridge_result = self.engine.find_bridges(from_id, to_id)

        if bridge_result["bridges"]:
            path = [(from_id, 1.0)]

            for bridge in bridge_result["bridges"]:
                corr = self.engine.get_correlation(from_id, bridge)
                path.append((bridge, corr))

            path.append(
                (
                    to_id,
                    bridge_result["strength"][-1] if bridge_result["strength"] else 0,
                )
            )

            return path

        return []

    def query(self, concept: str) -> Dict:
        """
        Запрос — найти все связанное с концептом
        """
        results = {
            "concept": concept,
            "correlations": {},
            "seed_bridges": [],
            "path_to": {},
        }

        # Что мы знаем о семенах
        for seed_name in BASE_SEEDS.keys():
            corr = self.engine.get_correlation(concept, seed_name)
            if abs(corr) > 0.2:
                results["seed_bridges"].append((seed_name, corr))

        # Сортируем
        results["seed_bridges"].sort(key=lambda x: abs(x[1]), reverse=True)

        return results


# ============================================================
# DEMO
# ============================================================


def demo():
    """Демонстрация"""
    print("=" * 60)
    print("Nucleus — Seed-Based SYSTEM")
    print("=" * 60)

    explorer = Explorer()

    print("\n1. СЕМЕНА (базовые паттерны):")
    for name, seed in explorer.engine.seeds.items():
        print(f"  {name}: {seed.description}")

    print("\n2. КОРРЕЛЯЦИИ ТОЧКИ:")
    correlations = explorer.explore_from("point", depth=2)
    for target, data in list(correlations.items())[:5]:
        marker = "★" if data["is_seed"] else "○"
        print(f"  {marker} {target}: {data['correlation']:.3f}")

    print("\n3. КРУГ ↔ КВАДРАТ — мосты:")
    bridges = explorer.engine.find_bridges("circle", "square")
    print(f"  bridges: {bridges['bridges']}")
    print(f"  common: {bridges['common_count']}")

    print("\n4. ПУТЬ ОТ ТОЧКИ ДО СФЕРЫ:")
    path = explorer.discover_path("point", "sphere")
    print(f"  path: {[p[0] for p in path]}")

    print("\n5. ЛЮБОЙ КОНЦЕПТ — поиск связей:")
    result = explorer.query("ml")
    for seed, corr in result["seed_bridges"][:5]:
        print(f"  {seed}: {corr:.3f}")

    print("\n" + "=" * 60)
    print("КЛЮЧЕВОЙ ИНСАЙТ:")
    print("=" * 60)
    print("""
    Нам НЕ нужно обучаться!

    Корреляции УЖЕ СУЩЕСТВУЮТ между ВСЕМ паттернами.
    Нам нужно просто ИХ ВЫЧИСЛИТЬ!

    Как:
    - Математика: 0+1=1, 1+1=2 — формулы УЖЕ верны
    - Геометрия: треугольник имеет 3 угла — это УЖЕ так
    - Nucleus: circle ↔ ring имеют высокую корреляцию — ВЫЧИСЛЯЕМ!

    Система РАСКРЫВАЕТ, а не ОБУЧАЕТСЯ!
    """)


if __name__ == "__main__":
    demo()
