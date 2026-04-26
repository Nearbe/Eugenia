#!/usr/bin/env python3
"""Universal Geometric Classifier on Eugenia core math."""

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
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

from core.linear_algebra import CoreVector, cosine_similarity, euclidean_distance, linspace, mean, norm, std, to_vector

EPSILON = 1.0e-10
DEFAULT_RANDOM_SEED = 42


@dataclass
class GeometricProfile:
    """Геометрический профиль объекта."""

    binary_histogram: CoreVector
    jump_events: List[Tuple[float, float, float, float]]
    betti_signature: CoreVector
    capacity: float
    phase_signature: CoreVector


class GeometricExtractor:
    """Извлекает геометрические признаки из любых list-like данных."""

    def __init__(self, n_thresholds: int = 100, jump_threshold: float = 1.0):
        self.n_thresholds = n_thresholds
        self.jump_threshold = jump_threshold

    def extract(self, data) -> GeometricProfile:
        flat = to_vector(data)
        if not flat:
            flat = CoreVector([0.0])
        min_value = min(flat)
        max_value = max(flat)
        span = max_value - min_value
        if span > EPSILON:
            flat = CoreVector((value - min_value) / span for value in flat)
        else:
            flat = CoreVector(0.0 for _ in flat)

        thresholds = linspace(0.0, 1.0, self.n_thresholds)
        binary_profiles: list[float] = []
        for threshold in thresholds:
            density = sum(1 for value in flat if value > threshold) / len(flat)
            binary_profiles.append(density)
        binary_histogram = CoreVector(binary_profiles)

        jump_events: list[tuple[float, float, float, float]] = []
        for index in range(1, len(binary_histogram)):
            before = binary_histogram[index - 1]
            after = binary_histogram[index]
            jump = abs(after - before)
            if jump > self.jump_threshold / 100.0:
                jump_events.append((thresholds[index], before, after, jump))

        b0_list: list[float] = []
        b1_list: list[float] = []
        for threshold in thresholds:
            binary = [1 if value > threshold else 0 for value in flat]
            regions = self._count_regions_simplified(binary)
            b0_list.append(float(regions["betti0"]))
            b1_list.append(float(regions["betti1"]))
        betti_signature = CoreVector(b0_list + b1_list)

        total_abs = sum(abs(value) for value in flat)
        capacity = max(abs(value) for value in flat) / (total_abs + EPSILON) if flat else 0.0
        phase_signature = CoreVector(math.atan2(value, index + 1.0) for index, value in enumerate(flat[:10]))

        return GeometricProfile(
            binary_histogram=binary_histogram,
            jump_events=jump_events,
            betti_signature=betti_signature,
            capacity=float(capacity),
            phase_signature=phase_signature,
        )

    def _count_regions_simplified(self, binary) -> Dict[str, int]:
        flat_binary = list(binary)
        if not flat_binary:
            return {"betti0": 0, "betti1": 0}
        b0 = 1
        transitions = 0
        for index in range(1, len(flat_binary)):
            if flat_binary[index] != flat_binary[index - 1]:
                b0 += 1
                transitions += 1
        return {"betti0": min(b0, 100), "betti1": min(max(0, transitions // 100), 100)}


class UniversalGeometricClassifier:
    """Универсальный геометрический классификатор."""

    def __init__(self, n_thresholds: int = 100):
        self.extractor = GeometricExtractor(n_thresholds)
        self.class_profiles: Dict[int, GeometricProfile] = {}
        self.signature: str = ""

    def fit(self, X, y) -> "UniversalGeometricClassifier":
        labels = list(y)
        classes = sorted(set(int(label) for label in labels))
        samples = list(X)
        for cls in classes:
            for sample, label in zip(samples, labels):
                if int(label) == cls:
                    self.class_profiles[cls] = self.extractor.extract(sample)
                    break
        self._generate_signature()
        return self

    def _generate_signature(self):
        hasher = hashlib.sha256()
        for cls in sorted(self.class_profiles.keys()):
            profile = self.class_profiles[cls]
            hasher.update(repr(profile.binary_histogram).encode())
            hasher.update(str(profile.capacity).encode())
        self.signature = hasher.hexdigest()[:16]

    def predict(self, x) -> int:
        query_profile = self.extractor.extract(x)
        best_class: int | None = None
        best_score = -float("inf")
        for cls, profile in self.class_profiles.items():
            score = self._similarity(query_profile, profile)
            if score > best_score:
                best_score = score
                best_class = cls
        return int(best_class) if best_class is not None else -1

    def _similarity(self, p1: GeometricProfile, p2: GeometricProfile) -> float:
        corr = cosine_similarity(p1.binary_histogram, p2.binary_histogram)
        jump_sim = 1.0 - min(abs(len(p1.jump_events) - len(p2.jump_events)), 10) / 10.0
        betti_norm = norm(p1.betti_signature) + EPSILON
        betti_sim = 1.0 - euclidean_distance(p1.betti_signature, p2.betti_signature) / betti_norm
        cap_sim = 1.0 - abs(p1.capacity - p2.capacity) / (max(p1.capacity, p2.capacity) + EPSILON)
        return 0.4 * corr + 0.2 * jump_sim + 0.3 * betti_sim + 0.1 * cap_sim

    def get_compressed_size(self) -> int:
        size = 0
        for profile in self.class_profiles.values():
            size += profile.binary_histogram.nbytes
            size += profile.betti_signature.nbytes
            size += profile.phase_signature.nbytes
            size += 8
        return size


def test_mnist_classification():
    rng = random.Random(DEFAULT_RANDOM_SEED)
    samples = [[rng.random() for _ in range(28 * 28)] for _ in range(10)]
    labels = list(range(10))
    classifier = UniversalGeometricClassifier(n_thresholds=50).fit(samples, labels)
    print(classifier.predict(samples[0]))


def demonstrate_geometry_vision():
    print("The classifier compares geometry, not raw values.")


def real_world_applications():
    print("Few-shot classification, anomaly detection and semantic search.")


if __name__ == "__main__":
    test_mnist_classification()
    demonstrate_geometry_vision()
    real_world_applications()
