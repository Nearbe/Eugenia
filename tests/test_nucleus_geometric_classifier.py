#!/usr/bin/env python3
"""
Tests for src/nucleus/universal_geometric_classifier.py

Covers: GeometricProfile, GeometricExtractor, UniversalGeometricClassifier.
"""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nucleus.universal_geometric_classifier import (
    GeometricProfile,
    GeometricExtractor,
    UniversalGeometricClassifier,
)


# ============================================================
# GeometricProfile
# ============================================================


class TestGeometricProfile:
    def test_creation(self):
        hist = np.random.rand(100)
        jumps = [(0.5, 0.3, 0.7, 0.4)]
        betti = np.random.rand(10).astype(np.float32)
        phase = np.random.rand(10).astype(np.float32)

        profile = GeometricProfile(
            binary_histogram=hist,
            jump_events=jumps,
            betti_signature=betti,
            capacity=1.5,
            phase_signature=phase,
        )

        assert np.array_equal(profile.binary_histogram, hist)
        assert profile.jump_events == jumps
        assert np.array_equal(profile.betti_signature, betti)
        assert profile.capacity == 1.5
        assert np.array_equal(profile.phase_signature, phase)

    def test_binary_histogram_is_ndarray(self):
        hist = np.random.rand(50)
        profile = GeometricProfile(
            binary_histogram=hist,
            jump_events=[],
            betti_signature=np.zeros(5),
            capacity=0.5,
            phase_signature=np.zeros(5),
        )
        assert isinstance(profile.binary_histogram, np.ndarray)


# ============================================================
# GeometricExtractor
# ============================================================


class TestGeometricExtractor:
    def test_init_defaults(self):
        extractor = GeometricExtractor()
        assert extractor.n_thresholds == 100
        assert extractor.jump_threshold == 1.0

    def test_init_custom_params(self):
        extractor = GeometricExtractor(n_thresholds=50, jump_threshold=2.0)
        assert extractor.n_thresholds == 50
        assert extractor.jump_threshold == 2.0

    def test_extract_returns_profile(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        profile = extractor.extract(data)

        assert isinstance(profile, GeometricProfile)

    def test_extract_profile_histogram_shape(self):
        extractor = GeometricExtractor(n_thresholds=50)
        data = np.random.randn(28, 28)
        profile = extractor.extract(data)

        assert len(profile.binary_histogram) == 50

    def test_extract_profile_histogram_normalized(self):
        extractor = GeometricExtractor(n_thresholds=100)
        data = np.random.randn(28, 28)
        profile = extractor.extract(data)

        # Histogram values are densities in [0, 1]
        assert np.all(profile.binary_histogram >= 0)
        assert np.all(profile.binary_histogram <= 1)

    def test_extract_profile_jump_events(self):
        extractor = GeometricExtractor(n_thresholds=100, jump_threshold=0.5)
        data = np.random.randn(28, 28)
        profile = extractor.extract(data)

        assert isinstance(profile.jump_events, list)
        for event in profile.jump_events:
            threshold, before, after, jump = event
            assert isinstance(threshold, float)
            assert isinstance(before, float)
            assert isinstance(after, float)
            assert isinstance(jump, float)

    def test_extract_profile_betti_signature(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        profile = extractor.extract(data)

        assert isinstance(profile.betti_signature, np.ndarray)
        assert len(profile.betti_signature) > 0

    def test_extract_profile_capacity(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        profile = extractor.extract(data)

        assert isinstance(profile.capacity, float)
        assert profile.capacity >= 0

    def test_extract_profile_phase_signature(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        profile = extractor.extract(data)

        assert isinstance(profile.phase_signature, np.ndarray)
        assert len(profile.phase_signature) == 10

    def test_extract_1d_data(self):
        extractor = GeometricExtractor()
        data = np.random.randn(100)
        profile = extractor.extract(data)

        assert isinstance(profile, GeometricProfile)

    def test_extract_2d_data(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28)
        profile = extractor.extract(data)

        assert isinstance(profile, GeometricProfile)

    def test_extract_3d_data(self):
        extractor = GeometricExtractor()
        data = np.random.randn(28, 28, 3)
        profile = extractor.extract(data)

        assert isinstance(profile, GeometricProfile)

    def test_extract_constant_data(self):
        extractor = GeometricExtractor()
        data = np.full((28, 28), 127.5)
        profile = extractor.extract(data)

        assert isinstance(profile, GeometricProfile)
        assert len(profile.binary_histogram) == 100

    def test_extract_zero_data(self):
        extractor = GeometricExtractor()
        data = np.zeros((28, 28))
        profile = extractor.extract(data)

        assert isinstance(profile, GeometricProfile)

    def test_extract_deterministic(self):
        extractor1 = GeometricExtractor()
        extractor2 = GeometricExtractor()
        data = np.random.randn(28, 28)

        profile1 = extractor1.extract(data)
        profile2 = extractor2.extract(data)

        np.testing.assert_array_almost_equal(profile1.binary_histogram, profile2.binary_histogram)
        assert profile1.capacity == profile2.capacity


# ============================================================
# UniversalGeometricClassifier
# ============================================================


class TestUniversalGeometricClassifier:
    def test_init(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        assert clf.extractor.n_thresholds == 50
        assert clf.class_profiles == {}
        assert clf.signature == ""

    def test_fit_basic(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        X = np.random.randn(20, 28, 28).astype(np.float32)
        y = np.array([0] * 10 + [1] * 10)

        result = clf.fit(X, y)

        assert result is clf
        assert len(clf.class_profiles) == 2
        assert 0 in clf.class_profiles
        assert 1 in clf.class_profiles

    def test_fit_multiple_classes(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        X = np.random.randn(50, 28, 28).astype(np.float32)
        y = np.array([0] * 10 + [1] * 10 + [2] * 10 + [3] * 10 + [4] * 10)

        clf.fit(X, y)
        assert len(clf.class_profiles) == 5

    def test_fit_sets_signature(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        X = np.random.randn(20, 28, 28).astype(np.float32)
        y = np.array([0] * 10 + [1] * 10)

        clf.fit(X, y)
        assert clf.signature != ""
        assert len(clf.signature) == 16

    def test_fit_deterministic(self):
        clf1 = UniversalGeometricClassifier(n_thresholds=50)
        clf2 = UniversalGeometricClassifier(n_thresholds=50)

        np.random.seed(42)
        X = np.random.randn(20, 28, 28).astype(np.float32)
        y = np.array([0] * 10 + [1] * 10)

        clf1.fit(X, y)
        clf2.fit(X, y)

        assert clf1.signature == clf2.signature
        assert len(clf1.class_profiles) == len(clf2.class_profiles)

    def test_predict_returns_int(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        X = np.random.randn(20, 28, 28).astype(np.float32)
        y = np.array([0] * 10 + [1] * 10)
        clf.fit(X, y)

        pred = clf.predict(np.random.randn(28, 28))
        assert isinstance(pred, int)

    def test_predict_returns_known_class(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        X = np.random.randn(20, 28, 28).astype(np.float32)
        y = np.array([0] * 10 + [1] * 10)
        clf.fit(X, y)

        for _ in range(10):
            pred = clf.predict(np.random.randn(28, 28))
            assert pred in [0, 1]

    def test_predict_deterministic(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        X = np.random.randn(20, 28, 28).astype(np.float32)
        y = np.array([0] * 10 + [1] * 10)
        clf.fit(X, y)

        test_input = np.random.randn(28, 28)
        pred1 = clf.predict(test_input)
        pred2 = clf.predict(test_input)

        assert pred1 == pred2

    def test_predict_untrained(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        # Not fitted
        with pytest.raises(Exception):
            clf.predict(np.random.randn(28, 28))

    def test_predict_with_similar_training_data(self):
        """Test that similar training data gets classified to same class."""
        clf = UniversalGeometricClassifier(n_thresholds=50)

        # Create two distinct classes
        np.random.seed(42)
        class_0 = np.random.randn(10, 28, 28).astype(np.float32) * 0.5 + 0.5
        class_1 = np.random.randn(10, 28, 28).astype(np.float32) * 0.5 - 0.5

        X = np.vstack([class_0, class_1])
        y = np.array([0] * 10 + [1] * 10)
        clf.fit(X, y)

        # Classify training samples
        correct = 0
        for i in range(20):
            pred = clf.predict(X[i])
            if pred == y[i]:
                correct += 1

        # Should be at least somewhat correct due to geometric similarity
        assert correct >= 5  # At least 25% correct

    def test_get_compressed_size(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        X = np.random.randn(20, 28, 28).astype(np.float32)
        y = np.array([0] * 10 + [1] * 10)
        clf.fit(X, y)

        size = clf.get_compressed_size()
        assert isinstance(size, int)
        assert size > 0

    def test_get_compressed_size_empty(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        size = clf.get_compressed_size()
        assert size == 0

    def test_fit_single_class(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        X = np.random.randn(10, 28, 28).astype(np.float32)
        y = np.zeros(10, dtype=int)

        clf.fit(X, y)
        assert len(clf.class_profiles) == 1
        assert 0 in clf.class_profiles

    def test_similarity_computed_correctly(self):
        """Test that the _similarity method produces valid scores."""
        clf = UniversalGeometricClassifier(n_thresholds=50)

        # Create profiles manually
        hist1 = np.random.rand(50)
        hist2 = np.random.rand(50)
        profile1 = GeometricProfile(
            binary_histogram=hist1,
            jump_events=[],
            betti_signature=np.zeros(10),
            capacity=1.0,
            phase_signature=np.zeros(10),
        )
        profile2 = GeometricProfile(
            binary_histogram=hist2,
            jump_events=[],
            betti_signature=np.zeros(10),
            capacity=1.0,
            phase_signature=np.zeros(10),
        )

        score = clf._similarity(profile1, profile2)
        assert isinstance(score, float)

    def test_similarity_identical_profiles(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        hist = np.random.rand(50)
        profile = GeometricProfile(
            binary_histogram=hist,
            jump_events=[],
            betti_signature=np.zeros(10),
            capacity=1.0,
            phase_signature=np.zeros(10),
        )

        score = clf._similarity(profile, profile)
        assert score > 0.5  # Should be high for identical profiles

    def test_fit_with_many_samples_per_class(self):
        clf = UniversalGeometricClassifier(n_thresholds=50)
        X = np.random.randn(100, 28, 28).astype(np.float32)
        y = np.array([0] * 50 + [1] * 50)

        clf.fit(X, y)
        assert len(clf.class_profiles) == 2
