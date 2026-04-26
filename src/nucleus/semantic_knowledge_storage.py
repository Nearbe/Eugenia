#!/usr/bin/env python3
"""Semantic Knowledge Storage System on Eugenia core math."""

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
import random
import struct
from dataclasses import dataclass
from typing import Dict, List, Tuple

from core.linear_algebra import (
    CoreMatrix,
    CoreVector,
    cosine_similarity,
    dot,
    mean,
    norm,
    outer,
    scalar_multiply,
    to_vector,
    zeros,
)
from nucleus.cross_layer_compressor import compress_layer

DEFAULT_RANDOM_SEED = 42
FLOAT_BYTES = 4


class SemanticOperators:
    """Семантические D/H/L операторы."""

    @staticmethod
    def D_pattern(pattern) -> CoreVector:
        vector = CoreVector(to_vector(pattern))
        return CoreVector(list(vector) + list(vector))

    @staticmethod
    def H_pattern(pattern, target_len: int) -> CoreVector:
        vector = CoreVector(to_vector(pattern))
        if len(vector) <= target_len:
            return vector
        block = max(1, len(vector) // target_len)
        return CoreVector(mean(vector[index * block : (index + 1) * block]) for index in range(target_len))

    @staticmethod
    def L_pattern(pattern) -> float:
        energy = sum(value * value for value in to_vector(pattern))
        return math.log(max(energy, 1.0e-10), 2)


@dataclass
class EigenPattern:
    """Один eigenpattern — главный семантический паттерн."""

    vector: CoreVector
    singular_value: float
    phase: float
    capacity: float


class SemanticPatternExtractor:
    """Извлекает семантические паттерны из весов модели."""

    def __init__(self, k_patterns: int = 32):
        self.k = k_patterns
        self.patterns: List[EigenPattern] = []
        self.relationships: CoreMatrix | None = None

    def extract_from_weights(self, W) -> List[EigenPattern]:
        layer = compress_layer(W, self.k)
        left = layer["U"]
        singular = CoreVector(layer["S"])
        patterns: list[EigenPattern] = []
        for index in range(min(self.k, len(singular))):
            vector = CoreVector(row[index] if index < len(row) else 0.0 for row in left)
            phase = math.atan2(vector[1] if len(vector) > 1 else 0.0, vector[0] if vector else 0.0)
            patterns.append(
                EigenPattern(
                    vector=vector,
                    singular_value=float(singular[index]),
                    phase=phase,
                    capacity=self._compute_capacity(vector),
                )
            )
        self.patterns = patterns
        return patterns

    def _compute_capacity(self, vector) -> float:
        values = [abs(value) ** 2 for value in to_vector(vector)]
        total = sum(values) + 1.0e-10
        probabilities = [value / total + 1.0e-10 for value in values]
        return -sum(prob * math.log(prob) for prob in probabilities)

    def extract_relationships(self) -> CoreMatrix:
        if not self.patterns:
            self.relationships = CoreMatrix()
            return self.relationships
        size = len(self.patterns)
        rows = []
        for i in range(size):
            rows.append([cosine_similarity(self.patterns[i].vector, self.patterns[j].vector) for j in range(size)])
        self.relationships = CoreMatrix(rows)
        return self.relationships

    def get_compressed_size(self) -> int:
        size = 0
        for pattern in self.patterns:
            size += pattern.vector.nbytes + 12
        if self.relationships is not None:
            size += self.relationships.nbytes
        return size


class KnowledgeGraph:
    """Граф знаний модели."""

    def __init__(self):
        self.nodes: List[EigenPattern] = []
        self.edges: CoreMatrix | None = None
        self.layer_index: Dict[str, int] = {}

    def build_from_model(self, model_weights: Dict[str, object], k: int = 32):
        all_patterns: list[EigenPattern] = []
        all_relationship_rows: list[list[float]] = []
        for layer_name, weights in model_weights.items():
            extractor = SemanticPatternExtractor(k)
            patterns = extractor.extract_from_weights(weights)
            relationships = extractor.extract_relationships()
            self.layer_index[layer_name] = len(all_patterns)
            all_patterns.extend(patterns)
            all_relationship_rows.extend(relationships)
        self.nodes = all_patterns
        self.edges = CoreMatrix(all_relationship_rows)
        return self

    def semantic_similarity(self, pattern_a: int, pattern_b: int) -> float:
        if pattern_b >= len(self.nodes) or pattern_a >= len(self.nodes):
            return 0.0
        return cosine_similarity(self.nodes[pattern_a].vector, self.nodes[pattern_b].vector)

    def find_related_patterns(self, pattern_idx: int, top_k: int = 5) -> List[Tuple[int, float]]:
        if self.edges is None or pattern_idx >= len(self.edges):
            return []
        similarities = self.edges[pattern_idx]
        ranked = sorted(range(len(similarities)), key=lambda index: abs(similarities[index]), reverse=True)
        return [(index, similarities[index]) for index in ranked[:top_k]]

    def get_knowledge_structure(self) -> Dict:
        edge_count = self.edges.size if self.edges is not None else 0
        return {
            "n_patterns": len(self.nodes),
            "n_relationships": edge_count,
            "total_capacity": sum(pattern.capacity for pattern in self.nodes),
            "layers": list(self.layer_index.keys()),
        }


class SemanticRetrieval:
    """Семантический поиск в модели."""

    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.graph = knowledge_graph

    def search_by_vector(self, query, top_k: int = 5) -> List[Tuple[int, float, float]]:
        scores = []
        query_vector = CoreVector(to_vector(query))
        for index, pattern in enumerate(self.graph.nodes):
            score = cosine_similarity(query_vector, pattern.vector)
            final_score = score * math.log(pattern.singular_value + 1.0)
            scores.append((index, final_score, pattern.capacity))
        scores.sort(key=lambda item: item[1], reverse=True)
        return scores[:top_k]

    def search_by_layer(self, layer_name: str, top_k: int = 5) -> List[int]:
        if layer_name not in self.graph.layer_index:
            return []
        start_idx = self.graph.layer_index[layer_name]
        return list(range(start_idx, min(start_idx + top_k, len(self.graph.nodes))))

    def semantic_expand(self, pattern_idx: int) -> List[int]:
        return [index for index, _ in self.graph.find_related_patterns(pattern_idx, top_k=10)]


class RuntimeReconstructor:
    """Восстановление весов из паттернов для inference."""

    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.graph = knowledge_graph

    def reconstruct_layer(self, layer_name: str, d_model: int, d_out: int) -> CoreMatrix:
        if layer_name not in self.graph.layer_index:
            return zeros(d_model, d_out)
        start_idx = self.graph.layer_index[layer_name]
        layer_count = max(len(self.graph.layer_index), 1)
        k = max(1, len(self.graph.nodes) // layer_count)
        result = zeros(d_model, d_out)
        for index in range(k):
            pattern_idx = start_idx + index
            if pattern_idx >= len(self.graph.nodes):
                break
            pattern = self.graph.nodes[pattern_idx]
            product = outer(pattern.vector[:d_model], pattern.vector[:d_out])
            scaled = scalar_multiply(product, pattern.singular_value)
            result = CoreMatrix(
                [[left + right for left, right in zip(row_a, row_b)] for row_a, row_b in zip(result, scaled)]
            )
        return result

    def efficient_forward(self, layer_name: str, x) -> CoreVector:
        start_idx = self.graph.layer_index.get(layer_name, 0)
        result = CoreVector(0.0 for _ in to_vector(x))
        for pattern in self.graph.nodes[start_idx : start_idx + 32]:
            activation = dot(x, pattern.vector) * pattern.singular_value
            contribution = scalar_multiply(pattern.vector, activation)
            result = CoreVector(left + right for left, right in zip(result, contribution))
        return result


class SemanticStorageFormat:
    """Компактный бинарный формат семантических знаний."""

    @staticmethod
    def serialize(graph: KnowledgeGraph) -> bytes:
        data = bytearray()
        data += struct.pack("<I", len(graph.nodes))
        for pattern in graph.nodes:
            data += struct.pack("<I", len(pattern.vector))
            data += struct.pack("<f", pattern.singular_value)
            data += struct.pack("<f", pattern.phase)
            data += struct.pack("<f", pattern.capacity)
            for value in pattern.vector:
                data += struct.pack("<f", float(value))
        rows, cols = graph.edges.shape if graph.edges is not None else (0, 0)
        data += struct.pack("<II", rows, cols)
        if graph.edges is not None:
            for row in graph.edges:
                for value in row:
                    data += struct.pack("<f", float(value))
        data += struct.pack("<I", len(graph.layer_index))
        for layer, index in graph.layer_index.items():
            raw = layer.encode("utf-8")
            data += struct.pack("<I", len(raw))
            data += raw
            data += struct.pack("<I", index)
        return bytes(data)

    @staticmethod
    def deserialize(data: bytes) -> KnowledgeGraph:
        graph = KnowledgeGraph()
        offset = 0
        pattern_count = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4
        for _ in range(pattern_count):
            vector_len = struct.unpack("<I", data[offset : offset + 4])[0]
            offset += 4
            singular = struct.unpack("<f", data[offset : offset + 4])[0]
            offset += 4
            phase = struct.unpack("<f", data[offset : offset + 4])[0]
            offset += 4
            capacity = struct.unpack("<f", data[offset : offset + 4])[0]
            offset += 4
            vector = CoreVector()
            for _ in range(vector_len):
                vector.append(struct.unpack("<f", data[offset : offset + 4])[0])
                offset += 4
            graph.nodes.append(EigenPattern(vector, singular, phase, capacity))
        rows, cols = struct.unpack("<II", data[offset : offset + 8])
        offset += 8
        edge_rows = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(struct.unpack("<f", data[offset : offset + 4])[0])
                offset += 4
            edge_rows.append(row)
        graph.edges = CoreMatrix(edge_rows)
        layer_count = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4
        for _ in range(layer_count):
            layer_len = struct.unpack("<I", data[offset : offset + 4])[0]
            offset += 4
            layer = data[offset : offset + layer_len].decode("utf-8")
            offset += layer_len
            index = struct.unpack("<I", data[offset : offset + 4])[0]
            offset += 4
            graph.layer_index[layer] = index
        return graph


def test_semantic_system():
    rng = random.Random(DEFAULT_RANDOM_SEED)
    weights = {"attn_q": CoreMatrix([[rng.gauss(0.0, 1.0) for _ in range(32)] for _ in range(32)])}
    graph = KnowledgeGraph().build_from_model(weights, k=8)
    print(graph.get_knowledge_structure())


if __name__ == "__main__":
    test_semantic_system()
