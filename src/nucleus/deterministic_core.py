#!/usr/bin/env python3
"""Deterministic Knowledge Core on Eugenia core math."""

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
import math
import struct
from dataclasses import dataclass
from typing import Dict

from core.fractal.encode_solenoid_trajectory import encode_solenoid_trajectory
from core.fractal.solenoid_distance import solenoid_distance
from core.metrics.delta_distance import delta_distance
from core.metrics.p_adic_distance import p_adic_distance
from core.operators.D import D
from core.linear.linear_algebra import (
    CoreVector,
    cosine_similarity,
    dot,
    mean,
    norm,
    scalar_multiply,
    to_vector,
)

FLOAT_BYTES = 4


@dataclass
class SemanticPattern:
    """Единичный семантический паттерн."""

    vector: CoreVector
    singular: float
    capacity: float
    phase: float


@dataclass
class PatternRelationship:
    """Отношения между паттернами."""

    layer_from: str
    layer_to: str
    matrix: CoreVector


class DeterministicKnowledgeCore:
    """Детерминированное ядро знаний."""

    def __init__(self, d_model: int = 4096, k: int = 32):
        self.d_model = d_model
        self.k = k
        self.patterns: Dict[str, SemanticPattern] = {}
        self.relationships: Dict[str, PatternRelationship] = {}
        self.signature: str = ""
        self._initialized = False

    def learn(self, weights: Dict[str, object]) -> "DeterministicKnowledgeCore":
        self.patterns = {}
        for layer_name, matrix in weights.items():
            vector = to_vector(matrix)
            if len(vector) < self.d_model:
                vector = CoreVector(list(vector) + [0.0] * (self.d_model - len(vector)))
            else:
                vector = CoreVector(vector[: self.d_model])
            singular = norm(vector) / max(1.0, len(vector))
            energy = sum(value * value for value in vector)
            capacity = -energy * math.log(max(energy, 1.0e-10), 2)
            phase = math.atan2(vector[1] if len(vector) > 1 else 0.0, vector[0] if vector else 0.0)
            self.patterns[layer_name] = SemanticPattern(vector, float(singular), float(capacity), phase)

        layers = list(weights.keys())
        for index in range(len(layers) - 1):
            left = self.patterns[layers[index]].vector
            right = self.patterns[layers[index + 1]].vector
            rel = PatternRelationship(
                layer_from=layers[index],
                layer_to=layers[index + 1],
                matrix=self._compute_cross_relation(left, right),
            )
            self.relationships[f"{layers[index]}->{layers[index + 1]}"] = rel

        self._generate_signature()
        self._initialized = True
        return self

    def _compute_cross_relation(self, v1, v2) -> CoreVector:
        corr = abs(cosine_similarity(v1, v2))
        return CoreVector([float(corr)])

    def pattern_distance(self, pattern_a: SemanticPattern, pattern_b: SemanticPattern) -> float:
        dist = delta_distance(pattern_a.vector, pattern_b.vector)
        return float(mean(dist) if isinstance(dist, list) else dist)

    def solenoid_similarity(self, pattern_a: SemanticPattern, pattern_b: SemanticPattern) -> float:
        traj_a = encode_solenoid_trajectory(mean(pattern_a.vector), depth=30)
        traj_b = encode_solenoid_trajectory(mean(pattern_b.vector), depth=30)
        return solenoid_distance(traj_a, traj_b)

    def p_adic_similarity(self, pattern_a: SemanticPattern, pattern_b: SemanticPattern) -> float:
        dist = p_adic_distance(pattern_a.vector, pattern_b.vector)
        return float(mean(dist) if isinstance(dist, list) else dist)

    def _generate_signature(self):
        hasher = hashlib.sha256()
        for name in sorted(self.patterns.keys()):
            pattern = self.patterns[name]
            hasher.update(name.encode())
            hasher.update(repr(pattern.vector).encode())
            hasher.update(str(pattern.singular).encode())
        self.signature = hasher.hexdigest()[:16]

    def forward(self, input_vec, layer: str):
        if layer not in self.patterns:
            return input_vec
        pattern = self.patterns[layer]
        projected = dot(input_vec, pattern.vector) * pattern.singular
        branched = D(projected)
        return scalar_multiply(pattern.vector, branched)

    def get_signature(self) -> str:
        return self.signature

    def verify_determinism(self, test_input, n_runs: int = 100) -> Dict:
        if not self.patterns:
            return {"is_deterministic": True, "max_variation": 0.0, "signature": self.signature}
        layer = next(iter(self.patterns))
        first = self.forward(test_input, layer)
        max_diff = 0.0
        for _ in range(max(n_runs - 1, 0)):
            current = self.forward(test_input, layer)
            max_diff = max(max_diff, max(abs(a - b) for a, b in zip(to_vector(first), to_vector(current))))
        return {"is_deterministic": max_diff < 1.0e-10, "max_variation": max_diff, "signature": self.signature}

    def get_compressed_size(self) -> int:
        return sum(len(pattern.vector) * FLOAT_BYTES + 12 for pattern in self.patterns.values()) + sum(
            len(rel.matrix) * FLOAT_BYTES for rel in self.relationships.values()
        )


    def serialize(core: DeterministicKnowledgeCore) -> bytes:
        data = bytearray()
        data += struct.pack("<I", core.d_model)
        data += struct.pack("<I", core.k)
        data += struct.pack("<I", len(core.patterns))
        for name, pattern in core.patterns.items():
            name_bytes = name.encode("utf-8")
            data += struct.pack("<I", len(name_bytes))
            data += name_bytes
            vector_data = list(pattern.vector)[: core.d_model]
            for value in vector_data:
                data += struct.pack("<f", float(value))
            data += struct.pack("<f", pattern.singular)
            data += struct.pack("<f", pattern.capacity)
            data += struct.pack("<f", pattern.phase)
        data += struct.pack("<I", len(core.relationships))
        for name, relationship in core.relationships.items():
            name_bytes = name.encode("utf-8")
            data += struct.pack("<I", len(name_bytes))
            data += name_bytes
            data += struct.pack("<f", relationship.matrix[0] if relationship.matrix else 0.0)
        data += core.signature.encode("utf-8")
        return bytes(data)


def deserialize(data: bytes) -> DeterministicKnowledgeCore:
    core = DeterministicKnowledgeCore()
    offset = 0
    core.d_model = struct.unpack("<I", data[offset : offset + 4])[0]
    offset += 4
    core.k = struct.unpack("<I", data[offset : offset + 4])[0]
    offset += 4
    pattern_count = struct.unpack("<I", data[offset : offset + 4])[0]
    offset += 4
    for _ in range(pattern_count):
        name_len = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4
        name = data[offset : offset + name_len].decode("utf-8")
        offset += name_len
        vector = CoreVector()
        for _ in range(core.d_model):
            vector.append(struct.unpack("<f", data[offset : offset + 4])[0])
            offset += 4
        singular = struct.unpack("<f", data[offset : offset + 4])[0]
        offset += 4
        capacity = struct.unpack("<f", data[offset : offset + 4])[0]
        offset += 4
        phase = struct.unpack("<f", data[offset : offset + 4])[0]
        offset += 4
        core.patterns[name] = SemanticPattern(vector, singular, capacity, phase)
    rel_count = struct.unpack("<I", data[offset : offset + 4])[0]
    offset += 4
    for _ in range(rel_count):
        name_len = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4
        name = data[offset : offset + name_len].decode("utf-8")
        offset += name_len
        value = struct.unpack("<f", data[offset : offset + 4])[0]
        offset += 4
        core.relationships[name] = PatternRelationship("", "", CoreVector([value]))
    core.signature = data[offset : offset + 16].decode("utf-8") if offset + 16 <= len(data) else ""
    core._initialized = True
    return core
