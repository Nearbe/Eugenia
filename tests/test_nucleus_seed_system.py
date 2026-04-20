#!/usr/bin/env python3
"""
Tests for src/nucleus/nucleus_seed_system.py

Covers: Seed dataclass, CorrelationEngine, Explorer, BASE_SEEDS.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nucleus.nucleus_seed_system import (
    Seed,
    CorrelationEngine,
    Explorer,
    BASE_SEEDS,
)


# ============================================================
# BASE_SEEDS
# ============================================================


class TestBaseSeeds:
    def test_all_seed_names_present(self):
        expected_names = {
            "point",
            "line",
            "angle",
            "plane",
            "circle",
            "square",
            "triangle",
            "sphere",
            "chain",
            "tree",
            "ring",
            "net",
        }
        assert set(BASE_SEEDS.keys()) == expected_names

    def test_seed_vectors_are_ndarray(self):
        for name, vec in BASE_SEEDS.items():
            assert isinstance(vec, np.ndarray)

    def test_seed_vectors_same_length(self):
        lengths = [len(v) for v in BASE_SEEDS.values()]
        assert all(l == lengths[0] for l in lengths)

    def test_seed_vectors_non_zero_norm(self):
        for name, vec in BASE_SEEDS.items():
            assert np.linalg.norm(vec) > 0

    def test_seed_vectors_sum_to_nonzero(self):
        for name, vec in BASE_SEEDS.items():
            assert np.sum(vec) != 0


# ============================================================
# Seed dataclass
# ============================================================


class TestSeed:
    def test_creation(self):
        vec = np.array([1.0, 0.0, 0.0])
        seed = Seed(
            seed_id="test",
            representation=vec,
            description="test seed",
            basic=True,
        )
        assert seed.seed_id == "test"
        assert np.array_equal(seed.representation, vec)
        assert seed.description == "test seed"
        assert seed.basic is True

    def test_default_basic(self):
        seed = Seed(
            seed_id="test",
            representation=np.array([1.0]),
            description="test",
        )
        assert seed.basic is True


# ============================================================
# CorrelationEngine
# ============================================================


class TestCorrelationEngine:
    def test_init_default_dim(self):
        engine = CorrelationEngine()
        assert engine.base_dim == 4
        assert len(engine.seeds) == len(BASE_SEEDS)

    def test_init_custom_dim(self):
        engine = CorrelationEngine(base_dim=8)
        assert engine.base_dim == 8

    def test_all_seeds_registered(self):
        engine = CorrelationEngine()
        for name in BASE_SEEDS:
            assert name in engine.seeds

    def test_seed_has_description(self):
        engine = CorrelationEngine()
        for name, seed in engine.seeds.items():
            assert seed.description != ""
            assert isinstance(seed.description, str)

    def test_seed_is_basic(self):
        engine = CorrelationEngine()
        for name, seed in engine.seeds.items():
            assert seed.basic is True

    def test_get_correlation_same_seed(self):
        engine = CorrelationEngine()
        corr = engine.get_correlation("point", "point")
        assert abs(corr - 1.0) < 1e-6

    def test_get_correlation_orthogonal_seeds(self):
        engine = CorrelationEngine()
        # point = [1,0,0,0], line = [0,1,0,0]
        corr = engine.get_correlation("point", "line")
        assert abs(corr) < 1e-6  # Should be ~0

    def test_get_correlation_range(self):
        engine = CorrelationEngine()
        for a in BASE_SEEDS:
            for b in BASE_SEEDS:
                corr = engine.get_correlation(a, b)
                assert -1.0 <= corr <= 1.0 + 1e-6  # floating point tolerance

    def test_get_correlation_symmetric(self):
        engine = CorrelationEngine()
        for a in BASE_SEEDS:
            for b in BASE_SEEDS:
                corr_ab = engine.get_correlation(a, b)
                corr_ba = engine.get_correlation(b, a)
                assert abs(corr_ab - corr_ba) < 1e-6

    def test_get_correlation_unknown_pattern(self):
        engine = CorrelationEngine()
        # Unknown patterns get hashed vector
        corr = engine.get_correlation("point", "unknown_pattern_xyz")
        assert isinstance(corr, float)
        assert -1.0 <= corr <= 1.0

    def test_get_correlation_both_unknown(self):
        engine = CorrelationEngine()
        corr = engine.get_correlation("unknown_a", "unknown_b")
        assert isinstance(corr, float)

    def test_expand_seed_basic(self):
        engine = CorrelationEngine()
        results = engine.expand_seed("point", depth=2)

        assert isinstance(results, list)
        for name, corr in results:
            assert isinstance(name, str)
            assert isinstance(corr, float)

    def test_expand_seed_excludes_self(self):
        engine = CorrelationEngine()
        results = engine.expand_seed("point", depth=2)
        names = [name for name, _ in results]
        assert "point" not in names

    def test_expand_seed_sorted_by_abs_correlation(self):
        engine = CorrelationEngine()
        results = engine.expand_seed("point", depth=3)
        abs_corrs = [abs(corr) for _, corr in results]
        for i in range(len(abs_corrs) - 1):
            assert abs_corrs[i] >= abs_corrs[i + 1] - 1e-6

    def test_expand_seed_few_results(self):
        engine = CorrelationEngine()
        results = engine.expand_seed("point", depth=1)
        # Only a few seeds will have |corr| > 0.1
        assert len(results) <= len(BASE_SEEDS) - 1

    def test_find_bridges_basic(self):
        engine = CorrelationEngine()
        result = engine.find_bridges("point", "line", max_hops=3)

        assert "from" in result
        assert "to" in result
        assert "bridges" in result
        assert "strength" in result
        assert "common_count" in result
        assert result["from"] == "point"
        assert result["to"] == "line"

    def test_find_bridges_same_seed(self):
        engine = CorrelationEngine()
        result = engine.find_bridges("point", "point", max_hops=3)
        assert result["from"] == "point"
        assert result["to"] == "point"

    def test_find_bridges_common_count(self):
        engine = CorrelationEngine()
        result = engine.find_bridges("point", "line", max_hops=3)
        assert isinstance(result["common_count"], int)
        assert result["common_count"] >= 0


# ============================================================
# Explorer
# ============================================================


class TestExplorer:
    def test_init(self):
        explorer = Explorer()
        assert isinstance(explorer.engine, CorrelationEngine)
        assert explorer.found_correlations == {}
        assert explorer.explored_seeds == set()

    def test_explore_from_basic(self):
        explorer = Explorer()
        results = explorer.explore_from("point", depth=2)

        assert isinstance(results, dict)
        for target, data in results.items():
            assert "correlation" in data
            assert "is_seed" in data

    def test_explore_from_tracks_explored(self):
        explorer = Explorer()
        explorer.explore_from("point", depth=2)
        assert "point" in explorer.explored_seeds

    def test_explore_from_stores_correlations(self):
        explorer = Explorer()
        explorer.explore_from("point", depth=2)

        assert len(explorer.found_correlations) > 0
        for (a, b), corr in explorer.found_correlations.items():
            assert isinstance(corr, float)

    def test_explore_from_multiple_times(self):
        explorer = Explorer()
        explorer.explore_from("point", depth=2)
        count1 = len(explorer.explored_seeds)

        explorer.explore_from("point", depth=2)
        count2 = len(explorer.explored_seeds)
        assert count1 == count2  # No double counting

    def test_explore_from_different_seeds(self):
        explorer = Explorer()
        explorer.explore_from("point", depth=2)
        explorer.explore_from("circle", depth=2)

        assert "point" in explorer.explored_seeds
        assert "circle" in explorer.explored_seeds

    def test_discover_path_direct(self):
        explorer = Explorer()
        # Find a pair with high correlation for direct path
        path = explorer.discover_path("point", "plane")
        assert isinstance(path, list)
        if path:
            assert isinstance(path[0], tuple)
            assert len(path[0]) == 2

    def test_discover_path_returns_list(self):
        explorer = Explorer()
        path = explorer.discover_path("point", "sphere")
        assert isinstance(path, list)

    def test_query_basic(self):
        explorer = Explorer()
        result = explorer.query("point")

        assert "concept" in result
        assert "correlations" in result
        assert "seed_bridges" in result
        assert "path_to" in result
        assert result["concept"] == "point"

    def test_query_returns_seed_bridges_sorted(self):
        explorer = Explorer()
        result = explorer.query("point")

        bridges = result["seed_bridges"]
        if len(bridges) > 1:
            abs_corrs = [abs(corr) for _, corr in bridges]
            for i in range(len(abs_corrs) - 1):
                assert abs_corrs[i] >= abs_corrs[i + 1] - 1e-6

    def test_query_unknown_concept(self):
        explorer = Explorer()
        result = explorer.query("unknown_concept_xyz")

        assert result["concept"] == "unknown_concept_xyz"
        assert isinstance(result["seed_bridges"], list)

    def test_deterministic_explore(self):
        explorer1 = Explorer()
        results1 = explorer1.explore_from("point", depth=2)

        explorer2 = Explorer()
        results2 = explorer2.explore_from("point", depth=2)

        for target in results1:
            assert target in results2
            assert abs(results1[target]["correlation"] - results2[target]["correlation"]) < 1e-6

    def test_deterministic_query(self):
        explorer1 = Explorer()
        result1 = explorer1.query("circle")

        explorer2 = Explorer()
        result2 = explorer2.query("circle")

        assert len(result1["seed_bridges"]) == len(result2["seed_bridges"])
        for (name1, corr1), (name2, corr2) in zip(result1["seed_bridges"], result2["seed_bridges"]):
            assert name1 == name2
            assert abs(corr1 - corr2) < 1e-6

    def test_explore_from_empty_result(self):
        """Test with a seed that has no correlations above threshold."""
        engine = CorrelationEngine()
        # Use a seed with very low correlation to others
        explorer = Explorer()
        # "net" might have low correlations
        results = explorer.explore_from("net", depth=1)
        assert isinstance(results, dict)
