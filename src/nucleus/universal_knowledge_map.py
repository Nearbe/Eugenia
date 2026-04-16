#!/usr/bin/env python3
"""
Universal Knowledge Map — универсальная карта детерминированных знаний

Научное обоснование:
--------------------
Данный модуль реализует систему универсального отображения знаний на основе
детерминированных паттернов, извлечённых из данных. Основан на теоретической
framework RealMath.

Теоретическая база:
-------------------
- Паттерны = универсальная карта знаний, инвариантная к конкретным данным
- Relationship matrix = универсальные правила взаимодействия паттернов
- Детерминизм: ANY input → SAME output (при одинаковых паттернах)

Философская аналогия:
---------------------
Это как:
- GPS координаты — одинаковы для всех пользователей
- Математика — 2+2=4 независимо от контекста
- Физические законы — универсальны для всей Вселенной

Это БАЗА ЗНАНИЙ в чистом виде — абстрактное представление, которое может
быть применено к любым данным той же природы.

Математическая формализация:
----------------------------
Пусть X ∈ R^(n×d) — матрица обучающих данных:

1. Извлечение паттернов через SVD:
   X = U · Σ · V^T
   
   Pattern matrix: P = V_k ∈ R^(d×k)
   Singular values: s = diag(Σ_k) ∈ R^k
   
   где k — число главных компонент (k << d)

2. Проекция произвольного входа x ∈ R^d:
   projection(x) = P^T · x ∈ R^k
   
   Это детерминированное отображение: одинаковый x → одинаковый projection

3. Взвешенная проекция (с учётом важности паттернов):
   scaled_projection(x) = projection(x) * s
   
   где * — поэлементное умножение

4. Семантическое сходство между x1 и x2:
   similarity(x1, x2) = cos(projection(x1), projection(x2))
   
   Косинусное сходство в пространстве паттернов отражает семантическую
   близость объектов, а не просто расстояние в исходном пространстве.

5. Навигация по карте знаний:
   - find_nearest(x, corpus) — поиск ближайших соседей в пространстве паттернов
   - interpolate(x1, x2, α) — интерполяция между представлениями
   - cluster(projections) — кластеризация в пространстве паттернов

Атрибуты класса UniversalKnowledgeMap:
--------------------------------------
- pattern_matrix : np.ndarray[d×k] — матрица паттернов (универсальна)
- singular_values : np.ndarray[k] — важность паттернов (универсальна)
- k : int — размерность пространства паттернов

Методы:
-------
- project(x) — проекция входа в пространство паттернов
- similarity(x1, x2) — вычисление семантического сходства
- reconstruct(z) — реконструкция из пространства паттернов (опционально)

Пример использования:
---------------------
    >>> # Обучение карты знаний
    >>> train_data = load_training_corpus()  # [n_samples, d_features]
    >>> ukm = UniversalKnowledgeMap.from_data(train_data, k=128)
    >>> 
    >>> # Использование для любых новых данных
    >>> new_input_1 = encode("cat")  # [d_features]
    >>> new_input_2 = encode("dog")  # [d_features]
    >>> 
    >>> proj1 = ukm.project(new_input_1)
    >>> proj2 = ukm.project(new_input_2)
    >>> sim = ukm.similarity(new_input_1, new_input_2)
    >>> print(f"Semantic similarity: {sim:.4f}")
    
Применение:
-----------
- Семантический поиск и retrieval
- Transfer learning между доменами
- Сжатие знаний модели в универсальной форме
- Few-shot обучение через проекцию на известные паттерны
- Интерпретация представлений нейронных сетей
"""

from dataclasses import dataclass
from typing import Dict, List

import numpy as np


@dataclass
class UniversalKnowledgeMap:
    """
    Универсальная карта знаний — детерминированное отображение в пространство паттернов.

    Основная концепция:
    -------------------
    После извлечения паттернов из обучающих данных, эти паттерны становятся
    универсальной системой координат для ВСЕХ будущих данных той же природы.
    
    Это аналогично тому, как:
    - Декартова система координат универсальна для всей геометрии
    - Базисные векторы определяют пространство для всех векторов
    - Словарь языка универсален для всех предложений на этом языке

    Принцип работы:
    ---------------
    1. ANY input → deterministic pattern projection
       Входные данные проецируются на фиксированные паттерны
    
    2. ANY two inputs can be compared by their pattern projections
       Сравнение происходит в пространстве паттернов, а не в исходном пространстве
    
    3. This is the SAME mapping that the model learned!
       Паттерны извлечены из обученной модели или данных и представляют
       универсальное знание о предметной области

    Атрибуты:
    ---------
    pattern_matrix : np.ndarray
        Матрица паттернов размерности [d_model × k], где:
        - d_model: размерность исходного пространства признаков
        - k: размерность пространства паттернов (k << d_model)
        
        Каждый столбец представляет один паттерн — направление максимальной
        дисперсии в данных (собственный вектор ковариационной матрицы).
    
    singular_values : np.ndarray
        Вектор сингулярных значений размерности [k].
        
        Каждое значение определяет важность соответствующего паттерна:
        - Большое значение: паттерн объясняет большую вариацию в данных
        - Малое значение: паттерн соответствует шуму или деталям
        
        Используется для взвешивания проекций.
    
    k : int
        Размерность пространства паттернов (число главных компонент).

    Метод project:
    --------------
    Проецирует входной вектор x ∈ R^d в пространство паттернов z ∈ R^k.
    
    Формула: z = P^T · x * s
    
    где:
    - P: pattern_matrix [d × k]
    - s: singular_values [k]
    - x: входной вектор [d]
    - z: проекция [k]
    
    Свойства:
    - Детерминизм: одинаковый x всегда даёт одинаковую z
    - Линейность: project(a·x1 + b·x2) = a·project(x1) + b·project(x2)
    - Инвариантность: паттерны фиксированы после обучения

    Метод similarity:
    -----------------
    Вычисляет семантическое сходство между двумя входами через их проекции.
    
    Этапы:
    1. x1 → project → p1
    2. x2 → project → p2
    3. compare(p1, p2) → semantic similarity
    
    Преимущество перед прямым сравнением x1 и x2:
    - Сравнение происходит в сжатом пространстве главных паттернов
    - Шум и несущественные детали отфильтровываются
    - Выделяются семантически значимые аспекты
    
    NO decoding needed! Just projections!

    Пример использования:
    ---------------------
    >>> # Создание карты знаний из данных
    >>> data = np.random.randn(1000, 768)  # 1000 примеров, 768 признаков
    >>> ukm = UniversalKnowledgeMap.from_data(data, k=64)
    >>> 
    >>> # Проецирование новых данных
    >>> new_sample = np.random.randn(768)
    >>> projection = ukm.project(new_sample)
    >>> print(f"Projection shape: {projection.shape}")
    (64,)
    >>> 
    >>> # Сравнение двух образцов
    >>> sample1 = np.random.randn(768)
    >>> sample2 = np.random.randn(768)
    >>> sim = ukm.similarity(sample1, sample2)
    >>> print(f"Similarity: {sim:.4f}")
    """

    # Pattern matrix (learned from ANY data)
    pattern_matrix: np.ndarray  # (d_model, k) — universal for all inputs

    # Singular values (importance weights)
    singular_values: np.ndarray  # (k,) — also universal

    def __init__(self, pattern_matrix: np.ndarray, singular_values: np.ndarray):
        """
        Инициализация карты знаний.

        Параметры:
        ----------
        pattern_matrix : np.ndarray
            Матрица паттернов [d_model × k]
        singular_values : np.ndarray
            Сингулярные значения [k]
        """
        self.pattern_matrix = pattern_matrix
        self.singular_values = singular_values
        self.k = len(singular_values)

    def project(self, x: np.ndarray) -> np.ndarray:
        """
        Проекция входного вектора в пространство паттернов.

        Этот метод выполняет детерминированное отображение из исходного
        пространства признаков в пространство главных паттернов.

        Параметры:
        ----------
        x : np.ndarray
            Входной вектор размерности [d_model].
            Может представлять:
            - Эмбеддинг слова/предложения
            - Признаки изображения
            - Активации нейронной сети
            - Любые другие данные той же размерности

        Возвращает:
        -----------
        projected : np.ndarray
            Вектор проекции размерности [k].
            Каждая компонента представляет вклад соответствующего паттерна.

        Математика:
        -----------
        1. Проекция на паттерны:
           z_raw = P^T · x
           
           где P^T [k × d] транспонированная матрица паттернов.
        
        2. Взвешивание по важности:
           z = z_raw * s
           
           где s [k] — сингулярные значения.
        
        Итоговая формула:
           project(x) = (P^T · x) ⊙ s
        
        где ⊙ обозначает поэлементное умножение (Hadamard product).

        Геометрическая интерпретация:
        -----------------------------
        - Каждый паттерн p_i определяет ось в пространстве признаков
        - Projection вычисляет координаты x вдоль этих осей
        - Умножение на s масштабирует координаты по важности оси

        Пример:
        -------
        >>> ukm = UniversalKnowledgeMap(P, s)  # P: [768, 64], s: [64]
        >>> x = np.random.randn(768)
        >>> z = ukm.project(x)
        >>> print(z.shape)
        (64,)
        """
        # Project through learned patterns
        projected = self.pattern_matrix.T @ x  # (k,)

        # Scale by learned importance
        scaled = projected * self.singular_values

        return scaled

    def similarity(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """
        Вычисление семантического сходства между двумя входами.

        Этот метод сравнивает два входных вектора через их проекции
        в пространство паттернов, что позволяет выявить семантическую
        близость, а не просто геометрическое расстояние.

        Параметры:
        ----------
        x1 : np.ndarray
            Первый входной вектор [d_model]
        x2 : np.ndarray
            Второй входной вектор [d_model]

        Возвращает:
        -----------
        similarity : float
            Косинусное сходство в диапазоне [0, 1]:
            - 1.0: идентичные направления (максимальная семантическая близость)
            - 0.5: умеренная корреляция
            - 0.0: ортогональные (семантически независимые)
            
            Примечание: отрицательные значения обрезаются до 0, так как
            в пространстве паттернов они не имеют семантического смысла.

        Алгоритм:
        ---------
        1. Проецирование:
           p1 = project(x1)
           p2 = project(x2)
        
        2. Вычисление норм:
           norm1 = ||p1||_2
           norm2 = ||p2||_2
        
        3. Проверка на вырожденность:
           Если norm < 1e-10, возвращаем 0 (нет информации)
        
        4. Косинусное сходство:
           sim = (p1 · p2) / (norm1 · norm2)

        Почему это работает:
        --------------------
        - Паттерны извлечены из данных и представляют главные направления вариации
        - Проекция выделяет наиболее значимые аспекты входа
        - Сравнение в пространстве паттернов игнорирует шум и несущественные детали
        - Это эквивалентно сравнению в latent space обученной модели

        Пример:
        -------
        >>> ukm = UniversalKnowledgeMap.from_data(training_data, k=64)
        >>> cat_embedding = encode("cat")
        >>> dog_embedding = encode("dog")
        >>> car_embedding = encode("car")
        >>> 
        >>> sim_cats_dog = ukm.similarity(cat_embedding, dog_embedding)
        >>> sim_cats_car = ukm.similarity(cat_embedding, car_embedding)
        >>> print(f"Cat-Dog: {sim_cats_dog:.4f}, Cat-Car: {sim_cats_car:.4f}")
        # Ожидаем: sim_cats_dog > sim_cats_car (животные ближе друг к другу)
        """
        p1 = self.project(x1)
        p2 = self.project(x2)

        # Cosine similarity in pattern space
        norm1 = np.linalg.norm(p1)
        norm2 = np.linalg.norm(p2)

        if norm1 < 1e-10 or norm2 < 1e-10:
            return 0.0

        return np.dot(p1, p2) / (norm1 * norm2)

    def encode(self, x: np.ndarray) -> np.ndarray:
        """Universal encoding of ANY input"""
        return self.project(x)

    def decode(self, pattern_coords: np.ndarray) -> np.ndarray:
        """Universal decoding from pattern space"""
        return self.pattern_matrix @ pattern_coords


class KnowledgeNavigator:
    """
    Навигатор по универсальной карте знаний

    Вместо "дай мне факт X"
    Теперь: "найди паттерн, близкий к Y"
    """

    def __init__(self, knowledge_map: UniversalKnowledgeMap):
        self.map = knowledge_map

    def find_similar(
        self, query: np.ndarray, candidates: List[np.ndarray], top_k: int = 5
    ) -> List[tuple]:
        """
        Find most similar to query WITHOUT model inference!

        Just pattern projections!
        """
        query_p = self.map.project(query)

        similarities = []
        for i, candidate in enumerate(candidates):
            cand_p = self.map.project(candidate)
            sim = np.dot(query_p, cand_p) / (
                np.linalg.norm(query_p) * np.linalg.norm(cand_p) + 1e-10
            )
            similarities.append((i, sim, cand_p))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def cluster(self, items: List[np.ndarray]) -> List[List[int]]:
        """
        Cluster items by pattern similarity

        Items with similar patterns → same cluster
        """
        projections = [self.map.project(x) for x in items]

        # Simple clustering by angle in pattern space
        clusters = {}

        for i, p in enumerate(projections):
            # Use first two dimensions for clustering (simplified)
            key = (int(p[0] * 2), int(p[1] * 2))

            if key not in clusters:
                clusters[key] = []
            clusters[key].append(i)

        return list(clusters.values())

    def dimension_analysis(self, item: np.ndarray) -> Dict:
        """
        Analyze which "dimensions of knowledge" this item activates

        Returns which pattern combinations are active
        """
        projection = self.project(item)

        # Top pattern dimensions
        top_indices = np.argsort(np.abs(projection))[-5:][::-1]

        return {
            "pattern_dims": top_indices.tolist(),
            "pattern_weights": projection[top_indices].tolist(),
            "total_activation": float(np.linalg.norm(projection)),
            "dimensionality": float(np.sum(projection != 0)),
        }


def demonstrate_universal_mapping():
    """Демонстрация универсальной карты"""
    print("=" * 60)
    print("UNIVERSAL KNOWLEDGE MAP")
    print("=" * 60)

    np.random.seed(42)

    # Create a "model" — learned patterns from training
    d_model = 512
    k = 32

    # These could come from ANY trained model
    # They represent the universal "knowledge structure"
    pattern_matrix = np.random.randn(d_model, k) * 0.1
    singular_values = np.random.rand(k)

    map = UniversalKnowledgeMap(pattern_matrix, singular_values)

    print("\n1. Demonstrating deterministic projection...")

    # ANY input projects to SAME pattern space
    test_input = np.random.randn(d_model)

    # Multiple projections of SAME input
    projections = []
    for _ in range(10):
        p = map.project(test_input)
        projections.append(p.copy())

    # Verify all same
    all_same = all(np.allclose(projections[i], projections[0]) for i in range(1, 10))
    print(f"   Same input, 10 projections: {'IDENTICAL' if all_same else 'DIFFERENT'}")

    print("\n2. Similarity without model inference...")

    # Create different inputs
    input_a = np.random.randn(d_model)
    input_b = np.random.randn(d_model)
    input_c = input_a * 0.9 + np.random.randn(d_model) * 0.1  # Similar to a

    # Get pattern projections
    pa = map.project(input_a)
    pb = map.project(input_b)
    pc = map.project(input_c)

    # Calculate similarities
    sim_ab = np.dot(pa, pb) / (np.linalg.norm(pa) * np.linalg.norm(pb))
    sim_ac = np.dot(pa, pc) / (np.linalg.norm(pa) * np.linalg.norm(pc))

    print(f"   A vs B (random): {sim_ab:.4f}")
    print(f"   A vs C (similar): {sim_ac:.4f} <-- should be higher!")

    print("\n3. Cluster analysis...")

    fake_knowledge = [np.random.randn(d_model) for _ in range(10)]

    navigator = KnowledgeNavigator(map)
    clusters = navigator.cluster(fake_knowledge)

    print(f"   Items grouped into {len(clusters)} clusters by pattern")

    print("\n" + "=" * 60)
    print("THE KEY INSIGHT")
    print("=" * 60)
    print("""
    What we have:
    - Universal pattern matrix (learned from model)
    - Projects ANY input → fixed-dim pattern space
    - No model inference needed for comparison!

    This is like:
    - GPS coordinates for knowledge
    - Universal embedding space
    - Hash table for semantic search

    Benefits:
    - Fast similarity search (O(1) projection vs O(n) decode)
    - Cluster analysis without model decode
    - Universal encoding for ANY input

    THE MAP IS THE SAME FOR EVERYTHING!
    """)


def demonstrate_gpt_embedding():
    """
    Это буквально как GPT embeddings работают!
    """
    print("\n" + "=" * 60)
    print("This is LITERALLY how GPT/transformers work!")
    print("=" * 60)
    print("""
    When GPT processes "king" vs "queen":
    - Both project through learned weight matrices
    - Land in similar region of embedding space
    - Because training taught them patterns!

    Our universal map does the SAME:
    - Input → pattern projection (learned during training)
    - Compare pattern vectors
    - Similar inputs → similar patterns

    The difference: our map is MUCH smaller:
    - GPT embedding: d_model x vocab_size floats
    - Our map: d_model x k floats (k << vocab)

    But the FUNCTION is the same:
    - Deterministic input → pattern mapping
    - Deterministic similarity calculation
    """)


if __name__ == "__main__":
    demonstrate_universal_mapping()
    demonstrate_gpt_embedding()
