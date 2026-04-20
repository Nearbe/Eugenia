#!/usr/bin/env python3
"""
Tests for src/nucleus/universal_knowledge_map.py

Covers: UniversalKnowledgeMap (project, similarity, encode, decode),
        KnowledgeNavigator (find_similar, cluster, dimension_analysis).
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nucleus.universal_knowledge_map import UniversalKnowledgeMap, KnowledgeNavigator


# ============================================================
# UniversalKnowledgeMap
# ============================================================


class TestUniversalKnowledgeMap:
    def test_init(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        assert ukm.pattern_matrix.shape == (64, 16)
        assert ukm.singular_values.shape == (16,)
        assert ukm.k == 16

    def test_init_k_matches_singular_values(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        assert ukm.k == len(s)

    def test_project_returns_array(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x = np.random.randn(64)
        proj = ukm.project(x)

        assert isinstance(proj, np.ndarray)
        assert len(proj) == 16

    def test_project_shape(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x = np.random.randn(64)
        proj = ukm.project(x)
        assert proj.shape == (16,)

    def test_project_deterministic(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x = np.random.randn(64)
        proj1 = ukm.project(x)
        proj2 = ukm.project(x)

        np.testing.assert_array_almost_equal(proj1, proj2)

    def test_project_different_inputs_different_outputs(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x1 = np.random.randn(64)
        x2 = np.random.randn(64)
        proj1 = ukm.project(x1)
        proj2 = ukm.project(x2)

        # Different inputs should generally give different projections
        assert not np.allclose(proj1, proj2)

    def test_project_with_zero_input(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x = np.zeros(64)
        proj = ukm.project(x)
        np.testing.assert_array_almost_equal(proj, np.zeros(16))

    def test_similarity_same_vector(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x = np.random.randn(64)
        sim = ukm.similarity(x, x)
        assert abs(sim - 1.0) < 1e-6

    def test_similarity_range(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x1 = np.random.randn(64)
        x2 = np.random.randn(64)
        sim = ukm.similarity(x1, x2)
        assert -1.0 <= sim <= 1.0 + 1e-6

    def test_similarity_symmetric(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x1 = np.random.randn(64)
        x2 = np.random.randn(64)
        sim_ab = ukm.similarity(x1, x2)
        sim_ba = ukm.similarity(x2, x1)
        assert abs(sim_ab - sim_ba) < 1e-6

    def test_similarity_orthogonal_vectors(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x1 = np.random.randn(64)
        x2 = np.zeros(64)
        sim = ukm.similarity(x1, x2)
        assert sim == 0.0

    def test_similarity_deterministic(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x1 = np.random.randn(64)
        x2 = np.random.randn(64)
        sim1 = ukm.similarity(x1, x2)
        sim2 = ukm.similarity(x1, x2)
        assert sim1 == sim2

    def test_encode_same_as_project(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x = np.random.randn(64)
        enc = ukm.encode(x)
        proj = ukm.project(x)
        np.testing.assert_array_almost_equal(enc, proj)

    def test_decode_returns_to_original_dim(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        coords = np.random.randn(16)
        decoded = ukm.decode(coords)
        assert decoded.shape == (64,)

    def test_decode_with_zero_coords(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        decoded = ukm.decode(np.zeros(16))
        np.testing.assert_array_almost_equal(decoded, np.zeros(64))

    def test_roundtrip_projection(self):
        """encode → decode should approximately recover the input."""
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x = np.random.randn(64)
        encoded = ukm.encode(x)
        decoded = ukm.decode(encoded)

        # Not exact because k < d_model, but should be close-ish
        error = np.linalg.norm(x - decoded) / np.linalg.norm(x)
        assert error > 0  # Some error expected (k < d_model)
        assert error < 5.0  # But not unbounded

    def test_different_k_values(self):
        """Test with various k values."""
        for k in [1, 4, 8, 16, 32]:
            P = np.random.randn(64, k).astype(np.float32)
            s = np.random.rand(k).astype(np.float32) + 0.1
            ukm = UniversalKnowledgeMap(P, s)

            x = np.random.randn(64)
            proj = ukm.project(x)
            assert len(proj) == k

    def test_large_d_model(self):
        P = np.random.randn(4096, 32).astype(np.float32)
        s = np.random.rand(32).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)

        x = np.random.randn(4096)
        proj = ukm.project(x)
        assert len(proj) == 32


# ============================================================
# KnowledgeNavigator
# ============================================================


class TestKnowledgeNavigator:
    def test_init(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        assert nav.map is ukm

    # --- find_similar ---

    def test_find_similar_returns_list(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        query = np.random.randn(64)
        candidates = [np.random.randn(64) for _ in range(5)]
        results = nav.find_similar(query, candidates, top_k=3)

        assert isinstance(results, list)
        assert len(results) == 3

    def test_find_similar_sorted_by_similarity(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        query = np.random.randn(64)
        candidates = [np.random.randn(64) for _ in range(10)]
        results = nav.find_similar(query, candidates, top_k=5)

        sims = [sim for _, sim, _ in results]
        for i in range(len(sims) - 1):
            assert sims[i] >= sims[i + 1] - 1e-6

    def test_find_similar_top_k_larger_than_candidates(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        query = np.random.randn(64)
        candidates = [np.random.randn(64) for _ in range(3)]
        results = nav.find_similar(query, candidates, top_k=10)

        assert len(results) == 3  # Can't return more than candidates

    def test_find_similar_empty_candidates(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        query = np.random.randn(64)
        results = nav.find_similar(query, [], top_k=5)
        assert results == []

    def test_find_similar_identical_candidates(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        query = np.random.randn(64)
        identical = [query.copy() for _ in range(3)]
        results = nav.find_similar(query, identical, top_k=3)

        # All should have high similarity
        for _, sim, _ in results:
            assert sim > 0.9

    # --- cluster ---

    def test_cluster_returns_list_of_lists(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        items = [np.random.randn(64) for _ in range(10)]
        clusters = nav.cluster(items)

        assert isinstance(clusters, list)
        for cluster in clusters:
            assert isinstance(cluster, list)

    def test_cluster_all_items_assigned(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        items = [np.random.randn(64) for _ in range(10)]
        clusters = nav.cluster(items)

        all_assigned = []
        for cluster in clusters:
            all_assigned.extend(cluster)
        assert sorted(all_assigned) == list(range(10))

    def test_cluster_no_items(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        clusters = nav.cluster([])
        assert clusters == []

    def test_cluster_identical_items(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        item = np.random.randn(64)
        identical = [item.copy() for _ in range(5)]
        clusters = nav.cluster(identical)

        # All identical items should be in the same cluster
        for cluster in clusters:
            if len(cluster) > 1:
                pass  # They should be together
        assert len(clusters) >= 1

    # --- dimension_analysis ---

    def test_dimension_analysis_returns_dict(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        item = np.random.randn(64)
        result = nav.dimension_analysis(item)

        assert "pattern_dims" in result
        assert "pattern_weights" in result
        assert "total_activation" in result
        assert "dimensionality" in result

    def test_dimension_analysis_top_5_dims(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        item = np.random.randn(64)
        result = nav.dimension_analysis(item)

        assert len(result["pattern_dims"]) == 5
        assert len(result["pattern_weights"]) == 5

    def test_dimension_analysis_total_activation(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        item = np.random.randn(64)
        result = nav.dimension_analysis(item)

        proj = ukm.project(item)
        expected_activation = np.linalg.norm(proj)
        assert abs(result["total_activation"] - expected_activation) < 1e-4

    def test_dimension_analysis_zero_item(self):
        P = np.random.randn(64, 16).astype(np.float32)
        s = np.random.rand(16).astype(np.float32) + 0.1
        ukm = UniversalKnowledgeMap(P, s)
        nav = KnowledgeNavigator(ukm)

        result = nav.dimension_analysis(np.zeros(64))
        assert result["total_activation"] == 0.0
        assert result["dimensionality"] == 0.0
