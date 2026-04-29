#!/usr/bin/env python3
"""Universal Knowledge System — Nucleus on Eugenia core math."""

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
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from core.dual.dual_pattern_transform import dual_pattern_transform
from core.fractal.fractal_pattern_signature import fractal_pattern_signature
from core.fractal.fractal_pyramid_structure import fractal_pyramid_structure
from core.fractal.pattern_bridge_identity import pattern_bridge_identity
from core.fractal.pattern_pyramid_depth import pattern_pyramid_depth
from core.fractal.pattern_spine_chain import pattern_spine_chain
from core.fractal.solenoid_encode_pattern import solenoid_encode_pattern
from core.fractal.solenoid_pattern_distance import solenoid_pattern_distance
from core.linear.linear_algebra import (
    CoreVector,
    cosine_similarity,
    linspace,
    mean,
    norm,
    std,
    to_vector,
)
from core.metrics.pattern_distance_from_delta import pattern_distance_from_delta
from core.operators.complex_delta_field import complex_delta_field
from core.operators.delta_field import delta_field
from nucleus.pattern_synthesizer import PatternSynthesizer, SynthesisResult

POTENTIAL_RANGE = 0.0
POTENTIAL_NORM = 0.0
MID_GRAY = 127.5
DELTA_MAX = 255.0
DEFAULT_PATTERN_LIMIT = 64
TOP_JUMP_PAD = 5
PYRAMID_FEATURES = 5
SPINE_FEATURES = 5


@dataclass
class PatternNode:
    """Узел паттерна — единица знаний."""

    node_id: str
    pattern: CoreVector
    singular: float
    correlations: Dict[str, float] = field(default_factory=dict)
    usage_count: int = 0
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
    solenoid: Optional[list[int]] = None
    fractal_sig: Optional[dict] = None
    pyramid: Optional[list[dict]] = None
    spine_chain: Optional[list[dict]] = None
    bridge: Optional[dict] = None


class GeometricExtractor:
    """Извлекает геометрические паттерны с RealMath/core интеграцией."""

    def __init__(self, n_thresholds: int = 64, solenoid_depth: int = 30, pyramid_levels: int = 10):
        self.n_thresholds = n_thresholds
        self.solenoid_depth = solenoid_depth
        self.pyramid_levels = pyramid_levels
        self._last_solenoid: list[int] = []
        self._last_fractal_sig: dict = {}
        self._last_pyramid: list[dict] = []
        self._last_spine_chain: list[dict] = []
        self._last_bridge: dict = {}
        self._last_pyramid_depth: float = 0.0

    def extract(self, data: Any) -> CoreVector:
        arr = self._normalize_to_delta_range(data)
        delta_field(arr)
        self._last_fractal_sig = fractal_pattern_signature(arr)
        self._last_solenoid = solenoid_encode_pattern(arr, self.solenoid_depth)

        complex_vals = complex_delta_field(arr)
        complex_real = [getattr(value, "real", 0.0) for value in complex_vals]
        complex_imag = [
            getattr(value, "imaginary", getattr(value, "imag", 0.0)) for value in complex_vals
        ]

        gradients = self._gradient(arr)
        form, velocity = dual_pattern_transform(arr, gradients)

        self._last_pyramid = fractal_pyramid_structure(self.pyramid_levels)
        self._last_spine_chain = pattern_spine_chain(self.pyramid_levels)
        avg_value = mean(arr)
        self._last_pyramid_depth = pattern_pyramid_depth(avg_value)
        self._last_bridge = pattern_bridge_identity(avg_value)

        top_jumps = list(self._last_fractal_sig.get("top_jumps", []))[:TOP_JUMP_PAD]
        top_jumps += [0.0] * (TOP_JUMP_PAD - len(top_jumps))

        pyramid_values = [
            self._last_pyramid[index]["bridge_analysis"]["left_spine_level"]
            if index < len(self._last_pyramid)
            else 0.0
            for index in range(PYRAMID_FEATURES)
        ]
        spine_values = [
            self._last_spine_chain[index]["spine_level"]
            if index < len(self._last_spine_chain)
            else 0.0
            for index in range(SPINE_FEATURES)
        ]

        components: list[float] = []
        components.extend(self._delta_sweep_profile(arr))
        components.extend(self._last_fractal_sig.get("profile", [])[: self.n_thresholds])
        components.extend(top_jumps)
        components.extend(
            [
                float(self._last_fractal_sig.get("fractal_dimension", 0.0)),
                float(self._last_fractal_sig.get("spine_level", 0.0)),
                float(self._last_fractal_sig.get("percentage", 0.0)),
                float(self._last_fractal_sig.get("avg_value", 0.0)),
            ]
        )
        components.extend(
            [mean(complex_real), std(complex_real), mean(complex_imag), std(complex_imag)]
        )
        components.extend([mean(form), std(form), mean(velocity), std(velocity)])
        components.extend(
            [
                sum(self._last_solenoid) / len(self._last_solenoid) if self._last_solenoid else 0.0,
                float(self._last_solenoid.count(1)) if self._last_solenoid else 0.0,
            ]
        )
        components.extend(pyramid_values)
        components.extend(spine_values)
        components.extend(
            [
                self._last_pyramid_depth,
                1.0 if self._last_bridge and self._last_bridge.get("bridge_identity") else 0.0,
            ]
        )
        return CoreVector(components)

    def _delta_sweep_profile(self, arr: list[float]) -> list[float]:
        thresholds = linspace(0.0, 1.0, self.n_thresholds)
        if not arr:
            return [0.0 for _ in thresholds]
        return [sum(1 for value in arr if value > threshold) / len(arr) for threshold in thresholds]

    def _normalize_to_delta_range(self, data: Any) -> list[float]:
        if isinstance(data, str):
            arr = [float(ord(char)) for char in data]
        else:
            arr = to_vector(data)
        if not arr:
            return [MID_GRAY]

        arr_min = min(arr)
        arr_max = max(arr)
        range_value = arr_max - arr_min
        if range_value == POTENTIAL_RANGE:
            return [MID_GRAY for _ in arr]
        return [(value - arr_min) / range_value * DELTA_MAX for value in arr]

    def _gradient(self, values: list[float]) -> list[float]:
        if len(values) < 2:
            return [0.0 for _ in values]
        result: list[float] = []
        for index, value in enumerate(values):
            if index == 0:
                result.append(values[1] - value)
            elif index == len(values) - 1:
                result.append(value - values[index - 1])
            else:
                result.append((values[index + 1] - values[index - 1]) / 2.0)
        return result

    def similarity(self, p1, p2) -> float:
        values_1 = to_vector(p1)
        values_2 = to_vector(p2)
        if not values_1 or not values_2:
            return 0.0
        if norm(values_1) == POTENTIAL_NORM or norm(values_2) == POTENTIAL_NORM:
            return 0.0

        limit = min(len(values_1), len(values_2), DEFAULT_PATTERN_LIMIT)
        score = cosine_similarity(values_1[:limit], values_2[:limit])
        return max(0.0, min(1.0, score))

    def distance(self, p1, p2) -> float:
        values_1 = to_vector(p1)
        values_2 = to_vector(p2)
        limit = min(len(values_1), len(values_2), DEFAULT_PATTERN_LIMIT)
        return pattern_distance_from_delta(values_1[:limit], values_2[:limit])

    def solenoid_distance(self, node_a: PatternNode, node_b: PatternNode) -> float:
        if node_a.solenoid and node_b.solenoid:
            return solenoid_pattern_distance(node_a.solenoid, node_b.solenoid)
        pattern_a = to_vector(node_a.pattern)[:DEFAULT_PATTERN_LIMIT]
        pattern_b = to_vector(node_b.pattern)[:DEFAULT_PATTERN_LIMIT]
        return solenoid_pattern_distance(pattern_a, pattern_b)


class KnowledgeSystem:
    """Система поглощения/связей паттернов."""

    def __init__(self, similarity_threshold: float = 0.7):
        self.extractor = GeometricExtractor()
        self.synthesizer = PatternSynthesizer()
        self.nodes: Dict[str, PatternNode] = {}
        self.similarity_threshold = similarity_threshold
        self._node_counter = 0

    def absorb(self, data: Any, label: Optional[str] = None) -> str:
        pattern = self.extractor.extract(data)
        singular = norm(pattern) / max(1.0, len(pattern))
        node_id = label or f"node_{self._node_counter}"
        self._node_counter += 1
        node = PatternNode(
            node_id=node_id,
            pattern=pattern,
            singular=singular,
            solenoid=self.extractor._last_solenoid,
            fractal_sig=self.extractor._last_fractal_sig,
            pyramid=self.extractor._last_pyramid,
            spine_chain=self.extractor._last_spine_chain,
            bridge=self.extractor._last_bridge,
        )
        self.nodes[node_id] = node
        self._auto_relate(node_id)
        return node_id

    def _auto_relate(self, node_id: str):
        new_node = self.nodes[node_id]
        for existing_id, existing_node in self.nodes.items():
            if existing_id == node_id:
                continue
            sim = self.extractor.similarity(new_node.pattern, existing_node.pattern)
            if sim > self.similarity_threshold:
                new_node.correlations[existing_id] = sim
                existing_node.correlations[node_id] = sim

    def relate(self, source_id: str, target_id: str, strength: float = 1.0):
        if source_id not in self.nodes or target_id not in self.nodes:
            return
        self.nodes[source_id].correlations[target_id] = strength
        self.nodes[target_id].correlations[source_id] = strength

    def strengthen(self, node_id: str):
        if node_id not in self.nodes:
            return
        node = self.nodes[node_id]
        node.usage_count += 1
        node.last_used = time.time()
        for related_id in list(node.correlations):
            if related_id in self.nodes:
                node.correlations[related_id] = min(1.0, node.correlations[related_id] * 1.05)

    def generate(
        self, context_node_id: str, max_nodes: int = 5, method: str = "retrieval"
    ) -> List[str]:
        """
        Generate new nodes via retrieval or synthesis.
        Returns a list of node IDs.
        """
        if context_node_id not in self.nodes:
            return []

        if method == "retrieval":
            related = sorted(
                self.nodes[context_node_id].correlations.items(),
                key=lambda item: item[1],
                reverse=True,
            )
            for node_id, _ in related[:max_nodes]:
                self.strengthen(node_id)
            return [node_id for node_id, _ in related[:max_nodes]]

        elif method == "synthesis":
            context_node = self.nodes[context_node_id]
            related_ids = [
                nid
                for nid, _ in sorted(
                    context_node.correlations.items(), key=lambda item: item[1], reverse=True
                )[:max_nodes]
            ]

            if not related_ids:
                res: SynthesisResult = self.synthesizer.evolve(
                    context_node.pattern, context_node.singular
                )
            else:
                related_patterns = [self.nodes[nid].pattern for nid in related_ids]
                related_velocities = [self.nodes[nid].singular for nid in related_ids]
                res: SynthesisResult = self.synthesizer.synthesize_from_set(
                    related_patterns, related_velocities, method="blending"
                )

            new_id = self.absorb(res.pattern.vector, label=f"synth_{context_node_id}_{res.method}")
            self.relate(new_id, context_node_id, res.velocity_magnitude)
            return [new_id]

        else:
            raise ValueError(f"Unknown generation method: {method}")

    def find_similar(self, data: Any, top_k: int = 3) -> List[Tuple[str, float]]:
        query_pattern = self.extractor.extract(data)
        similarities = [
            (node_id, self.extractor.similarity(query_pattern, node.pattern))
            for node_id, node in self.nodes.items()
        ]
        similarities.sort(key=lambda item: item[1], reverse=True)
        return similarities[:top_k]

    def query(self, data: Any) -> Dict[str, Any]:
        similar = self.find_similar(data, top_k=3)
        if not similar:
            node_id = self.absorb(data)
            return {"status": "new", "node_id": node_id, "similar": []}

        best_id, best_sim = similar[0]
        self.strengthen(best_id)
        if best_sim > 0.95:
            new_id = self.absorb(data)
            self.relate(new_id, best_id, best_sim)
        related = self.generate(best_id)
        return {
            "status": "existing",
            "best_match": best_id,
            "similarity": best_sim,
            "related": related,
        }

    def get_stats(self) -> Dict[str, Any]:
        total_correlations = sum(len(node.correlations) for node in self.nodes.values())
        most_used = (
            max(self.nodes.items(), key=lambda item: item[1].usage_count)[0] if self.nodes else None
        )
        return {
            "total_nodes": len(self.nodes),
            "total_correlations": total_correlations,
            "most_used_node": most_used,
            "most_used_count": self.nodes[most_used].usage_count if most_used else 0,
        }


def demo():
    system = KnowledgeSystem(similarity_threshold=0.5)
    for text in ["собака", "кошка", "кот"]:
        print(system.absorb(text, label=text))
    print(system.get_stats())


if __name__ == "__main__":
    demo()
