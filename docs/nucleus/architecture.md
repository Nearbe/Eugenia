# Nucleus Architecture

## Module Map

Based on actual code in `src/nucleus/` (19 Python modules):

### Group 1: Core Pattern Extraction

| Module                       | Classes                                                                       | Purpose                                                                                                                                                                                                    |
|------------------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `deterministic_core.py`      | `SemanticPattern`, `PatternRelationship`, `DeterministicKnowledgeCore`        | Extract eigenpatterns from weight matrices via SVD. `learn(weights)` → patterns + relationships. `forward(input, layer)` → deterministic projection. Includes `serialize()`/`deserialize()` binary format. |
| `deterministic_knowledge.py` | `DeterministicPattern`, `DeterministicKnowledgeCore`, `DeterministicFunction` | Duplicate/alternative core with `fit(weights)`, `__call__(x)`, `verify(x, n)`. Provides `DeterministicFunction` wrapper interface.                                                                         |

### Group 2: Universal Knowledge Map & Protocol

| Module                            | Classes                                       | Purpose                                                                                                                                                                                                                                                              |
|-----------------------------------|-----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `universal_knowledge_map.py`      | `UniversalKnowledgeMap`, `KnowledgeNavigator` | Projects any input through learned pattern matrix: `project(x) = P^T @ x * s`. Computes semantic similarity via cosine in pattern space. `KnowledgeNavigator` adds `find_similar()`, `cluster()`, `dimension_analysis()`.                                            |
| `universal_knowledge_protocol.py` | `UniversalMap`, `UniversalKnowledgeProtocol`  | Layer-specific universal maps. `learn(weights)` → maps per layer. `encode(layer, x)` → k-dim pattern. `similarity(layer, x1, x2)` → cosine similarity. Uses `safe_divide`/`has_potential`/`resolve_potential` from `core.math`. Has `save()`/`load()` serialization. |

### Group 3: Knowledge System

| Module                        | Classes                                                | Purpose                                                                                                                                                                                                                                                                                   |
|-------------------------------|--------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `nucleus_knowledge_system.py` | `PatternNode`, `GeometricExtractor`, `KnowledgeSystem` | Core absorption/generation system. `GeometricExtractor.extract(data)` → binary sweep + jump events + topology profile. `KnowledgeSystem.absorb(data)` → creates node. `generate(context)` → finds related nodes. `strengthen(node_id)` → boosts on use. Auto-relates nodes by similarity. |
| `nucleus_unified.py`          | `NucleusUnified`, `TaskMode`, `NucleusState`           | Unified system combining pattern extraction, geometric engine, and duality. `load_model(path)` → extracts patterns. `generate(prompt, mode)` → renders via fractal engine. `learn_from_feedback(success)` → boosts correlations.                                                          |
| `nucleus_hybrid.py`           | `HybridProcessor`, `Mode`                              | DET/RND/HYBRID mode system. `compute_correlation()` varies by mode. `find_path()` varies by mode. DET = deterministic, RND = random variation, HYBRID = combination.                                                                                                                      |
| `nucleus_duality.py`          | `DualState`, `UnifiedSystem`                           | Omega (Ω, potential) ↔ Pi (Π, completeness) duality. `transition(input, exploration_factor)` → result + new state. `measure()` → current state snapshot. Uses `safe_divide`/`is_potential` from `core.math`.                                                                              |

### Group 4: Compressors

| Module                      | Classes                                                           | Purpose                                                                                                                                                                                                                                                                                   |
|-----------------------------|-------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `correlation_compressor.py` | `CorrelationCompressor`                                           | Four compression methods: (1) `compress_delta(W, init_type)` — delta from init, (2) `compress_correlation_svd(W, k)` — correlation SVD, (3) `compress_graph(W, threshold)` — sparse graph, (4) `compress_hessian_pattern(W)` — Hessian approximation. Has `decompress_correlation_svd()`. |
| `cross_layer_compressor.py` | `compress_layer()`, `decompress_layer()`, `cross_layer_pattern()` | Layer-level SVD compression. `compress_layer(W, k)` → `{U, S, Vt}` dict. `cross_layer_pattern(layer1, layer2, k)` → k×k cross-correlation matrix.                                                                                                                                         |
| `fractal_compressor.py`     | `RadicalCompressor`                                               | Iterative multi-level SVD. `levels=4, base_k=4` by default. Each level halves k. `compress(W)` → list of level dicts + first error. `decompress()` → reconstructed matrix.                                                                                                                |

### Group 5: Classifier

| Module                              | Classes                                                                  | Purpose                                                                                                                                                                                                                                                                                                                                   |
|-------------------------------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `universal_geometric_classifier.py` | `GeometricProfile`, `GeometricExtractor`, `UniversalGeometricClassifier` | Geometry-based few-shot classification. `GeometricExtractor.extract(data)` → `{binary_histogram, jump_events, betti_signature, capacity, phase_signature}`. `UniversalGeometricClassifier.fit(X, y)` → learns class profiles. `predict(x)` → class label. Uses weighted similarity: 0.4·histogram + 0.2·jumps + 0.3·betti + 0.1·capacity. |

### Group 6: Seed System

| Module                   | Classes                                 | Purpose                                                                                                                                                                                                                                                                                                                                                          |
|--------------------------|-----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `nucleus_seed_system.py` | `Seed`, `CorrelationEngine`, `Explorer` | Deterministic correlation-based pattern generation. `BASE_SEEDS` = 12 geometric primitives (point, line, angle, plane, circle, square, triangle, sphere, chain, tree, ring, net). `CorrelationEngine.get_correlation(a, b)` → cosine similarity. `find_bridges(from, to)` → common intermediate patterns. `Explorer.discover_path(from, to)` → path via bridges. |

### Group 7: Graphics

| Module                | Classes                                                             | Purpose                                                                                                                                                                                                                                                                                      |
|-----------------------|---------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `nucleus_graphics.py` | `GeometricProfile`, `RenderParams`, `GeometricEngine`, `RenderMode` | Geometric rendering engine. `GeometricEngine.register_profile(name, profile)` → stores profile. `render_fractal(formula, params, profile)` → renders mandelbrot/julia/burning_ship/newton. `compress_profiles(k)` → SVD basis. `generate_from_basis(coefficients)` → reconstruct from basis. |

### Group 8: Analysis

| Module                          | Classes                                                                                                                                                 | Purpose                                                                                                                                                                                                                                                                                                |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `nucleus_model_patterns.py`     | `ModelProfile`, `ModelLoader`, `PatternExtractor`                                                                                                       | Model weight loading (GGUF, MLX, safetensors, PyTorch). `ModelLoader.discover_models()` → list of model files. `load_safetensors(path)` → dict of layers. `PatternExtractor.extract_from_weights(W, name)` → `ModelProfile` with SVD. `get_pattern_geometry(profile)` → entropy, energy concentration. |
| `semantic_knowledge_storage.py` | `SemanticOperators`, `EigenPattern`, `SemanticPatternExtractor`, `KnowledgeGraph`, `SemanticRetrieval`, `RuntimeReconstructor`, `SemanticStorageFormat` | Semantic storage operators. ⚠️ `KnowledgeGraph` here builds a **multi-layer semantic graph** from all model weights (stores `EigenPattern` nodes). Different from `KnowledgeGraph` in `knowledge_graph.py` which works on a **single weight matrix** for eigenstructure extraction.                    |
| `llm_crisis_analysis.py`        | `LLMCrisisAnalysis`                                                                                                                                     | Static analysis class (no methods beyond `@staticmethod`). Analyzes LLM problems through geometric lens: tokenization, context window, understanding, computation. `new_architecture()` and `demonstration()` are standalone functions.                                                                |

## Data Flow

```
Input: Model weights (dict[str, np.ndarray])
    │
    ├─► [Pattern Extraction]
    │     CorrelationCompressor.compress_correlation_svd(W, k)
    │     → {U, S, Vt} per layer
    │
    ├─► [Compression]
    │     RadicalCompressor.compress(W)       → multi-level SVD
    │     cross_layer_pattern(layer1, layer2) → k×k cross-correlation
    │
    ├─► [Knowledge Graph]
    │     KnowledgeGraph.build_from_model(weights, k)
    │     → nodes (EigenPatterns) + edges (relationships)
    │
    ├─► [Universal Map]
    │     UniversalKnowledgeMap(P, S)
    │     → project(x) = P^T @ x * s
    │     → similarity(x1, x2) = cosine(project(x1), project(x2))
    │
    ├─► [Geometric Classifier]
    │     UniversalGeometricClassifier.fit(X, y)
    │     → class profiles (binary sweep + jump events + betti)
    │     predict(x) → nearest class profile
    │
    └─► [Seed System]
          CorrelationEngine.get_correlation(a, b)
          → deterministic cosine similarity
          Explorer.discover_path(from, to)
          → path via bridge patterns
```

## Serialization Formats

| Component                    | Format          | Details                                                                                                            |
|------------------------------|-----------------|--------------------------------------------------------------------------------------------------------------------|
| `DeterministicKnowledgeCore` | Binary (struct) | Header (d_model, k) → patterns (name, vector, singular, entropy, phase) → relationships (name, matrix) → signature |
| `UniversalKnowledgeProtocol` | Binary (struct) | Header (k) → maps (name, d, P, S) → signature                                                                      |
| `SemanticStorageFormat`      | Binary (struct) | Header (n_patterns) → patterns (singular, phase, entropy, vector) → edges → layer_index                            |

## Known Issues with AGENTS.md

The following are documented in AGENTS.md but **do not exist** in the current codebase:

1. **`src/extractors/gguf_extractor.py`** — Referenced in NUCLEUS_ROADMAP.md as "in progress" but not present in `src/`
2. **`src/extractors/__main__.py`** — Module entry point not present
3. **`src/extractors/cli_extract.py`** — CLI tool not present
4. **`src/nucleus/solenoid_encoder.py`** — P1 task, not implemented
5. **`src/nucleus/solenoid_engine.py`** — P1 task, not implemented
6. **`src/nucleus/graph_checkpoint.py`** — P2 task, not implemented
7. **`src/nucleus/persistent_storage.py`** — P2 task, not implemented
8. **`src/nucleus/graph_index.py`** — P2 task, not implemented
9. **`src/nucleus/gemma_nucleus_pipeline.py`** — P3 task, not implemented
10. **`src/nucleus/cli/extract_gemma.py`** — P3 task, not implemented
11. **`src/nucleus/gpu_accelerator.py`** — P4 task, not implemented
12. **`src/nucleus/cache_manager.py`** — P4 task, not implemented
13. **`src/nucleus/batch_processor.py`** — P4 task, not implemented
14. **`src/nucleus/multi_modal_input.py`** — P5 task, not implemented
15. **`src/nucleus/modal_fusion.py`** — P5 task, not implemented

AGENTS.md also references classes `DeterministicPattern` and `DeterministicFunction` from `deterministic_knowledge.py`
as if they are the primary classes, but `DeterministicKnowledgeCore` from `deterministic_core.py` is the one exported in
`__init__.py`.
