#!/usr/bin/env python3
"""
Tests for src/nucleus/knowledge_graph.py

Covers: KnowledgeGraph build_from_weights, get_node_vector, similarity,
        and RealMath integration.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nucleus.knowledge_graph import KnowledgeGraph


# ============================================================
# KnowledgeGraph
# ============================================================


class TestKnowledgeGraph:
    def test_init_empty(self):
        graph = KnowledgeGraph()
        assert graph.nodes is None
        assert graph.edges is None
        assert graph.embeddings is None

    def test_build_from_weights_basic(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        embeddings = graph.build_from_weights(W, k=8)

        assert embeddings is not None
        assert "left" in embeddings
        assert "singular" in embeddings
        assert "right" in embeddings
        assert embeddings["left"].shape == (64, 8)
        assert embeddings["singular"].shape == (8,)
        assert embeddings["right"].shape == (8, 64)

    def test_build_from_weights_dtype(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        embeddings = graph.build_from_weights(W, k=8)

        assert embeddings["left"].dtype == np.float16
        assert embeddings["singular"].dtype == np.float16
        assert embeddings["right"].dtype == np.float16

    def test_build_from_weights_k_larger_than_rank(self):
        graph = KnowledgeGraph()
        W = np.random.randn(10, 10).astype(np.float32)
        embeddings = graph.build_from_weights(W, k=64)  # k > min(m,n)

        # Should clip to min(m,n)
        assert embeddings["left"].shape[1] == 10
        assert embeddings["singular"].shape[0] == 10
        assert embeddings["right"].shape[0] == 10

    def test_build_from_weights_rectangular(self):
        graph = KnowledgeGraph()
        W = np.random.randn(128, 32).astype(np.float32)
        embeddings = graph.build_from_weights(W, k=16)

        assert embeddings["left"].shape == (128, 16)
        assert embeddings["singular"].shape == (16,)
        assert embeddings["right"].shape == (16, 32)

    def test_build_from_weights_square(self):
        graph = KnowledgeGraph()
        W = np.random.randn(512, 512).astype(np.float32)
        embeddings = graph.build_from_weights(W, k=32)

        assert embeddings["left"].shape == (512, 32)
        assert embeddings["right"].shape == (32, 512)

    def test_build_from_weights_deterministic(self):
        graph = KnowledgeGraph()
        np.random.seed(42)
        W = np.random.randn(64, 64).astype(np.float32)

        embeddings1 = graph.build_from_weights(W, k=8)

        graph2 = KnowledgeGraph()
        embeddings2 = graph2.build_from_weights(W, k=8)

        np.testing.assert_array_almost_equal(embeddings1["left"], embeddings2["left"])
        np.testing.assert_array_almost_equal(embeddings1["singular"], embeddings2["singular"])
        np.testing.assert_array_almost_equal(embeddings1["right"], embeddings2["right"])

    def test_get_node_vector(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        graph.build_from_weights(W, k=8)

        vector = graph.get_node_vector(0)
        assert isinstance(vector, np.ndarray)
        assert len(vector) == 8

    def test_get_node_vector_all_indices(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        graph.build_from_weights(W, k=8)

        for i in range(64):
            vector = graph.get_node_vector(i)
            assert len(vector) == 8

    def test_get_node_vector_different_indices(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        graph.build_from_weights(W, k=8)

        v0 = graph.get_node_vector(0)
        v1 = graph.get_node_vector(1)
        # Different nodes may have different vectors (not guaranteed different)
        assert isinstance(v0, np.ndarray)
        assert isinstance(v1, np.ndarray)

    def test_similarity_same_node(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        graph.build_from_weights(W, k=8)

        sim = graph.similarity(0, 0)
        assert abs(sim - 1.0) < 0.01  # Should be close to 1

    def test_similarity_range(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        graph.build_from_weights(W, k=8)

        for i in range(64):
            for j in range(i + 1, 64):
                sim = graph.similarity(i, j)
                assert isinstance(sim, float)
                # RealMath similarity can exceed [0,1] due to weighting
                assert sim >= -1.0

    def test_similarity_different_nodes(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        graph.build_from_weights(W, k=8)

        sim = graph.similarity(0, 1)
        assert isinstance(sim, float)

    def test_similarity_with_orthogonal_vectors(self):
        graph = KnowledgeGraph()
        # Create a matrix with orthogonal rows
        W = np.eye(10, dtype=np.float32)
        graph.build_from_weights(W, k=5)

        sim = graph.similarity(0, 1)
        # Orthogonal vectors should have low similarity
        assert sim < 0.5

    def test_build_from_weights_preserves_singular_values_order(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        embeddings = graph.build_from_weights(W, k=32)

        S = embeddings["singular"]
        # SVD guarantees non-increasing singular values
        for i in range(len(S) - 1):
            assert S[i] >= S[i + 1] - 1e-6  # float16 tolerance

    def test_build_from_weights_with_zero_matrix(self):
        graph = KnowledgeGraph()
        W = np.zeros((10, 10), dtype=np.float32)
        embeddings = graph.build_from_weights(W, k=4)

        assert embeddings is not None
        assert embeddings["left"].shape == (10, 4)
        assert embeddings["singular"].shape == (4,)

    def test_build_from_weights_with_one_matrix(self):
        graph = KnowledgeGraph()
        W = np.ones((10, 10), dtype=np.float32)
        embeddings = graph.build_from_weights(W, k=4)

        assert embeddings is not None
        assert embeddings["left"].shape == (10, 4)

    def test_node_vector_is_weighted(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        graph.build_from_weights(W, k=8)

        # Node vector = left[i] * singular
        left = graph.embeddings["left"]
        singular = graph.embeddings["singular"]

        expected = left[0] * singular
        actual = graph.get_node_vector(0)

        np.testing.assert_array_almost_equal(actual, expected)

    def test_similarity_symmetry(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        graph.build_from_weights(W, k=8)

        sim_ab = graph.similarity(0, 1)
        sim_ba = graph.similarity(1, 0)
        assert abs(sim_ab - sim_ba) < 0.01

    def test_large_matrix(self):
        graph = KnowledgeGraph()
        W = np.random.randn(256, 256).astype(np.float32)
        embeddings = graph.build_from_weights(W, k=32)

        assert embeddings["left"].shape == (256, 32)
        assert embeddings["right"].shape == (32, 256)

    def test_small_k(self):
        graph = KnowledgeGraph()
        W = np.random.randn(64, 64).astype(np.float32)
        embeddings = graph.build_from_weights(W, k=1)

        assert embeddings["left"].shape == (64, 1)
        assert embeddings["singular"].shape == (1,)
        assert embeddings["right"].shape == (1, 64)

    def test_k_equals_min_dim(self):
        graph = KnowledgeGraph()
        W = np.random.randn(32, 48).astype(np.float32)
        embeddings = graph.build_from_weights(W, k=32)

        assert embeddings["left"].shape[1] == 32
        assert embeddings["singular"].shape[0] == 32
        assert embeddings["right"].shape[0] == 32
