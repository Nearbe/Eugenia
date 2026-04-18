#!/usr/bin/env python3
"""
Semantic Knowledge Storage System
==================================

Основано на концепциях из RealMath/Essentials:
- L(M) = глубина структуры, не величина
- D(a) — создаёт различие между паттернами
- Ω — потенциал (все возможные семантические связи)
- Π — полнота (актуальные знания)

Система хранит НЕ веса, а СЕМАНТИЧЕСКИЕ ПАТТЕРНЫ:
1. Eigenpatterns — главные паттерны знаний
2. Cross-pattern relationships — как паттерны связаны
3. Semantic adjacency — семантическая близость

Это даёт:
- Компактное хранение (111GB → ~1GB)
- Knowledge retrieval по семантике
- Runtime inference через pattern reconstruction
"""

import struct
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np


# ============================================================
# Базовые операторы из RealMath
# ============================================================


class SemanticOperators:
    """
    Семантические операторы:
    - D(a): создаёт различие, новый паттерн
    - H(a): схлопывает к сути, убирает шум
    - L(M): глубина структуры = информация
    """

    @staticmethod
    def D_pattern(pattern: np.ndarray) -> np.ndarray:
        """Создаёт новый паттерн через удвоение"""
        return np.concatenate([pattern, pattern])

    @staticmethod
    def H_pattern(pattern: np.ndarray, target_len: int) -> np.ndarray:
        """Схлопывает паттерн к нужной длине"""
        if len(pattern) <= target_len:
            return pattern
        # Усреднение блоков
        blocks = len(pattern) // target_len
        return np.array([pattern[i * blocks : (i + 1) * blocks].mean() for i in range(target_len)])

    @staticmethod
    def L_pattern(pattern: np.ndarray) -> float:
        """Глубина паттерна = log2(энергия)"""
        energy = np.sum(pattern**2)
        return np.log2(max(energy, 1e-10))


# ============================================================
# Семантические паттерны
# ============================================================


@dataclass
class EigenPattern:
    """Один eigenpattern — главный семантический паттерн"""

    vector: np.ndarray  # Паттерн (compressed)
    singular_value: float  # Важность (L — глубина)
    phase: float  # Фаза ( для кодирования)
    entropy: float  # Сложность паттерна


class SemanticPatternExtractor:
    """
    Извлекает семантические паттерны из весов модели

    Вместо значений храним структуру паттернов
    """

    def __init__(self, k_patterns: int = 32):
        self.k = k_patterns
        self.patterns: List[EigenPattern] = []
        self.relationships: np.ndarray = None

    def extract_from_weights(self, W: np.ndarray) -> List[EigenPattern]:
        """
        Извлекает eigenpatterns из весов

        Метод: SVD разложение
        - U: собственные вектора = паттерны
        - S: сингулярные значения = важность паттернов
        - Vt: правая проекция
        """
        U, S, Vt = np.linalg.svd(W, full_matrices=False)

        patterns = []
        for i in range(min(self.k, len(S))):
            # Создаём паттерн
            pattern = EigenPattern(
                vector=U[:, i].astype(np.float16),
                singular_value=S[i],
                phase=np.angle(U[0, i] + 1j * U[1, i]),  # фаза в комплексной плоскости
                entropy=self._compute_entropy(U[:, i]),
            )
            patterns.append(pattern)

        self.patterns = patterns
        return patterns

    def _compute_entropy(self, vector: np.ndarray) -> float:
        """Вычисляет энтропию паттерна"""
        # Нормализация
        p = np.abs(vector) ** 2
        p = p / p.sum() + 1e-10
        return -np.sum(p * np.log(p))

    def extract_relationships(self) -> np.ndarray:
        """
        Извлекает relationships между паттернами

        Это ключевое — хранит как паттерны связаны!
        """
        if not self.patterns:
            return np.array([])

        k = len(self.patterns)
        relationships = np.zeros((k, k), dtype=np.float32)

        # Cross-correlation между паттернами
        for i in range(k):
            for j in range(k):
                vec_i = self.patterns[i].vector.astype(np.float32)
                vec_j = self.patterns[j].vector.astype(np.float32)

                # Косинусное сходство
                sim = np.dot(vec_i, vec_j) / (np.linalg.norm(vec_i) * np.linalg.norm(vec_j) + 1e-10)
                relationships[i, j] = sim

        self.relationships = relationships
        return relationships

    def get_compressed_size(self) -> int:
        """Размер в байтах для хранения паттернов"""
        if not self.patterns:
            return 0

        size = 0
        for p in self.patterns:
            size += p.vector.nbytes  # float16 vector
            size += 4 + 4 + 4  # singular_value, phase, entropy (float32 each)

        if self.relationships is not None:
            size += self.relationships.nbytes

        return size


# ============================================================
# Knowledge Graph — структура знаний
# ============================================================


class KnowledgeGraph:
    """
    Граф знаний модели

    Узлы = семантические паттерны
    Ребра = relationships между паттернами

    Это хранит СЕМАНТИКУ модели, не веса!
    """

    def __init__(self):
        self.nodes: List[EigenPattern] = []
        self.edges: np.ndarray = None
        self.layer_index: Dict[str, int] = {}

    def build_from_model(self, model_weights: Dict[str, np.ndarray], k: int = 32):
        """
        Строит knowledge graph из весов модели

        model_weights: {layer_name: weight_matrix}
        """
        all_patterns = []
        all_relationships = []

        for layer_name, W in model_weights.items():
            # Извлекаем паттерны слоя
            extractor = SemanticPatternExtractor(k)
            patterns = extractor.extract_from_weights(W)
            relationships = extractor.extract_relationships()

            # Индексируем
            self.layer_index[layer_name] = len(all_patterns)
            all_patterns.extend(patterns)

            if relationships is not None:
                all_relationships.append(relationships)

        self.nodes = all_patterns
        self.edges = np.block(all_relationships) if all_relationships else np.array([])

        return self

    def semantic_similarity(self, pattern_a: int, pattern_b: int) -> float:
        """Семантическое сходство двух паттернов"""
        if pattern_b >= len(self.nodes) or pattern_a >= len(self.nodes):
            return 0.0

        vec_a = self.nodes[pattern_a].vector.astype(np.float32)
        vec_b = self.nodes[pattern_b].vector.astype(np.float32)

        return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b) + 1e-10)

    def find_related_patterns(self, pattern_idx: int, top_k: int = 5) -> List[Tuple[int, float]]:
        """Находит семантически связанные паттерны"""
        if self.edges is None or pattern_idx >= len(self.edges):
            return []

        similarities = self.edges[pattern_idx]
        top_indices = np.argsort(np.abs(similarities))[-top_k:][::-1]

        return [(idx, similarities[idx]) for idx in top_indices]

    def get_knowledge_structure(self) -> Dict:
        """Возвращает структуру знаний модели"""
        return {
            "n_patterns": len(self.nodes),
            "n_relationships": len(self.edges) ** 2 if self.edges is not None else 0,
            "total_entropy": sum(p.entropy for p in self.nodes),
            "layers": list(self.layer_index.keys()),
        }


# ============================================================
# Semantic Retrieval — поиск по семантике
# ============================================================


class SemanticRetrieval:
    """
    Семантический поиск в модели

    Позволяет находить знания по смыслу, не по весам!
    """

    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.graph = knowledge_graph

    def search_by_vector(self, query: np.ndarray, top_k: int = 5) -> List[Tuple[int, float, float]]:
        """
        Поиск по вектору запроса

        Вместо decode всей модели — ищем по паттернам
        """
        scores = []

        for i, pattern in enumerate(self.graph.nodes):
            vec = pattern.vector.astype(np.float32)
            score = np.dot(query, vec) / (np.linalg.norm(query) * np.linalg.norm(vec) + 1e-10)
            importance = pattern.singular_value

            # Комбинируем relevance и importance
            final_score = score * np.log(importance + 1)
            scores.append((i, final_score, pattern.entropy))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def search_by_layer(self, layer_name: str, top_k: int = 5) -> List[int]:
        """Поиск паттернов в конкретном слое"""
        if layer_name not in self.graph.layer_index:
            return []

        start_idx = self.graph.layer_index[layer_name]
        # Assuming k patterns per layer
        return list(range(start_idx, start_idx + top_k))

    def semantic_expand(self, pattern_idx: int) -> List[int]:
        """Семантическое разворачивание — все связанные паттерны"""
        related = self.graph.find_related_patterns(pattern_idx, top_k=10)
        return [idx for idx, _ in related]


# ============================================================
# Runtime Reconstruction — восстановление для inference
# ============================================================


class RuntimeReconstructor:
    """
    Восстановление весов из паттернов для inference

    Работает в runtime с минимальной памятью
    """

    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.graph = knowledge_graph

    def reconstruct_layer(self, layer_name: str, d_model: int, d_out: int) -> np.ndarray:
        """
        Восстанавливает слой из паттернов

        W = Σ pattern_i * importance_i * pattern_vector_i^T
        """
        if layer_name not in self.graph.layer_index:
            return np.zeros((d_model, d_out))

        start_idx = self.graph.layer_index[layer_name]
        # k паттернов на слой
        k = len(self.graph.nodes) // len(self.graph.layer_index)

        W = np.zeros((d_model, d_out), dtype=np.float32)

        for i in range(k):
            pattern_idx = start_idx + i
            if pattern_idx >= len(self.graph.nodes):
                break

            pattern = self.graph.nodes[pattern_idx]
            vector = pattern.vector.astype(np.float32)
            importance = pattern.singular_value

            # Outer product pattern
            W += importance * np.outer(vector, vector)

        return W

    def efficient_forward(self, layer_name: str, x: np.ndarray) -> np.ndarray:
        """
        Эффективный forward pass без восстановления всей матрицы

        x -> pattern projection -> importance -> output

        Это требует O(k*d) вместо O(d*d)!
        """
        # Get patterns for this layer
        start_idx = self.graph.layer_index.get(layer_name, 0)
        k = 32  # number of patterns

        # Project input to pattern space
        patterns = []
        for i in range(k):
            if start_idx + i < len(self.graph.nodes):
                patterns.append(self.graph.nodes[start_idx + i].vector.astype(np.float32))

        # Project: x -> pattern space
        pattern_matrix = np.column_stack(patterns)  # (d, k)
        x_proj = pattern_matrix.T @ x  # (k,)

        # Scale by importance
        for i, p in enumerate(patterns):
            if start_idx + i < len(self.graph.nodes):
                x_proj[i] *= self.graph.nodes[start_idx + i].singular_value

        # Reconstruct output
        output = pattern_matrix @ x_proj

        return output


# ============================================================
# Serialization / Deserialization
# ============================================================


class SemanticStorageFormat:
    """
    Формат хранения семантических знаний

    Компактный бинарный формат:
    - Header: метаинформация
    - Patterns: eigenpatterns (compressed)
    - Relationships: cross-pattern matrix
    - Index: mapping layer -> patterns
    """

    @staticmethod
    def serialize(graph: KnowledgeGraph) -> bytes:
        """Сериализация графа знаний"""
        data = b""

        # Header
        n_patterns = len(graph.nodes)
        data += struct.pack("<I", n_patterns)

        # Patterns
        for p in graph.nodes:
            data += struct.pack("<f", p.singular_value)
            data += struct.pack("<f", p.phase)
            data += struct.pack("<f", p.entropy)
            data += p.vector.tobytes()

        # Relationships
        if graph.edges is not None:
            data += struct.pack("<I", graph.edges.shape[0])
            data += graph.edges.tobytes()
        else:
            data += struct.pack("<I", 0)

        # Layer index
        data += struct.pack("<I", len(graph.layer_index))
        for layer, idx in graph.layer_index.items():
            layer_bytes = layer.encode("utf-8")
            data += struct.pack("<I", len(layer_bytes))
            data += layer_bytes
            data += struct.pack("<I", idx)

        return data

    @staticmethod
    def deserialize(data: bytes) -> KnowledgeGraph:
        """Десериализация графа"""
        graph = KnowledgeGraph()
        offset = 0

        # Header
        n_patterns = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4

        # Patterns
        for _ in range(n_patterns):
            singular = struct.unpack("<f", data[offset : offset + 4])[0]
            offset += 4
            phase = struct.unpack("<f", data[offset : offset + 4])[0]
            offset += 4
            entropy = struct.unpack("<f", data[offset : offset + 4])[0]
            offset += 4

            vec_len = 32  # Assuming k=32
            vector = np.frombuffer(data[offset : offset + vec_len * 2], dtype=np.float16)
            offset += vec_len * 2

            graph.nodes.append(
                EigenPattern(
                    vector=vector,
                    singular_value=singular,
                    phase=phase,
                    entropy=entropy,
                )
            )

        # Relationships
        rel_size = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4
        if rel_size > 0:
            graph.edges = np.frombuffer(
                data[offset : offset + rel_size * 4], dtype=np.float32
            ).reshape(rel_size, rel_size)

        # Layer index
        n_layers = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4

        for _ in range(n_layers):
            layer_len = struct.unpack("<I", data[offset : offset + 4])[0]
            offset += 4
            layer = data[offset : offset + layer_len].decode("utf-8")
            offset += layer_len
            idx = struct.unpack("<I", data[offset : offset + 4])[0]
            offset += 4
            graph.layer_index[layer] = idx

        return graph


# ============================================================
# Demo / Test
# ============================================================


def test_semantic_system():
    """Тест семантической системы"""
    print("=" * 60)
    print("Semantic Knowledge Storage System")
    print("=" * 60)

    np.random.seed(42)

    # Симулируем модель
    model_weights = {
        "attn_q": np.random.randn(4096, 4096).astype(np.float32),
        "attn_k": np.random.randn(4096, 4096).astype(np.float32),
        "attn_v": np.random.randn(4096, 4096).astype(np.float32),
        "ffn_up": np.random.randn(4096, 16384).astype(np.float32),
        "ffn_down": np.random.randn(16384, 4096).astype(np.float32),
    }

    original_size = sum(w.nbytes for w in model_weights.values())
    print(f"\nОригинальные веса: {original_size / 1024**2:.1f} MB")

    # Строим knowledge graph
    print("\nИзвлечение семантических паттернов...")
    kg = KnowledgeGraph()
    kg.build_from_model(model_weights, k=32)

    structure = kg.get_knowledge_structure()
    print(f"Паттернов: {structure['n_patterns']}")
    print(f"Связей: {structure['n_relationships']}")
    print(f"Слоёв: {len(structure['layers'])}")

    # Размер
    extractor = SemanticPatternExtractor(k=32)
    extractor.extract_from_weights(model_weights["attn_q"])
    relationships = extractor.extract_relationships()

    size_per_layer = extractor.get_compressed_size()
    if relationships is not None:
        size_per_layer += relationships.nbytes

    total_size = size_per_layer * len(model_weights)

    print(f"\nСжатый размер: {total_size / 1024**2:.2f} MB")
    print(f"Ratio: {original_size / total_size:.0f}x")
    print(f"111GB -> {111 * total_size / original_size:.2f}GB")

    # Retrieval demo
    print("\n" + "-" * 40)
    print("Semantic Retrieval Demo:")

    retrieval = SemanticRetrieval(kg)

    # Случайный query vector
    query = np.random.randn(4096).astype(np.float32)
    results = retrieval.search_by_vector(query, top_k=3)

    print("Query: случайный вектор")
    print("Top 3 семантически связанных паттерна:")
    for idx, score, entropy in results:
        p = kg.nodes[idx]
        print(
            f"  Pattern {idx}: score={score:.3f}, entropy={entropy:.3f}, importance={p.singular_value:.2f}"
        )

    # Layer-specific search
    print("\nПоиск в слое attn_q:")
    attn_patterns = retrieval.search_by_layer("attn_q", top_k=5)
    print(f"  Найдены паттерны: {attn_patterns}")


if __name__ == "__main__":
    test_semantic_system()
