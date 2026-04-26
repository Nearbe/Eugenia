#!/usr/bin/env python3
"""Knowledge graph compression on Eugenia core math."""

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
import random

from core.delta_distance import delta_distance
from core.encode_solenoid_trajectory import encode_solenoid_trajectory
from core.linear_algebra import CoreMatrix, CoreVector, cosine_similarity, mean, to_matrix
from core.p_adic_distance import p_adic_distance
from core.solenoid_distance import solenoid_distance
from nucleus.cross_layer_compressor import compress_layer

DEFAULT_RANDOM_SEED = 42


class KnowledgeGraph:
    """Представление знаний модели как графа корреляций."""

    def __init__(self):
        self.nodes = None
        self.edges = None
        self.embeddings = None

    def build_from_weights(self, W, k=32):
        layer = compress_layer(W, k)
        self.embeddings = {
            "left": layer["U"],
            "singular": layer["S"],
            "right": layer["Vt"],
        }
        return self.embeddings

    def get_node_vector(self, idx):
        if self.embeddings is None:
            return CoreVector()
        left = to_matrix(self.embeddings["left"])
        singular = CoreVector(self.embeddings["singular"])
        if not left:
            return CoreVector()
        row = left[idx % len(left)]
        return CoreVector(value * singular[col] for col, value in enumerate(row))

    def similarity(self, i, j):
        v1 = self.get_node_vector(i)
        v2 = self.get_node_vector(j)
        cos_sim = cosine_similarity(v1, v2)

        delta_dist = delta_distance(v1, v2)
        if isinstance(delta_dist, list):
            delta_dist = mean(delta_dist)

        p_adic_dist = p_adic_distance(v1, v2)
        if isinstance(p_adic_dist, list):
            p_adic_dist = mean(p_adic_dist)

        traj1 = encode_solenoid_trajectory(mean(v1), depth=30)
        traj2 = encode_solenoid_trajectory(mean(v2), depth=30)
        sol_dist = solenoid_distance(traj1, traj2)
        return float(0.5 * cos_sim + 0.3 * (1.0 / (1.0 + delta_dist)) + 0.2 * sol_dist)


def extract_knowledge_structure():
    rng = random.Random(DEFAULT_RANDOM_SEED)
    matrix = CoreMatrix([[rng.gauss(0.0, 0.1) for _ in range(32)] for _ in range(32)])
    graph = KnowledgeGraph()
    graph.build_from_weights(matrix, k=8)
    print(graph.similarity(0, 1))


def knowledge_retrieval():
    print("Retrieval uses graph node vectors from core math.")


def memory_efficient_inference():
    print("Inference can reconstruct only requested core patterns.")


if __name__ == "__main__":
    extract_knowledge_structure()
    knowledge_retrieval()
    memory_efficient_inference()
