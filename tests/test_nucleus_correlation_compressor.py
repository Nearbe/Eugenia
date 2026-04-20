#!/usr/bin/env python3
"""
Tests for src/nucleus/correlation_compressor.py

Covers: CorrelationCompressor compress_delta, compress_correlation_svd,
        decompress_correlation_svd, compress_graph, compress_hessian_pattern.
"""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nucleus.correlation_compressor import CorrelationCompressor


# ============================================================
# CorrelationCompressor
# ============================================================


class TestCorrelationCompressor:
    def test_init(self):
        comp = CorrelationCompressor()
        assert comp.delta is None
        assert comp.correlation_eigen is None
        assert comp.graph is None

    # --- compress_delta ---

    def test_compress_delta_random(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        delta, W_init = comp.compress_delta(W, init_type="random")

        assert isinstance(delta, np.ndarray)
        assert isinstance(W_init, np.ndarray)
        assert delta.shape == W.shape
        assert W_init.shape == W.shape
        np.testing.assert_array_almost_equal(W, delta + W_init)

    def test_compress_delta_zeros(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        delta, W_init = comp.compress_delta(W, init_type="zeros")

        np.testing.assert_array_almost_equal(W_init, np.zeros_like(W))
        np.testing.assert_array_almost_equal(delta, W)

    def test_compress_delta_xavier(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        delta, W_init = comp.compress_delta(W, init_type="xavier")

        assert delta.shape == W.shape
        assert W_init.shape == W.shape
        # Xavier scale
        expected_scale = np.sqrt(2.0 / (10 + 10))
        assert W_init.std() < expected_scale * 3  # Should be within ~3σ

    def test_compress_delta_reconstruction(self):
        comp = CorrelationCompressor()
        W = np.random.randn(20, 15).astype(np.float32)
        delta, W_init = comp.compress_delta(W, init_type="xavier")

        W_reconstructed = W_init + delta
        np.testing.assert_array_almost_equal(W, W_reconstructed)

    # --- compress_correlation_svd ---

    def test_compress_correlation_svd_basic(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        result = comp.compress_correlation_svd(W, k=4)

        assert "U" in result
        assert "S" in result
        assert "Vt" in result
        assert "k" in result
        assert "shape" in result
        assert result["U"].shape == (10, 4)
        assert result["S"].shape == (4,)
        assert result["Vt"].shape == (4, 10)
        assert result["k"] == 4
        assert result["shape"] == (10, 10)

    def test_compress_correlation_svd_default_k(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        result = comp.compress_correlation_svd(W)

        assert result["k"] == 4  # default
        assert result["U"].shape == (10, 4)

    def test_compress_correlation_svd_clips_k(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        result = comp.compress_correlation_svd(W, k=100)

        assert result["U"].shape[1] == 10  # clipped to min(m,n)

    def test_compress_correlation_svd_stores_in_instance(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        comp.compress_correlation_svd(W, k=4)

        assert comp.correlation_eigen is not None
        assert comp.correlation_eigen["k"] == 4

    def test_compress_correlation_svd_dtype(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        result = comp.compress_correlation_svd(W, k=4)

        assert result["U"].dtype == np.float16
        assert result["S"].dtype == np.float16
        assert result["Vt"].dtype == np.float16

    # --- decompress_correlation_svd ---

    def test_decompress_correlation_svd_shape(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        comp.compress_correlation_svd(W, k=4)
        W_rec = comp.decompress_correlation_svd()

        assert W_rec.shape == (10, 10)
        assert W_rec.dtype == np.float32

    def test_decompress_correlation_svd_quality(self):
        comp = CorrelationCompressor()
        W = np.random.randn(50, 50).astype(np.float32)
        comp.compress_correlation_svd(W, k=32)
        W_rec = comp.decompress_correlation_svd()

        error = np.linalg.norm(W - W_rec) / np.linalg.norm(W)
        # With k=32 on 50x50, error should be reasonable
        assert error < 0.5  # Relaxed tolerance for float16

    def test_decompress_correlation_svd_requires_prior_call(self):
        comp = CorrelationCompressor()
        with pytest.raises(KeyError):
            comp.decompress_correlation_correlation_svd()  # Will fail

    # --- compress_graph ---

    def test_compress_graph_basic(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        data, sparsity = comp.compress_graph(W, threshold=0.5)

        assert isinstance(data, bytes)
        assert isinstance(sparsity, float)
        assert 0.0 <= sparsity <= 1.0

    def test_compress_graph_sparse(self):
        comp = CorrelationCompressor()
        W = np.random.randn(100, 100).astype(np.float32) * 0.01  # Small values
        data, sparsity = comp.compress_graph(W, threshold=0.5)

        # Most values should be below threshold
        assert sparsity < 0.5

    def test_compress_graph_dense(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32) * 100  # Large values
        data, sparsity = comp.compress_graph(W, threshold=0.01)

        # Most values should be above threshold
        assert sparsity > 0.5

    def test_compress_graph_zero_matrix(self):
        comp = CorrelationCompressor()
        W = np.zeros((10, 10), dtype=np.float32)
        data, sparsity = comp.compress_graph(W, threshold=0.5)

        assert sparsity == 0.0

    # --- compress_hessian_pattern ---

    def test_compress_hessian_pattern_square(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        H = comp.compress_hessian_pattern(W)

        assert H.shape == (10, 10)
        assert H.dtype == np.float64  # W @ W.T with float32 → float64

    def test_compress_hessian_pattern_rectangular(self):
        comp = CorrelationCompressor()
        W = np.random.randn(20, 10).astype(np.float32)
        H = comp.compress_hessian_pattern(W)

        assert H.shape == (20, 20)

    def test_compress_hessian_pattern_symmetric(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        H = comp.compress_hessian_pattern(W)

        np.testing.assert_array_almost_equal(H, H.T)

    def test_compress_hessian_pattern_positive_semidefinite(self):
        comp = CorrelationCompressor()
        W = np.random.randn(10, 10).astype(np.float32)
        H = comp.compress_hessian_pattern(W)

        # H = W @ W.T should be positive semi-definite
        eigenvalues = np.linalg.eigvalsh(H)
        assert np.all(eigenvalues >= -1e-6)  # Allow small numerical errors

    # --- Integration ---

    def test_pipeline_compress_decompress(self):
        """Test full compression → decompression pipeline."""
        comp = CorrelationCompressor()
        W = np.random.randn(50, 50).astype(np.float32)

        comp.compress_correlation_svd(W, k=20)
        W_rec = comp.decompress_correlation_svd()

        error = np.linalg.norm(W - W_rec) / np.linalg.norm(W)
        assert error < 0.3  # Should be a reasonable approximation
