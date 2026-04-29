"""Extract deterministic geometric features from graph snapshots."""

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
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import networkx as nx

from core import safe_divide
from core.operators.D import D
from core.operators.gradient_magnitude import gradient_magnitude


DEFAULT_PRIME = 2
MIN_CURVATURE_SCALE = 1.0e-9
SIGMOID_MIDPOINT = 0.5
SIGMOID_SLOPE = 1.0


@dataclass(frozen=True)
class GeometricFeatures:
    """Deterministic feature vector for a concept graph."""

    curvature: float
    delta_score: float
    s_curve_score: float
    gradient: float
    resistance: float
    threshold_count: int

    def as_vector(self) -> list[float]:
        """Return a stable numeric representation suitable for comparisons."""

        return [
            self.curvature,
            self.delta_score,
            self.s_curve_score,
            self.gradient,
            self.resistance,
            float(self.threshold_count),
        ]


class GeometricExtractor:
    """Build graph-level features using only deterministic core operators."""

    def extract(self, graph: nx.Graph, *, prime: int = DEFAULT_PRIME) -> GeometricFeatures:
        """Compute deterministic geometric features for ``graph``."""

        node_count = graph.number_of_nodes()
        edge_count = graph.number_of_edges()

        if node_count == 0:
            return GeometricFeatures(0.0, 0.0, 0.0, 0.0, 0.0, 0)

        density = nx.density(graph) if node_count > 1 else 0.0
        curvature = self._curvature(graph)
        delta_score = float(D(safe_divide(edge_count + 1, max(node_count, 1))))
        s_curve_score = self._s_curve(density)
        gradient = gradient_magnitude(curvature, density)
        resistance = self._average_path_resistance(graph)
        threshold_count = self._threshold_count(
            (curvature, density, delta_score, s_curve_score), prime=prime
        )

        return GeometricFeatures(
            curvature=curvature,
            delta_score=delta_score,
            s_curve_score=s_curve_score,
            gradient=gradient,
            resistance=resistance,
            threshold_count=threshold_count,
        )

    def distance(self, left: GeometricFeatures, right: GeometricFeatures) -> float:
        """Return Euclidean distance between two feature vectors."""

        squared_distance = sum(
            (left_value - right_value) ** 2
            for left_value, right_value in zip(left.as_vector(), right.as_vector(), strict=True)
        )
        return math.sqrt(squared_distance)

    def combine(self, *features: GeometricFeatures) -> GeometricFeatures:
        """Average multiple feature vectors into one representative feature set."""

        if not features:
            return GeometricFeatures(0.0, 0.0, 0.0, 0.0, 0.0, 0)

        total = len(features)
        threshold_count = round(sum(feature.threshold_count for feature in features) / total)
        return GeometricFeatures(
            curvature=sum(feature.curvature for feature in features) / total,
            delta_score=sum(feature.delta_score for feature in features) / total,
            s_curve_score=sum(feature.s_curve_score for feature in features) / total,
            gradient=sum(feature.gradient for feature in features) / total,
            resistance=sum(feature.resistance for feature in features) / total,
            threshold_count=threshold_count,
        )

    def _curvature(self, graph: nx.Graph) -> float:
        if graph.number_of_nodes() <= 1:
            return 0.0

        clustering = nx.average_clustering(graph) if graph.number_of_edges() else 0.0
        density = nx.density(graph)
        return self._sigmoid(clustering - density, scale=max(abs(density), MIN_CURVATURE_SCALE))

    def _average_path_resistance(self, graph: nx.Graph) -> float:
        if graph.number_of_nodes() <= 1:
            return 0.0

        values: list[float] = []
        components = nx.connected_components(graph) if not graph.is_directed() else nx.weakly_connected_components(graph)
        for component in components:
            subgraph = graph.subgraph(component)
            nodes = list(subgraph.nodes)
            for index, source in enumerate(nodes):
                for target in nodes[index + 1 :]:
                    path = nx.shortest_path(subgraph, source, target)
                    weights = [
                        self._edge_weight(subgraph, path[position], path[position + 1])
                        for position in range(len(path) - 1)
                    ]
                    values.append(self._path_resistance(weights))

        if not values:
            return 0.0
        return sum(values) / len(values)

    @staticmethod
    def _edge_weight(graph: nx.Graph, source: Any, target: Any) -> float:
        data = graph.get_edge_data(source, target, default={})
        if isinstance(data, dict) and "weight" in data:
            return float(data["weight"])
        return 1.0

    @staticmethod
    def _path_resistance(weights: list[float]) -> float:
        if not weights:
            return 0.0
        return sum(safe_divide(1.0, max(abs(weight), MIN_CURVATURE_SCALE)) for weight in weights)

    @staticmethod
    def _s_curve(value: float) -> float:
        return 1.0 / (1.0 + math.exp(-(value - SIGMOID_MIDPOINT) / SIGMOID_SLOPE))

    @staticmethod
    def _sigmoid(value: float, *, scale: float) -> float:
        return 1.0 / (1.0 + math.exp(-safe_divide(value, scale)))
