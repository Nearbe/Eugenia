# Eugenia Architecture Guide

## Overview

Eugenia is a deterministic knowledge system that transforms neural network weights into structured, interpretable
patterns using SVD decomposition and geometric analysis.

## Core Architecture

### 1. NEED_REWRITE → src/nucleus

The `src/nucleus/` directory contains the heart of EUGENIA:

| Module                              | Purpose                                     | Key Classes                                                                      |
|-------------------------------------|---------------------------------------------|----------------------------------------------------------------------------------|
| `deterministic_core.py`             | Pattern extraction from weights             | `DeterministicKnowledgeCore`, `SemanticPattern`, `PatternRelationship`           |
| `universal_knowledge_map.py`        | Compressed knowledge storage (111GB → 50MB) | `UniversalKnowledgeMap`, `KnowledgeNavigator`                                    |
| `nucleus_knowledge_system.py`       | Data absorption & generation                | `KnowledgeSystem`, `GeometricExtractor`, `PatternNode`                           |
| `knowledge_graph.py`                | Pattern graph with auto-connections         | `KnowledgeGraph`                                                                 |
| `correlation_compressor.py`         | SVD weight compression                      | `CorrelationCompressor`                                                          |
| `nucleus_seed_system.py`            | Correlation seed system                     | `Seed`, `CorrelationEngine`, `Explorer`                                          |
| `nucleus_unified.py`                | Unified nucleus processor                   | `NucleusUnified`, `TaskMode`, `NucleusState`                                     |
| `nucleus_hybrid.py`                 | Hybrid processing mode                      | `HybridProcessor`, `Mode`                                                        |
| `nucleus_duality.py`                | Dual-state nucleus                          | `UnifiedSystem`, `DualState`                                                     |
| `nucleus_graphics.py`               | Geometric rendering engine                  | `GeometricEngine`, `RenderParams`, `RenderMode`                                  |
| `nucleus_model_patterns.py`         | Model pattern extraction                    | `ModelProfile`, `ModelLoader`, `PatternExtractor`                                |
| `deterministic_knowledge.py`        | Deterministic knowledge representation      | `DeterministicPattern`, `DeterministicKnowledgeCore`, `DeterministicFunction`    |
| `universal_geometric_classifier.py` | Geometric classification                    | `UniversalGeometricClassifier`, `GeometricProfile`, `GeometricExtractor`         |
| `universal_knowledge_protocol.py`   | Knowledge protocol implementation           | `UniversalKnowledgeProtocol`, `UniversalMap`                                     |
| `semantic_knowledge_storage.py`     | Semantic storage operators                  | `SemanticOperators`, `EigenPattern`, `SemanticRetrieval`, `RuntimeReconstructor` |
| `fractal_compressor.py`             | Fractal/radial compression                  | `RadicalCompressor`                                                              |
| `llm_crisis_analysis.py`            | LLM crisis analysis                         | `LLMCrisisAnalysis`                                                              |

### 2. Key Principles

1. **Deterministic Patterns**: Instead of chaotic weights → deterministic eigenvectors
2. **Fixed Relationships**: Instead of static values → deterministic relationship matrices
3. **Model as Function**: The model becomes a deterministic function of patterns

### 3. Data Flow

```
Weights (111GB)
    ↓ SVD
Patterns (k=32 per layer)
    ↓ Geometric Analysis
Topology Graph
    ↓ Correlation Engine
Seed System → Knowledge Generation
```

## API Usage

```python
from nucleus import (
    DeterministicKnowledgeCore,
    UniversalKnowledgeMap,
    KnowledgeSystem,
    CorrelationCompressor,
    SemanticPattern,
    PatternRelationship,
    KnowledgeGraph,
    Seed, CorrelationEngine, Explorer,
    UniversalKnowledgeMap, KnowledgeNavigator,
    PatternNode, GeometricExtractor, KnowledgeSystem,
)

# Extract patterns from model weights
core = DeterministicKnowledgeCore(d_model=4096, k=32)
core.learn(weight_dict)

# Compress to universal map
mapper = UniversalKnowledgeMap()
compressed = mapper.compress(core.patterns)

# Generate new knowledge
system = KnowledgeSystem()
system.absorb(compressed)
new_patterns = system.generate(seed_vector)

# Use knowledge graph for pattern relationships
graph = KnowledgeGraph()
graph.add_pattern(SemanticPattern(...))
graph.connect(PatternRelationship(...))

# Use seed system for correlation-based generation
seed = Seed(...)
engine = CorrelationEngine(seed)
results = engine.process(data)

# Use explorer for advanced analysis
explorer = Explorer(engine)
analysis = explorer.analyze()
```

> **Note**: All nucleus classes are exported via `src/nucleus/__init__.py`. Import from `.nucleus` (the package), not
> individual files.

## Configuration

### Environment Variables (.env)

Create `.env` manually (or run `make local-env` which copies from template if present):

```bash
# If .env.example exists:
make local-env
# Otherwise, create .env manually with these variables:
```

Key variables:

- `LLM_API_URL`: Local LLM endpoint (default: `http://localhost:11434/api/generate`)
- `LLM_MODEL`: Model name (default: `llama2`)
- `LOG_LEVEL`: DEBUG/INFO/WARNING/ERROR
- `CACHE_DIR`: Intermediate results cache directory
- `OUTPUT_DIR`: Generated files output directory

> **Note**: `.env.example` is referenced by `make local-env` but may not exist in all repo versions. Create `.env`
> manually if needed.

### Python Version

Requires Python >= 3.11 (updated from incorrect 3.14 requirement)

## Development

### Setup

```bash
make setup      # Create venv and install dependencies
make lint       # Run ruff linter
make format     # Format code with ruff
make typecheck  # Run mypy type checker
make test       # Run pytest tests
```

### Adding New Modules

```bash
make generate-module name=my_module desc="My new module"
```

## Performance Notes

- **SVD Parallelization**: Uses ProcessPoolExecutor for heavy computations
- **GPU Support**: Automatic CUDA/MPS detection in orchestrator
- **Caching**: Global cache prevents re-loading data within session
- **Memory**: 8-worker limit prevents OOM with large datasets

## File Structure

```
.
├── AGENTS.md              # This file (architecture guide)
├── QWEN.md                # Delta field pipeline docs
├── README.md              # Project overview & usage
├── generate.py            # CLI entry point
├── pyproject.toml         # Project metadata & config
├── Makefile               # Common tasks
├── src/
│   ├── orchestrator.py    # Main coordinator (load → sweep → render)
│   ├── core/              # Sweep algorithms & math
│   │   ├── sweep.py
│   │   └── math.py
│   ├── data/              # Data loaders (MNIST, PNG, CMYK)
│   │   └── loaders.py
│   ├── models/            # Config & types
│   │   ├── config.py
│   │   └── types.py
│   ├── nucleus/           # 🔥 Deterministic knowledge system
│   │   ├── __init__.py    # Package exports (all classes)
│   │   ├── deterministic_core.py
│   │   ├── universal_knowledge_map.py
│   │   ├── nucleus_knowledge_system.py
│   │   ├── knowledge_graph.py
│   │   ├── correlation_compressor.py
│   │   ├── nucleus_seed_system.py
│   │   └── ... (16+ modules)
│   ├── renderers/         # Visualization modules (23 files)
│   └── utils/             # Shared utilities
│       ├── image_utils.py
│       ├── viz_utils.py
│       ├── path_utils.py
│       ├── tensor_utils.py
│       ├── delta_precompute.py
│       └── clean_output.py
├── tests/
├── output/                # Generated visualizations (gitignored)
└── venv/                  # Python virtual environment (gitignored)
```

## Troubleshooting

### Import Errors

Ensure `src/` is in PYTHONPATH (set by `generate.py`) or install in editable mode:

```bash
pip install -e .
```

### GPU Memory Issues

Reduce `num_workers` in `run_all_visualizations()` or set environment variable:

```bash
export VIZ_WORKERS=4
```

### Module Not Found

Import from the nucleus package (not `src.nucleus`):

```python
from nucleus import DeterministicKnowledgeCore  # ✓ correct
# from src.nucleus import ...  # ✗ incorrect — use nucleus package directly
```

> **Note**: All modules in `src/` are imported with direct paths (e.g., `from core.sweep import ...`,
`from data.loaders import ...`). The `src/` directory is added to PYTHONPATH automatically by `generate.py`.
