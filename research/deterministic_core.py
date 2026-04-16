#!/usr/bin/env python3
"""
Deterministic Knowledge Core — Final System
=======================================

ЭТО КЛЮЧ КО ВСЕМУ:

1. ПАТТЕРНЫ = детерминированные представления знаний
2. СВЯЗИ = детерминированные правила обработки
3. FORWARD = детерминированная функция

Из RealMath:
- L(M) = глубина структуры (информация)
- D(a) = создаёт различия между состояниями
- Ω = потенциал, реализуемый через паттерны

Принцип:
- Вместо хаотичных весов — детерминированные PATТЕРНЫ
- Вместо статичных значений — детерминированные СВЯЗИ
- Модель = детерминированная ФУНКЦИЯ паттернов
"""

import numpy as np
import struct
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import hashlib

from core.division import normalize_vector_safe, div_safe


# ============================================================
# Core Data Structures
# ============================================================


@dataclass
class SemanticPattern:
    """One semantic pattern — deterministic representation."""

    vector: np.ndarray  # (d_model,) eigenvector
    singular: float  # singular value = importance
    capacity: float  # information capacity
    phase: float  # orientation


@dataclass
class PatternRelationship:
    """Отношения между паттернами — детерминированные"""

    layer_from: str
    layer_to: str
    matrix: np.ndarray  # (k, k) relationship matrix


# ============================================================
# Main System Class
# ============================================================


class DeterministicKnowledgeCore:
    """
    ГЛАВНЫЙ КЛАСС: Детерминированное ядро знаний

    API:
    1. learn(weight_dict) → извлекает детерминированные паттерны
    2. forward(input) → детерминированный forward pass
    3. get_signature() → уникальная подпись
    4. verify() → проверяет детерминизм

    Storage:
    - 111GB → ~0.5-1GB (через k control)
    - Паттерны + Связи (не веса)
    """

    def __init__(self, d_model: int = 4096, k: int = 32):
        self.d_model = d_model
        self.k = k
        self.patterns: Dict[str, SemanticPattern] = {}
        self.relationships: Dict[str, PatternRelationship] = {}
        self.signature: str = ""
        self._initialized = False

    def learn(self, weights: Dict[str, np.ndarray]) -> "DeterministicKnowledgeCore":
        """
        MAIN METHOD: Извлечение детерминированных паттернов

        Вызывается ОДИН раз при создании ядра
        """
        self.patterns = {}

        # Extract patterns from each weight matrix
        for layer_name, W in weights.items():
            # SVD — детерминированная операция
            U, S, Vt = np.linalg.svd(W, full_matrices=False)

            # Top-k patterns
            with np.errstate(divide="ignore", invalid="ignore"):
                log_S2 = np.log(S**2)
                log_S2 = np.where(np.isneginf(log_S2), 0.0, log_S2)

            pattern = SemanticPattern(
                vector=U[:, : self.k].flatten()[: self.d_model],  # First d_model values
                singular=float(S[0]),  # Most important singular value
                entropy=float(-np.sum((S**2) * log_S2)),
                phase=float(np.angle(U[0, 0] + 1j * U[1, 0])),
            )
            self.patterns[layer_name] = pattern

        # Build relationships between layers
        layers = list(weights.keys())
        for i in range(len(layers) - 1):
            rel = PatternRelationship(
                layer_from=layers[i],
                layer_to=layers[i + 1],
                matrix=self._compute_cross_relation(
                    self.patterns[layers[i]].vector,
                    self.patterns[layers[i + 1]].vector,
                ),
            )
            self.relationships[f"{layers[i]}->{layers[i + 1]}"] = rel

        # Generate deterministic signature
        self._generate_signature()
        self._initialized = True

        return self

    def _compute_cross_relation(self, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        """Cross-correlation — deterministic operation."""
        v1_norm = normalize_vector_safe(v1)
        v2_norm = normalize_vector_safe(v2)

        corr = np.abs(np.dot(v1_norm, v2_norm))

        return np.array([corr], dtype=np.float32)

    def _generate_signature(self):
        """Генерирует детерминированную подпись"""
        # Хешируем все паттерны
        hasher = hashlib.sha256()

        for name in sorted(self.patterns.keys()):
            p = self.patterns[name]
            hasher.update(p.vector.tobytes())
            hasher.update(str(p.singular).encode())

        self.signature = hasher.hexdigest()[:16]

    def forward(self, input_vec: np.ndarray, layer: str) -> np.ndarray:
        """
        Детерминированный forward pass

        Всегда возвращает ОДИН результат для того же входа
        """
        if layer not in self.patterns:
            return input_vec

        p = self.patterns[layer]

        # Project through pattern
        projected = np.dot(input_vec, p.vector) * p.singular

        # Reconstruct (simplified)
        output = p.vector * projected

        return output

    def get_signature(self) -> str:
        """Возвращает подпись — уникальный идентификатор"""
        return self.signature

    def verify_determinism(self, test_input: np.ndarray, n_runs: int = 100) -> Dict:
        """Проверяет детерминизм множеством запусков"""
        outputs = []

        for _ in range(n_runs):
            # Use first available layer for testing
            layer = list(self.patterns.keys())[0]
            out = self.forward(test_input, layer)
            outputs.append(out.copy())

        # Check all equal
        max_diff = 0.0
        for i in range(1, n_runs):
            diff = np.max(np.abs(outputs[i] - outputs[0]))
            max_diff = max(max_diff, diff)

        return {
            "is_deterministic": max_diff < 1e-10,
            "max_variation": max_diff,
            "signature": self.signature,
        }

    def get_compressed_size(self) -> int:
        """Размер сжатого представления"""
        size = 0
        for p in self.patterns.values():
            size += p.vector.nbytes
            size += 4 + 4 + 4  # singular, entropy, phase
        for r in self.relationships.values():
            size += r.matrix.nbytes
        return size


# ============================================================
# Storage Format
# ============================================================


def serialize(core: DeterministicKnowledgeCore) -> bytes:
    """Сериализация в бинарный формат"""
    data = b""

    # Header
    data += struct.pack("<I", core.d_model)
    data += struct.pack("<I", core.k)

    # Patterns
    data += struct.pack("<I", len(core.patterns))

    for name, p in core.patterns.items():
        name_bytes = name.encode("utf-8")
        data += struct.pack("<I", len(name_bytes))
        data += name_bytes
        data += p.vector.tobytes()
        data += struct.pack("<f", p.singular)
        data += struct.pack("<f", p.entropy)
        data += struct.pack("<f", p.phase)

    # Relationships
    data += struct.pack("<I", len(core.relationships))

    for name, r in core.relationships.items():
        name_bytes = name.encode("utf-8")
        data += struct.pack("<I", len(name_bytes))
        data += name_bytes
        data += r.matrix.tobytes()

    # Signature
    data += core.signature.encode("utf-8")

    return data


def deserialize(data: bytes) -> DeterministicKnowledgeCore:
    """Десериализация"""
    core = DeterministicKnowledgeCore()

    offset = 0
    core.d_model = struct.unpack("<I", data[offset : offset + 4])[0]
    offset += 4
    core.k = struct.unpack("<I", data[offset : offset + 4])[0]
    offset += 4

    n_patterns = struct.unpack("<I", data[offset : offset + 4])[0]
    offset += 4

    for _ in range(n_patterns):
        name_len = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4
        name = data[offset : offset + name_len].decode("utf-8")
        offset += name_len

        vector = np.frombuffer(data[offset : offset + core.d_model * 2], dtype=np.float16).astype(
            np.float32
        )
        offset += core.d_model * 2

        singular = struct.unpack("<f", data[offset : offset + 4])[0]
        offset += 4
        entropy = struct.unpack("<f", data[offset : offset + 4])[0]
        offset += 4
        phase = struct.unpack("<f", data[offset : offset + 4])[0]
        offset += 4

        core.patterns[name] = SemanticPattern(vector, singular, entropy, phase)

    n_rels = struct.unpack("<I", data[offset : offset + 4])[0]
    offset += 4

    for _ in range(n_rels):
        name_len = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4
        name = data[offset : offset + name_len].decode("utf-8")
        offset += name_len

        matrix = np.frombuffer(data[offset : offset + 4], dtype=np.float32)
        offset += 4

        core.relationships[name] = PatternRelationship("", "", matrix)

    core.signature = data[offset : offset + 16].decode("utf-8")
    offset += 16
    core._initialized = True

    return core
