# Eugenia Architecture Guide

## Overview

Eugenia is a deterministic knowledge system that transforms neural network weights into structured, interpretable patterns using SVD decomposition and geometric analysis.

## Core Architecture

### 1. NEED_REWRITE → src/nucleus

The `src/nucleus/` directory contains the heart of EUGENIA:

| Module | Purpose | Key Classes |
|--------|---------|-------------|
| `deterministic_core.py` | Pattern extraction from weights | `DeterministicKnowledgeCore`, `SemanticPattern`, `PatternRelationship` |
| `universal_knowledge_map.py` | Compressed knowledge storage (111GB → 50MB) | `UniversalKnowledgeMap`, `KnowledgeNavigator` |
| `eugenia_knowledge_system.py` | Data absorption & generation | `KnowledgeSystem`, `GeometricExtractor`, `PatternNode` |
| `knowledge_graph.py` | Pattern graph with auto-connections | `KnowledgeGraph` |
| `correlation_compressor.py` | SVD weight compression | `CorrelationCompressor` |
| `eugenia_seed_system.py` | Correlation seed system | `Seed`, `CorrelationEngine`, `Explorer` |

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
from src.nucleus import (
    DeterministicKnowledgeCore,
    UniversalKnowledgeMap,
    KnowledgeSystem,
    CorrelationCompressor,
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
```

## Configuration

### Environment Variables (.env)

Copy `.env.example` to `.env`:

```bash
make local-env
```

Key variables:
- `LLM_API_URL`: Local LLM endpoint (default: `http://localhost:11434/api/generate`)
- `LLM_MODEL`: Model name (default: `llama2`)
- `LOG_LEVEL`: DEBUG/INFO/WARNING/ERROR
- `CACHE_DIR`: Intermediate results cache
- `OUTPUT_DIR`: Generated files output

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
/workspace/
├── src/
│   ├── nucleus/            # 🔥 KEY CORE (ex-NEED_REWRITE)
│   ├── core/               # Sweep algorithms
│   ├── data/               # Loaders (MNIST, PNG, CMYK)
│   ├── models/             # Config & types
│   ├── renderers/          # Visualization modules
│   ├── utils/              # Path helpers
│   └── orchestrator.py     # Main coordinator
├── tests/
├── .env.example
├── pyproject.toml
└── AGENTS.md              # This file
```

## Troubleshooting

### Import Errors

Ensure `src/` is in PYTHONPATH or install in editable mode:
```bash
pip install -e .
```

### GPU Memory Issues

Reduce `num_workers` in `run_all_visualizations()` or set environment variable:
```bash
export VIZ_WORKERS=4
```

### Module Not Found

Check that imports use absolute paths from `src/`:
```python
from src.nucleus import DeterministicKnowledgeCore  # ✓
from nucleus import ...  # ✗ (unless installed)
```
