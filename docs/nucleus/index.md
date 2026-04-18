# Nucleus — Deterministic Knowledge System

## Overview

The Nucleus is a system for extracting, compressing, and navigating the **geometric structure** of neural network
weights. It replaces raw weight storage with a pattern-based representation.

## Core Concept

```
Raw weights (111GB)
    ↓ SVD decomposition
Eigenpatterns (U, S, Vt) — k << d
    ↓ Correlation analysis
Knowledge graph
    ↓ Compression
~50MB compressed pattern storage
```

Instead of storing `W ∈ R^(m×n)` directly, the system:

1. **Extracts** eigenpatterns via SVD: `W = U · Σ · V^T`
2. **Compresses** to top-k components: `W ≈ U_k · Σ_k · V_k^T`
3. **Builds** a correlation graph between patterns across layers
4. **Stores** the graph in a compact binary format

## Key Properties

| Property          | Description                                 |
|-------------------|---------------------------------------------|
| **Deterministic** | Same input → same output, always            |
| **Compressed**    | 111GB → ~50MB via SVD low-rank              |
| **Cross-modal**   | Works on any data type (text, image, audio) |
| **Few-shot**      | Classification with 1-10 examples per class |
| **Queryable**     | Pattern-based semantic search               |

## Public API

All public classes are exported via `src/nucleus/__init__.py`:

```python
from nucleus import (
    # Deterministic Core
    DeterministicKnowledgeCore,
    SemanticPattern,
    PatternRelationship,

    # Knowledge Map
    UniversalKnowledgeMap,
    KnowledgeNavigator,

    # Knowledge System
    KnowledgeSystem,
    PatternNode,
    GeometricExtractor,

    # Knowledge Graph
    KnowledgeGraph,

    # Correlation Compressor
    CorrelationCompressor,

    # Seed System
    Seed,
    CorrelationEngine,
    Explorer,
)
```

## Modules at a Glance

The nucleus consists of **19 Python modules** organized into 4 groups:

| Group              | Modules                                                                            | Purpose                                |
|--------------------|------------------------------------------------------------------------------------|----------------------------------------|
| **Core**           | `deterministic_core`, `deterministic_knowledge`                                    | Pattern extraction from weights        |
| **Map & Protocol** | `universal_knowledge_map`, `universal_knowledge_protocol`                          | Universal pattern projection           |
| **System**         | `nucleus_knowledge_system`, `nucleus_unified`, `nucleus_hybrid`, `nucleus_duality` | Knowledge absorption and generation    |
| **Compressors**    | `correlation_compressor`, `cross_layer_compressor`, `fractal_compressor`           | Weight compression strategies          |
| **Classifier**     | `universal_geometric_classifier`                                                   | Geometry-based few-shot classification |
| **Seed System**    | `nucleus_seed_system`                                                              | Correlation-based pattern generation   |
| **Graphics**       | `nucleus_graphics`                                                                 | Geometric rendering engine             |
| **Analysis**       | `nucleus_model_patterns`, `semantic_knowledge_storage`, `llm_crisis_analysis`      | Model analysis and LLM crisis study    |

## Architecture

See [Architecture](/nucleus/architecture/) for detailed module map and data flow.

## Module Reference

See [Modules](/nucleus/modules/) for per-module API documentation based on actual code.

## Name Collisions

Two pairs of classes share the same name across different modules. This is intentional — they serve different phases of
the pipeline:

### `KnowledgeGraph`

| Module                          | Role                                                                                                                       |
|---------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| `knowledge_graph.py`            | **Single matrix** — extracts eigenstructure from one weight matrix. Used for compression analysis.                         |
| `semantic_knowledge_storage.py` | **Multi-layer** — builds semantic graph from all model weights. Stores `EigenPattern` nodes. Used for knowledge retrieval. |

`__init__.py` exports the **single matrix** version.

### `GeometricExtractor`

| Module                              | Role                                                                                                                                    |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| `nucleus_knowledge_system.py`       | **Universal** — accepts any data type (strings, arrays, numbers), returns raw `np.ndarray` profile. Used by `KnowledgeSystem.absorb()`. |
| `universal_geometric_classifier.py` | **Array-only** — works on numpy arrays, returns `GeometricProfile` dataclass. Used by `UniversalGeometricClassifier.fit()`.             |

`__init__.py` exports the **universal** version.
