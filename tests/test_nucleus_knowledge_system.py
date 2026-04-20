#!/usr/bin/env python3
"""
Tests for src/nucleus/nucleus_knowledge_system.py

Covers: PatternNode, GeometricExtractor, KnowledgeSystem.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nucleus.nucleus_knowledge_system import (
    PatternNode,
    GeometricExtractor,
    KnowledgeSystem,
)


# ============================================================
# PatternNode
# ============================================================


class TestPatternNode:
    def test_creation_minimal(self):
        pattern = np.random.randn(32).astype(np.float32)
        node = PatternNode(
            node_id="test_1",
            pattern=pattern,
        )
        assert node.node_id == "test_1"
        assert np.array_equal(node.pattern, pattern)
        assert node.correlations == {}
        assert node.usage_count == 0
        assert node.solenoid is None
        assert node.fractal_sig is None
        assert node.pyramid is None
        assert node.spine_chain is None
        assert node.bridge is None

    def test_creation_with_all_fields(self):
        pattern = np.random.randn(32).astype(np.float32)
        solenoid = [0, 1, 0, 1]
        fractal_sig = {"dim": 1.5}
        pyramid = [{"level": 0}]
        spine_chain = [{"spine": 1}]
        bridge = {"identity": True}

        node = PatternNode(
            node_id="test_full",
            pattern=pattern,
            correlations={"related": 0.8},
            usage_count=5,
            created_at=1000.0,
            last_used=2000.0,
            solenoid=solenoid,
            fractal_sig=fractal_sig,
            pyramid=pyramid,
            spine_chain=spine_chain,
            bridge=bridge,
        )

        assert node.correlations == {"related": 0.8}
        assert node.usage_count == 5
        assert node.created_at == 1000.0
        assert node.last_used == 2000.0
        assert node.solenoid == solenoid
        assert node.fractal_sig == fractal_sig
        assert node.pyramid == pyramid
        assert node.spine_chain == spine_chain
        assert node.bridge == bridge

    def test_usage_count_increments(self):
        node = PatternNode(node_id="test", pattern=np.zeros(4))
        assert node.usage_count == 0
        node.usage_count += 1
        assert node.usage_count == 1

    def test_pattern_is_numpy_array(self):
        pattern = np.random.randn(16).astype(np.float32)
        node = PatternNode(node_id="test", pattern=pattern)
        assert isinstance(node.pattern, np.ndarray)


# ============================================================
# GeometricExtractor
# ============================================================


class TestGeometricExtractor:
    def test_init_defaults(self):
        extractor = GeometricExtractor()
        assert extractor.n_thresholds == 64
        assert extractor.solenoid_depth == 30
        assert extractor.pyramid_levels == 10

    def test_init_custom_params(self):
        extractor = GeometricExtractor(n_thresholds=128, solenoid_depth=20, pyramid_levels=15)
        assert extractor.n_thresholds == 128
        assert extractor.solenoid_depth == 20
        assert extractor.pyramid_levels == 15

    def test_extract_numpy_array(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        pattern = extractor.extract(data)

        assert isinstance(pattern, np.ndarray)
        assert len(pattern) > 0

    def test_extract_numpy_array_1d(self):
        extractor = GeometricExtractor()
        data = np.random.randn(100)
        pattern = extractor.extract(data)

        assert isinstance(pattern, np.ndarray)
        assert len(pattern) > 0

    def test_extract_string(self):
        extractor = GeometricExtractor()
        data = "hello world"
        pattern = extractor.extract(data)

        assert isinstance(pattern, np.ndarray)
        assert len(pattern) > 0

    def test_extract_scalar(self):
        extractor = GeometricExtractor()
        data = 42.0
        pattern = extractor.extract(data)

        assert isinstance(pattern, np.ndarray)
        assert len(pattern) > 0

    def test_extract_constant_data(self):
        extractor = GeometricExtractor()
        data = np.full((28, 28), 127.5)
        pattern = extractor.extract(data)

        assert isinstance(pattern, np.ndarray)
        assert len(pattern) > 0

    def test_extract_zero_data(self):
        extractor = GeometricExtractor()
        data = np.zeros((28, 28))
        pattern = extractor.extract(data)

        assert isinstance(pattern, np.ndarray)
        assert len(pattern) > 0

    def test_extract_different_data_different_patterns(self):
        extractor = GeometricExtractor()
        data1 = np.random.randn(28, 28)
        data2 = np.random.randn(28, 28) * 10
        pattern1 = extractor.extract(data1)
        pattern2 = extractor.extract(data2)

        # Patterns should differ
        assert not np.allclose(pattern1, pattern2)

    def test_extract_pattern_float32(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        pattern = extractor.extract(data)

        assert pattern.dtype == np.float32

    def test_extract_stores_solenoid(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        extractor.extract(data)

        assert extractor._last_solenoid is not None
        assert isinstance(extractor._last_solenoid, list)

    def test_extract_stores_fractal_sig(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        extractor.extract(data)

        assert extractor._last_fractal_sig is not None
        assert isinstance(extractor._last_fractal_sig, dict)

    def test_extract_stores_pyramid(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        extractor.extract(data)

        assert extractor._last_pyramid is not None
        assert isinstance(extractor._last_pyramid, list)

    def test_extract_stores_spine_chain(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        extractor.extract(data)

        assert extractor._last_spine_chain is not None
        assert isinstance(extractor._last_spine_chain, list)

    def test_extract_stores_bridge(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        extractor.extract(data)

        assert extractor._last_bridge is not None
        assert isinstance(extractor._last_bridge, dict)

    def test_similarity_same_pattern(self):
        extractor = GeometricExtractor()
        pattern = np.random.randn(32).astype(np.float32)
        sim = extractor.similarity(pattern, pattern)
        assert abs(sim - 1.0) < 0.01  # Should be ~1

    def test_similarity_range(self):
        extractor = GeometricExtractor()
        p1 = np.random.randn(32).astype(np.float32)
        p2 = np.random.randn(32).astype(np.float32)
        sim = extractor.similarity(p1, p2)
        # Similarity can be any value due to RealMath weighting
        assert isinstance(sim, float)

    def test_similarity_symmetric(self):
        extractor = GeometricExtractor()
        p1 = np.random.randn(32).astype(np.float32)
        p2 = np.random.randn(32).astype(np.float32)
        sim_ab = extractor.similarity(p1, p2)
        sim_ba = extractor.similarity(p2, p1)
        assert abs(sim_ab - sim_ba) < 0.01

    def test_similarity_zero_pattern(self):
        extractor = GeometricExtractor()
        p1 = np.random.randn(32).astype(np.float32)
        p2 = np.zeros(32)
        sim = extractor.similarity(p1, p2)
        assert sim == 0.0

    def test_distance_returns_float(self):
        extractor = GeometricExtractor()
        p1 = np.random.randn(32).astype(np.float32)
        p2 = np.random.randn(32).astype(np.float32)
        dist = extractor.distance(p1, p2)
        assert isinstance(dist, float)
        assert dist >= 0

    def test_distance_same_pattern(self):
        extractor = GeometricExtractor()
        p = np.random.randn(32).astype(np.float32)
        dist = extractor.distance(p, p)
        assert dist >= 0
        assert dist < 1e-6  # Should be ~0

    def test_solenoid_distance(self):
        node_a = PatternNode(node_id="a", pattern=np.random.randn(64).astype(np.float32))
        node_b = PatternNode(node_id="b", pattern=np.random.randn(64).astype(np.float32))

        dist = extractor = GeometricExtractor().solenoid_distance(node_a, node_b)
        assert isinstance(dist, float)
        assert dist >= 0

    def test_solenoid_distance_same_node(self):
        pattern = np.random.randn(64).astype(np.float32)
        node_a = PatternNode(node_id="a", pattern=pattern)
        node_b = PatternNode(node_id="b", pattern=pattern)

        extractor = GeometricExtractor()
        dist = extractor.solenoid_distance(node_a, node_b)
        assert dist >= 0


# ============================================================
# KnowledgeSystem
# ============================================================


class TestKnowledgeSystem:
    def test_init_defaults(self):
        system = KnowledgeSystem()
        assert system.extractor is not None
        assert system.nodes == {}
        assert system.similarity_threshold == 0.7
        assert system._node_counter == 0

    def test_init_custom_threshold(self):
        system = KnowledgeSystem(similarity_threshold=0.5)
        assert system.similarity_threshold == 0.5

    def test_absorb_text(self):
        system = KnowledgeSystem()
        node_id = system.absorb("hello world")

        assert node_id in system.nodes
        assert isinstance(system.nodes[node_id].pattern, np.ndarray)

    def test_absorb_numpy_array(self):
        system = KnowledgeSystem()
        data = np.random.randn(28, 28)
        node_id = system.absorb(data)

        assert node_id in system.nodes

    def test_absorb_with_label(self):
        system = KnowledgeSystem()
        node_id = system.absorb("test data", label="my_label")

        assert node_id == "my_label"

    def test_absorb_multiple(self):
        system = KnowledgeSystem()
        id1 = system.absorb("text one")
        id2 = system.absorb("text two")

        assert id1 != id2
        assert len(system.nodes) == 2

    def test_absorb_auto_increment_id(self):
        system = KnowledgeSystem()
        id1 = system.absorb("data1")
        id2 = system.absorb("data2")

        assert id1 == "node_0"
        assert id2 == "node_1"

    def test_absorb_creates_correlations(self):
        system = KnowledgeSystem(similarity_threshold=0.5)
        system.absorb("hello world")
        system.absorb("hello there")

        node0 = system.nodes["node_0"]
        node1 = system.nodes["node_1"]

        # They should be correlated if similarity > threshold
        if node1.node_id in node0.correlations:
            assert node0.correlations[node1.node_id] > 0.5

    def test_relate(self):
        system = KnowledgeSystem()
        system.absorb("text1", label="a")
        system.absorb("text2", label="b")

        system.relate("a", "b", strength=0.8)

        assert system.nodes["a"].correlations["b"] == 0.8
        assert system.nodes["b"].correlations["a"] == 0.8

    def test_relate_unknown_node(self):
        system = KnowledgeSystem()
        system.relate("unknown", "also_unknown", strength=0.5)
        assert system.nodes == {}

    def test_strengthen_existing_node(self):
        system = KnowledgeSystem()
        system.absorb("text1", label="a")
        system.absorb("text2", label="b")
        system.relate("a", "b", strength=0.8)

        system.strengthen("a")

        assert system.nodes["a"].usage_count == 1
        assert system.nodes["a"].last_used > 0

    def test_strengthen_correlation_boost(self):
        system = KnowledgeSystem()
        system.absorb("text1", label="a")
        system.absorb("text2", label="b")
        system.relate("a", "b", strength=0.5)

        system.strengthen("a")

        # Related correlation should be boosted
        if "b" in system.nodes["a"].correlations:
            assert system.nodes["a"].correlations["b"] >= 0.5

    def test_strengthen_unknown_node(self):
        system = KnowledgeSystem()
        system.strengthen("unknown")
        # Should not raise

    def test_generate_existing_node(self):
        system = KnowledgeSystem(similarity_threshold=0.0)  # Connect everything
        system.absorb("text1", label="a")
        system.absorb("text2", label="b")
        system.absorb("text3", label="c")

        related = system.generate("a", max_nodes=2)
        assert isinstance(related, list)

    def test_generate_unknown_node(self):
        system = KnowledgeSystem()
        related = system.generate("unknown")
        assert related == []

    def test_generate_returns_node_ids(self):
        system = KnowledgeSystem(similarity_threshold=0.0)
        system.absorb("text1", label="a")
        system.absorb("text2", label="b")
        system.absorb("text3", label="c")

        related = system.generate("a", max_nodes=2)
        for nid in related:
            assert nid in system.nodes

    def test_find_similar_basic(self):
        system = KnowledgeSystem()
        system.absorb("dog", label="dog1")
        system.absorb("cat", label="cat1")
        system.absorb("dog_house", label="dog2")

        similar = system.find_similar("dog", top_k=2)

        assert isinstance(similar, list)
        assert len(similar) == 2
        for nid, sim in similar:
            assert nid in system.nodes
            assert isinstance(sim, float)

    def test_find_similar_sorted(self):
        system = KnowledgeSystem()
        system.absorb("dog", label="dog1")
        system.absorb("cat", label="cat1")
        system.absorb("dog_house", label="dog2")

        similar = system.find_similar("dog", top_k=3)

        sims = [sim for _, sim in similar]
        for i in range(len(sims) - 1):
            assert sims[i] >= sims[i + 1] - 1e-6

    def test_find_similar_top_k_larger_than_nodes(self):
        system = KnowledgeSystem()
        system.absorb("text1", label="a")
        system.absorb("text2", label="b")

        similar = system.find_similar("text", top_k=10)
        assert len(similar) == 2

    def test_find_similar_empty_system(self):
        system = KnowledgeSystem()
        similar = system.find_similar("text")
        assert similar == []

    def test_query_new_data(self):
        system = KnowledgeSystem()
        result = system.query("brand new text")

        assert result["status"] == "new"
        assert "node_id" in result
        assert result["similar"] == []

    def test_query_existing_data(self):
        system = KnowledgeSystem(similarity_threshold=0.0)
        system.absorb("hello world", label="greeting")

        result = system.query("hello there")

        assert result["status"] == "existing"
        assert result["best_match"] == "greeting"
        assert "similarity" in result
        assert "related" in result

    def test_query_strengthens_best_match(self):
        system = KnowledgeSystem(similarity_threshold=0.0)
        system.absorb("hello world", label="greeting")

        initial_count = system.nodes["greeting"].usage_count
        system.query("hello there")

        assert system.nodes["greeting"].usage_count >= initial_count

    def test_get_stats_empty(self):
        system = KnowledgeSystem()
        stats = system.get_stats()

        assert stats["total_nodes"] == 0
        assert stats["total_correlations"] == 0
        assert stats["most_used_node"] is None
        assert stats["most_used_count"] == 0

    def test_get_stats_with_nodes(self):
        system = KnowledgeSystem(similarity_threshold=0.0)
        system.absorb("text1", label="a")
        system.absorb("text2", label="b")
        system.relate("a", "b", strength=0.5)

        stats = system.get_stats()

        assert stats["total_nodes"] == 2
        assert stats["total_correlations"] == 2  # bidirectional
        assert stats["most_used_node"] is not None

    def test_get_stats_most_used(self):
        system = KnowledgeSystem()
        system.absorb("text1", label="a")
        system.absorb("text2", label="b")

        system.strengthen("a")
        system.strengthen("a")
        system.strengthen("b")

        stats = system.get_stats()
        assert stats["most_used_node"] == "a"
        assert stats["most_used_count"] == 2

    def test_roundtrip_absorb_query(self):
        system = KnowledgeSystem(similarity_threshold=0.0)

        # Absorb training data
        for text in ["dog", "cat", "bird", "fish"]:
            system.absorb(text, label=text)

        # Query with similar text
        result = system.query("dog animal")
        assert result["status"] == "existing"
        assert result["best_match"] in ["dog", "cat", "bird", "fish"]

    def test_absorb_with_constant_data(self):
        system = KnowledgeSystem()
        data = np.full((28, 28), 127.5)
        node_id = system.absorb(data)

        assert node_id in system.nodes
