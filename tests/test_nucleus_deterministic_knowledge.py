#!/usr/bin/env python3
"""
Tests for src/nucleus/deterministic_knowledge.py

Covers: DeterministicPattern, DeterministicKnowledgeCore, DeterministicFunction.
"""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nucleus.deterministic_knowledge import (
    DeterministicPattern,
    DeterministicKnowledgeCore,
    DeterministicFunction,
)


# ============================================================
# DeterministicPattern
# ============================================================


class TestDeterministicPattern:
    def test_creation(self):
        vector = np.random.randn(16, 8).astype(np.float32)
        singular = np.random.rand(8).astype(np.float32) + 0.1
        pattern = DeterministicPattern(
            vector=vector,
            singular=singular,
            phase=0.5,
        )
        assert np.array_equal(pattern.vector, vector)
        assert np.array_equal(pattern.singular, singular)
        assert pattern.phase == 0.5

    def test_vector_shape(self):
        vector = np.random.randn(32, 16).astype(np.float32)
        singular = np.random.rand(16).astype(np.float32) + 0.1
        pattern = DeterministicPattern(
            vector=vector,
            singular=singular,
            phase=0.0,
        )
        assert pattern.vector.shape == (32, 16)
        assert pattern.singular.shape == (16,)


# ============================================================
# DeterministicKnowledgeCore
# ============================================================


class TestDeterministicKnowledgeCore:
    def test_init_defaults(self):
        core = DeterministicKnowledgeCore(d_model=4096, k=32)
        assert core.d_model == 4096
        assert core.k == 32
        assert core.patterns == []
        assert core.relationships is None
        assert core._initialized is False

    def test_init_custom_params(self):
        core = DeterministicKnowledgeCore(d_model=512, k=16)
        assert core.d_model == 512
        assert core.k == 16

    def test_learn_single_layer(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        core.learn(weights)

        assert len(core.patterns) == 1
        assert isinstance(core.patterns[0], DeterministicPattern)
        assert core._initialized is True

    def test_learn_multiple_layers(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {
            "q": np.random.randn(32, 32).astype(np.float32),
            "k": np.random.randn(32, 32).astype(np.float32),
            "v": np.random.randn(32, 32).astype(np.float32),
        }
        core.learn(weights)

        assert len(core.patterns) == 3
        assert core.relationships is not None

    def test_learn_returns_self(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        result = core.learn(weights)
        assert result is core

    def test_pattern_svd_extracted(self):
        core = DeterministicKnowledgeCore(d_model=32, k=8)
        W = np.random.randn(32, 32).astype(np.float32)
        core.learn({"layer_0": W})

        pattern = core.patterns[0]
        assert pattern.vector.shape == (32, 8)  # (d_model, k)
        assert pattern.singular.shape == (8,)
        assert pattern.singular[0] >= pattern.singular[1]  # SVD ordered

    def test_learn_relationships_shape(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {
            "layer_0": np.random.randn(32, 32).astype(np.float32),
            "layer_1": np.random.randn(32, 32).astype(np.float32),
        }
        core.learn(weights)

        assert core.relationships is not None
        assert core.relationships.shape[0] == 1  # layers - 1

    def test_forward_before_learn_raises(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        x = np.random.randn(32)

        with pytest.raises(ValueError, match="not initialized"):
            core.forward(x)

    def test_forward_returns_array(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        core.learn(weights)

        x = np.random.randn(32)
        output = core.forward(x)

        assert isinstance(output, np.ndarray)

    def test_forward_deterministic(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        core.learn(weights)

        x = np.random.randn(32)
        out1 = core.forward(x)
        out2 = core.forward(x)

        np.testing.assert_array_almost_equal(out1, out2)

    def test_apply_deterministic_before_learn(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        x = np.random.randn(32)

        with pytest.raises(ValueError, match="not initialized"):
            core.apply_deterministic(x, 0)

    def test_apply_deterministic_valid_layer(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {
            "layer_0": np.random.randn(32, 32).astype(np.float32),
            "layer_1": np.random.randn(32, 32).astype(np.float32),
        }
        core.learn(weights)

        x = np.random.randn(32)
        output = core.apply_deterministic(x, 0)

        assert isinstance(output, np.ndarray)
        assert len(output) == 32

    def test_apply_deterministic_out_of_range(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        core.learn(weights)

        x = np.random.randn(32)
        output = core.apply_deterministic(x, 10)

        np.testing.assert_array_equal(output, x)

    def test_apply_deterministic_same_input_same_output(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        core.learn(weights)

        x = np.random.randn(32)
        out1 = core.apply_deterministic(x, 0)
        out2 = core.apply_deterministic(x, 0)

        np.testing.assert_array_almost_equal(out1, out2)

    def test_get_deterministic_signature_uninitialized(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        sig = core.get_deterministic_signature()
        assert sig == "NOT_INITIALIZED"

    def test_get_deterministic_signature_initialized(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        core.learn(weights)

        sig = core.get_deterministic_signature()
        assert sig != "NOT_INITIALIZED"
        assert isinstance(sig, str)
        assert "d32_k4" in sig  # Contains d_model and k

    def test_get_deterministic_signature_deterministic(self):
        core1 = DeterministicKnowledgeCore(d_model=32, k=4)
        np.random.seed(42)
        weights1 = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        core1.learn(weights1)

        core2 = DeterministicKnowledgeCore(d_model=32, k=4)
        np.random.seed(42)
        weights2 = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        core2.learn(weights2)

        assert core1.get_deterministic_signature() == core2.get_deterministic_signature()

    def test_verify_determinism(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        core.learn(weights)

        x = np.random.randn(32)
        is_det, max_diff = core.verify_determinism(x, n_tests=10)

        assert is_det is True
        assert max_diff < 1e-10

    def test_verify_determinism_different_runs(self):
        core = DeterministicKnowledgeCore(d_model=32, k=4)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        core.learn(weights)

        x = np.random.randn(32)
        is_det, max_diff = core.verify_determinism(x, n_tests=100)

        assert is_det is True
        assert max_diff < 1e-10

    def test_learn_with_rank_deficient_matrix(self):
        core = DeterministicKnowledgeCore(d_model=10, k=4)
        W = np.ones((10, 10), dtype=np.float32) * 0.1
        core.learn({"rank1": W})
        assert len(core.patterns) == 1

    def test_learn_with_identity_matrix(self):
        core = DeterministicKnowledgeCore(d_model=10, k=4)
        W = np.eye(10, dtype=np.float32)
        core.learn({"eye": W})
        assert len(core.patterns) == 1
        assert core.patterns[0].singular[0] > 0


# ============================================================
# DeterministicFunction
# ============================================================


class TestDeterministicFunction:
    def test_init(self):
        df = DeterministicFunction(k=32)
        assert df.k == 32
        assert df.signature is None
        assert isinstance(df.core, DeterministicKnowledgeCore)

    def test_fit_returns_self(self):
        df = DeterministicFunction(k=16)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        result = df.fit(weights)
        assert result is df

    def test_fit_sets_signature(self):
        df = DeterministicFunction(k=16)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        df.fit(weights)

        assert df.signature is not None
        assert df.signature != ""

    def test_call_returns_array(self):
        df = DeterministicFunction(k=16)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        df.fit(weights)

        x = np.random.randn(32)
        output = df(x)
        assert isinstance(output, np.ndarray)

    def test_call_deterministic(self):
        df = DeterministicFunction(k=16)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        df.fit(weights)

        x = np.random.randn(32)
        out1 = df(x)
        out2 = df(x)

        np.testing.assert_array_almost_equal(out1, out2)

    def test_apply_returns_array(self):
        df = DeterministicFunction(k=16)
        weights = {
            "layer_0": np.random.randn(32, 32).astype(np.float32),
            "layer_1": np.random.randn(32, 32).astype(np.float32),
        }
        df.fit(weights)

        x = np.random.randn(32)
        output = df.apply(x, 0)
        assert isinstance(output, np.ndarray)

    def test_apply_out_of_range(self):
        df = DeterministicFunction(k=16)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        df.fit(weights)

        x = np.random.randn(32)
        output = df.apply(x, 10)
        np.testing.assert_array_equal(output, x)

    def test_verify_returns_dict(self):
        df = DeterministicFunction(k=16)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        df.fit(weights)

        x = np.random.randn(32)
        result = df.verify(x, n=10)

        assert "is_deterministic" in result
        assert "max_variation" in result
        assert "signature" in result
        assert result["is_deterministic"] is True
        assert result["signature"] == df.signature

    def test_different_weights_different_signature(self):
        df1 = DeterministicFunction(k=16)
        df1.fit({"layer_0": np.ones((32, 32), dtype=np.float32)})

        df2 = DeterministicFunction(k=16)
        df2.fit({"layer_0": np.ones((32, 32), dtype=np.float32) * 2})

        # Signatures should differ
        assert df1.signature != df2.signature

    def test_same_weights_same_signature(self):
        df1 = DeterministicFunction(k=16)
        np.random.seed(42)
        df1.fit({"layer_0": np.random.randn(32, 32).astype(np.float32)})

        df2 = DeterministicFunction(k=16)
        np.random.seed(42)
        df2.fit({"layer_0": np.random.randn(32, 32).astype(np.float32)})

        assert df1.signature == df2.signature

    def test_verify_with_many_tests(self):
        df = DeterministicFunction(k=16)
        weights = {"layer_0": np.random.randn(32, 32).astype(np.float32)}
        df.fit(weights)

        x = np.random.randn(32)
        result = df.verify(x, n=100)

        assert result["is_deterministic"] is True
        assert result["max_variation"] < 1e-10
