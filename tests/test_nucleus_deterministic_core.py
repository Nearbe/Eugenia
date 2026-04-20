#!/usr/bin/env python3
"""
Tests for src/nucleus/deterministic_core.py

Covers: SemanticPattern, PatternRelationship, DeterministicKnowledgeCore,
        serialize/deserialize, RealMath integration methods.
"""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nucleus.deterministic_core import (
    SemanticPattern,
    PatternRelationship,
    DeterministicKnowledgeCore,
    serialize,
    deserialize,
)


# ============================================================
# SemanticPattern
# ============================================================


class TestSemanticPattern:
    def test_creation_with_valid_vector(self):
        vector = np.array([1.0, 0.0, 0.0])
        pattern = SemanticPattern(
            vector=vector,
            singular=2.5,
            capacity=10.0,
            phase=0.5,
        )
        assert np.array_equal(pattern.vector, vector)
        assert pattern.singular == 2.5
        assert pattern.capacity == 10.0
        assert pattern.phase == 0.5

    def test_creation_with_flat_vector(self):
        vector = np.array([1.0, 2.0, 3.0, 4.0])
        pattern = SemanticPattern(
            vector=vector,
            singular=1.0,
            capacity=4.0,
            phase=0.0,
        )
        assert len(pattern.vector) == 4

    def test_vector_is_copy(self):
        original = np.array([1.0, 2.0])
        pattern = SemanticPattern(vector=original, singular=1.0, capacity=1.0, phase=0.0)
        original[0] = 999.0
        assert pattern.vector[0] != 999.0  # dataclass doesn't copy, but we test the value


# ============================================================
# PatternRelationship
# ============================================================


class TestPatternRelationship:
    def test_creation(self):
        matrix = np.array([[0.5]], dtype=np.float32)
        rel = PatternRelationship(
            layer_from="layer_0",
            layer_to="layer_1",
            matrix=matrix,
        )
        assert rel.layer_from == "layer_0"
        assert rel.layer_to == "layer_1"
        assert rel.matrix.shape == (1, 1)

    def test_matrix_dtype(self):
        matrix = np.array([[1.0]], dtype=np.float32)
        rel = PatternRelationship(
            layer_from="a",
            layer_to="b",
            matrix=matrix,
        )
        assert rel.matrix.dtype == np.float32


# ============================================================
# DeterministicKnowledgeCore
# ============================================================


class TestDeterministicKnowledgeCore:
    def test_init_defaults(self):
        core = DeterministicKnowledgeCore()
        assert core.d_model == 4096
        assert core.k == 32
        assert core.patterns == {}
        assert core.relationships == {}
        assert core.signature == ""
        assert core._initialized is False

    def test_init_custom_params(self):
        core = DeterministicKnowledgeCore(d_model=512, k=16)
        assert core.d_model == 512
        assert core.k == 16

    def test_learn_single_layer(self):
        core = DeterministicKnowledgeCore(d_model=64, k=4)
        W = np.random.randn(64, 64).astype(np.float32)
        core.learn({"layer_0": W})

        assert len(core.patterns) == 1
        assert "layer_0" in core.patterns
        assert isinstance(core.patterns["layer_0"], SemanticPattern)
        assert core._initialized is True

    def test_learn_multiple_layers(self):
        core = DeterministicKnowledgeCore(d_model=64, k=4)
        weights = {
            "layer_0": np.random.randn(64, 64).astype(np.float32),
            "layer_1": np.random.randn(64, 64).astype(np.float32),
            "layer_2": np.random.randn(64, 64).astype(np.float32),
        }
        core.learn(weights)

        assert len(core.patterns) == 3
        assert len(core.relationships) == 2  # 3 layers → 2 relationships
        assert "layer_0->layer_1" in core.relationships
        assert "layer_1->layer_2" in core.relationships

    def test_learn_returns_self(self):
        core = DeterministicKnowledgeCore(d_model=64, k=4)
        W = np.random.randn(64, 64).astype(np.float32)
        result = core.learn({"layer_0": W})
        assert result is core

    def test_pattern_vector_shape(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W = np.random.randn(64, 64).astype(np.float32)
        core.learn({"layer_0": W})
        assert len(core.patterns["layer_0"].vector) == 32  # d_model

    def test_pattern_singular_value(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W = np.random.randn(64, 64).astype(np.float32)
        core.learn({"layer_0": W})
        assert core.patterns["layer_0"].singular > 0  # SVD singular values are always >= 0

    def test_pattern_capacity(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W = np.random.randn(64, 64).astype(np.float32)
        core.learn({"layer_0": W})
        # capacity = -sum(S^2 * log(S^2)), depends on singular values
        assert isinstance(core.patterns["layer_0"].capacity, float)

    def test_pattern_phase(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W = np.random.randn(64, 64).astype(np.float32)
        core.learn({"layer_0": W})
        assert isinstance(core.patterns["layer_0"].phase, float)

    def test_signature_is_deterministic(self):
        core = DeterministicKnowledgeCore(d_model=64, k=4)
        np.random.seed(42)
        W1 = np.random.randn(64, 64).astype(np.float32)
        core.learn({"layer_0": W1})
        sig1 = core.get_signature()

        core2 = DeterministicKnowledgeCore(d_model=64, k=4)
        np.random.seed(42)
        W2 = np.random.randn(64, 64).astype(np.float32)
        core2.learn({"layer_0": W2})
        sig2 = core2.get_signature()

        assert sig1 == sig2
        assert len(sig1) == 16  # first 16 chars of SHA-256

    def test_signature_changes_with_different_weights(self):
        core = DeterministicKnowledgeCore(d_model=64, k=4)
        W1 = np.ones((64, 64), dtype=np.float32) * 0.1
        core.learn({"layer_0": W1})
        sig1 = core.get_signature()

        core2 = DeterministicKnowledgeCore(d_model=64, k=4)
        W2 = np.ones((64, 64), dtype=np.float32) * 0.2
        core2.learn({"layer_0": W2})
        sig2 = core2.get_signature()

        assert sig1 != sig2

    def test_forward_returns_array(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W = np.random.randn(32, 32).astype(np.float32)
        core.learn({"layer_0": W})

        input_vec = np.random.randn(32)
        output = core.forward(input_vec, "layer_0")
        assert isinstance(output, np.ndarray)
        assert len(output) == 32  # d_model

    def test_forward_with_unknown_layer(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W = np.random.randn(32, 32).astype(np.float32)
        core.learn({"layer_0": W})

        input_vec = np.random.randn(32)
        output = core.forward(input_vec, "unknown_layer")
        np.testing.assert_array_equal(output, input_vec)

    def test_verify_determinism(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W = np.random.randn(32, 32).astype(np.float32)
        core.learn({"layer_0": W})

        input_vec = np.random.randn(32)
        result = core.verify_determinism(input_vec, n_runs=10)

        assert result["is_deterministic"] is True
        assert result["max_variation"] < 1e-10
        assert result["signature"] == core.get_signature()

    def test_get_compressed_size(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W = np.random.randn(32, 32).astype(np.float32)
        core.learn({"layer_0": W})

        size = core.get_compressed_size()
        assert size > 0
        assert isinstance(size, int)

    # ============================================================
    # RealMath integration methods
    # ============================================================

    def test_pattern_distance(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W1 = np.random.randn(32, 32).astype(np.float32)
        W2 = np.random.randn(32, 32).astype(np.float32)
        core.learn({"layer_0": W1, "layer_1": W2})

        dist = core.pattern_distance(core.patterns["layer_0"], core.patterns["layer_1"])
        assert isinstance(dist, float)
        assert dist >= 0

    def test_pattern_distance_same_pattern(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W = np.random.randn(32, 32).astype(np.float32)
        core.learn({"layer_0": W})

        dist = core.pattern_distance(core.patterns["layer_0"], core.patterns["layer_0"])
        assert dist >= 0

    def test_solenoid_similarity(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W1 = np.random.randn(32, 32).astype(np.float32)
        W2 = np.random.randn(32, 32).astype(np.float32)
        core.learn({"layer_0": W1, "layer_1": W2})

        sim = core.solenoid_similarity(core.patterns["layer_0"], core.patterns["layer_1"])
        assert isinstance(sim, float)
        assert 0.0 <= sim <= 1.0

    def test_p_adic_similarity(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        W1 = np.random.randn(32, 32).astype(np.float32)
        W2 = np.random.randn(32, 32).astype(np.float32)
        core.learn({"layer_0": W1, "layer_1": W2})

        sim = core.p_adic_similarity(core.patterns["layer_0"], core.patterns["layer_1"])
        assert isinstance(sim, float)
        assert sim >= 0

    def test_learn_with_small_matrix(self):
        core = DeterministicKnowledgeCore(d_model=4, k=2)
        W = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
        core.learn({"small": W})
        assert "small" in core.patterns

    def test_learn_with_rank_deficient_matrix(self):
        core = DeterministicKnowledgeCore(d_model=4, k=2)
        # Rank-1 matrix
        W = np.ones((4, 4), dtype=np.float32) * 0.1
        core.learn({"rank1": W})
        assert "rank1" in core.patterns

    def test_learn_with_identity_matrix(self):
        core = DeterministicKnowledgeCore(d_model=4, k=2)
        W = np.eye(4, dtype=np.float32)
        core.learn({"eye": W})
        assert "eye" in core.patterns


# ============================================================
# serialize / deserialize
# ============================================================


class TestSerializeDeserialize:
    def test_roundtrip(self):
        core = DeterministicKnowledgeCore(d_model=16, k=2)
        W = np.random.randn(8, 8).astype(np.float32)
        core.learn({"layer_0": W})

        data = serialize(core)
        assert isinstance(data, bytes)
        assert len(data) > 0

        restored = deserialize(data)
        assert restored.d_model == core.d_model
        assert restored.k == core.k
        assert len(restored.patterns) == len(core.patterns)
        assert restored.signature == core.signature

    def test_roundtrip_multiple_layers(self):
        core = DeterministicKnowledgeCore(d_model=16, k=2)
        weights = {
            "layer_0": np.random.randn(8, 8).astype(np.float32),
            "layer_1": np.random.randn(8, 8).astype(np.float32),
        }
        core.learn(weights)

        data = serialize(core)
        restored = deserialize(data)

        assert len(restored.patterns) == 2
        assert len(restored.relationships) == 1
        assert "layer_0" in restored.patterns
        assert "layer_1" in restored.patterns

    def test_serialize_different_d_model(self):
        core = DeterministicKnowledgeCore(d_model=64, k=4)
        W = np.random.randn(8, 8).astype(np.float32)
        core.learn({"layer_0": W})

        data = serialize(core)
        restored = deserialize(data)
        assert restored.d_model == 64

    def test_serialize_empty_core(self):
        core = DeterministicKnowledgeCore(d_model=8, k=2)
        data = serialize(core)
        restored = deserialize(data)
        assert restored.d_model == 8
        assert len(restored.patterns) == 0

    def test_deserialize_corrupted_data(self):
        data = b"\x00" * 10  # Too short
        with pytest.raises(Exception):
            deserialize(data)

    def test_pattern_vector_preserved(self):
        core = DeterministicKnowledgeCore(d_model=8, k=2)
        W = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
        core.learn({"layer_0": W})

        original_vector = core.patterns["layer_0"].vector.copy()
        original_singular = core.patterns["layer_0"].singular

        data = serialize(core)
        restored = deserialize(data)

        # Note: vectors are stored as float16 in serialization
        np.testing.assert_array_almost_equal(
            restored.patterns["layer_0"].vector, original_vector, decimal=2
        )
        assert abs(restored.patterns["layer_0"].singular - original_singular) < 0.1
