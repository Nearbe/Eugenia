# Eugenia — Delta Field Visualization & Deterministic Knowledge Pipeline

[![Easy](easy_mnist.png)](easy_mnist.png)
[![Easy](easy_mnist_animation.gif)](easy_mnist_animation.gif)

## Overview

Eugenia is a dual-purpose project combining:

1. **Delta Field Visualization Pipeline** — A high-performance topological image analysis system that maps pixel intensity
   values into a continuous "delta field" using a logarithmic transformation, then performs a high-resolution threshold
   sweep (~111k steps) to detect topological "jump events" — moments where image connectivity and occupancy change
   significantly. Produces **23 visualization modules** (22 PNG + 1 GIF) per data source.

2. **Deterministic Knowledge System (Nucleus)** — Transforms neural network weights into structured, interpretable
   patterns using SVD decomposition and geometric analysis. Compresses 111GB of weights into a 50MB knowledge map
   with deterministic pattern extraction.

## Key Mathematical Concept: Delta Field

The transformation maps image pixel values $X \in [0, 255]$ into a continuous real-valued delta field $D \in [-5.546, 5.546]$:

$$D = \log(X + 1) - \log(256 - X)$$

Key properties:

- $\log(1) - \log(256) \approx -5.545$ (darkest pixels)
- $\log(256) - \log(1) \approx 5.545$ (brightest pixels)
- Values centered around 0 represent mid-gray contrast
- Positive values = brighter-than-mid-gray regions; negative values = darker-than-mid-gray regions

## Core Algorithm

1. **Delta Field Transformation**: Maps pixel values X ∈ [0, 255] to D ∈ [-5.546, 5.546]
2. **Threshold Sweep**: ~111k threshold levels spanning the delta field range
3. **Occupancy Rates**: Histogram-based computation of % of pixels above each threshold per class
4. **Jump Detection**: Occupancy changes > 1% between adjacent thresholds flagged as events
5. **Dynamic Renderer Discovery**: All `src/renderers/*.py` modules are auto-discovered and executed in parallel

## Stack & Prerequisites

- **Python**: 3.11+
- **Primary Framework**: PyTorch (with Apple Metal Performance Shaders (MPS) support for macOS, or CUDA)
- **Runtime Dependencies**: numpy, scipy, matplotlib, Pillow, torch, tqdm, scikit-learn (for t-SNE)
- **Dev Dependencies**: pytest, pytest-mpl, ruff, mypy

## Installation

```bash
make setup          # Create venv + install deps (including dev)
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## Data Sources

| Source    | Input                                      | Classes                            |
|-----------|--------------------------------------------|------------------------------------|
| `mnist`   | `data/mnist.npz` (or set `VIZ_DATA_DIR`)  | 10 digits                          |
| `fashion` | `data/fashion_mnist.npz` (or set `VIZ_DATA_DIR`) | 10 clothing categories    |
| `png`     | `Eugene.jpeg` (or `--file latin/cyrillic`) | Extracted via connected components |
| `cmyk`    | `Eugene_cmyk.tiff`                         | 4 channels (C, M, Y, K)            |

> Datasets are loaded from `data/` (or a custom path via `VIZ_DATA_DIR` env var). Required files: `mnist.npz`
> (with `x_train` and `y_train` keys), `fashion_mnist.npz` (same format). Place these files in `data/` before running.

## Usage

### Run Pipeline

```bash
# Full pipeline for all sources
python3 generate.py

# Single source
python3 generate.py --source mnist
python3 generate.py --source png --file latin
python3 generate.py --source cmyk
python3 generate.py --source fashion

# Parallel execution across sources (faster on multi-core CPUs)
python3 generate.py --parallel
python3 generate.py --parallel --workers 4

# Custom sweep parameters
python3 generate.py --sweep-min -6.0 --sweep-max 6.0 --sweep-step 0.0005 --jump-threshold 0.5

# Run specific renderers only
python3 generate.py --renderers betti_0_components,tsne_analysis
```

> **Note**: No Makefile is included. Run code quality commands manually (see below).

### CLI Arguments

| Argument           | Description                                           |
|--------------------|-------------------------------------------------------|
| `--source`         | Data source: `mnist`, `png`, `cmyk`, `fashion`, `all` (default: `all`) |
| `--file`           | Specific file for `png` source (e.g., `eng_alphabetical`, `Rus-alfabita`) |
| `--parallel`       | Use `ProcessPoolExecutor` to run multiple sources in parallel |
| `--workers`        | Number of parallel workers for rendering (default: auto-detected) |
| `--sweep-min`      | Minimum threshold value for sweep                     |
| `--sweep-max`      | Maximum threshold value for sweep                     |
| `--sweep-step`     | Step size for sweep thresholds                        |
| `--jump-threshold` | Jump detection threshold in percent                   |
| `--renderers`      | Comma-separated list of renderer names to run         |

## Output Structure

Results are saved to `output/{source}/`. Each run generates **22 visualization files** (21 PNG + 1 GIF) per source:

| File                              | Description                                          |
|-----------------------------------|------------------------------------------------------|
| `delta_histograms_by_class.png`   | Distribution of delta values per class               |
| `horizon_scan_heatmap.png`        | 2D heatmaps of the delta field for all classes       |
| `horizon_scan_animation.gif`      | Animated threshold sweep across the delta field      |
| `mean_std_analysis.png`           | Statistical distribution of delta values             |
| `jump_analysis.png`               | Detection of significant occupancy changes           |
| `tsne_analysis.png`               | t-SNE visualization of binary occupancy profiles     |
| `surface_3d_projection.png`       | 3D mesh representation of the delta field            |
| `cumulative_distribution.png`     | Cumulative distribution functions of delta values    |
| `topological_capacity.png`        | Topological capacity analysis                        |
| `symbol_grid.png`                 | Visual grid of source symbols                        |
| `betti_0_components.png`          | Betti-0 number (connected components) persistence    |
| `betti_1_holes.png`               | Betti-1 number (holes) persistence                   |
| `euler_characteristic.png`        | Euler characteristic and topological complexity      |
| `persistence_landscape.png`       | Topological landscapes across the sweep              |
| `gradient_stress.png`             | Gradient magnitude and localized "stress"            |
| `phase_volume.png`                | State transition volumes in the delta field          |
| `class_correlation.png`           | Correlation between class labels and delta values    |
| `individual_histograms/`          | Directory with per-symbol high-resolution histograms |
| `jump_footprint.png`              | Jump event footprint analysis                        |
| `noise_robustness.png`            | Noise robustness testing results                     |
| `threshold_comparison.png`        | Threshold comparison visualization                   |
| `summary_dashboard.png`           | Summary dashboard of all metrics                     |

> Note: `threshold_comparison.py` and `summary_dashboard.py` are excluded from mypy type checking.

## Project Architecture

```
Eugenia/
├── generate.py              # CLI entry point (delta field pipeline)
├── pyproject.toml           # Project metadata, deps, tool config
├── README.md                # This file
├── output/                  # Generated visualizations (gitignored)
├── data/                    # Dataset files (place mnist.npz, fashion_mnist.npz here)
├── venv/                    # Python virtual environment (gitignored)
├── src/
│   ├── core/                # Sweep algorithms, math utilities, delta operations
│   │   ├── sweep.py         # compute_sweep(): histogram-based occupancy + jump detection
│   │   └── division.py      # safe_divide, div_safe
│   ├── data/                # Data loaders (MNIST, Fashion-MNIST, PNG, CMYK)
│   │   └── loaders.py
│   ├── extractors/          # GGUF/model weight extraction
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── cli_extract.py
│   │   ├── correlation_extractor.py
│   │   └── gguf_extractor.py
│   ├── models/              # Configuration & types
│   │   ├── config.py        # CONFIG dataclass (sweep params, colors, figure sizes)
│   │   └── types.py         # VisualizationData, SweepResults dataclasses
│   ├── nucleus/             # 🔥 Deterministic knowledge system (19 modules)
│   │   ├── __init__.py      # Package exports (all classes)
│   │   ├── deterministic_core.py
│   │   ├── universal_knowledge_map.py
│   │   ├── nucleus_knowledge_system.py
│   │   ├── knowledge_graph.py
│   │   ├── correlation_compressor.py
│   │   ├── nucleus_seed_system.py
│   │   ├── nucleus_unified.py
│   │   ├── nucleus_hybrid.py
│   │   ├── nucleus_duality.py
│   │   ├── nucleus_graphics.py
│   │   ├── nucleus_model_patterns.py
│   │   ├── deterministic_knowledge.py
│   │   ├── universal_geometric_classifier.py
│   │   ├── universal_knowledge_protocol.py
│   │   ├── semantic_knowledge_storage.py
│   │   ├── fractal_compressor.py
│   │   ├── cross_layer_compressor.py
│   │   ├── llm_crisis_analysis.py
│   │   └── nucleus_data/    # (internal, not listed individually)
│   ├── renderers/           # 21 visualization modules (each exports render())
│   │   ├── betti_0_components.py
│   │   ├── betti_1_holes.py
│   │   ├── class_correlation.py
│   │   ├── cumulative_distribution.py
│   │   ├── delta_histograms.py
│   │   ├── euler_characteristic.py
│   │   ├── gradient_stress.py
│   │   ├── horizon_scan_animation.py
│   │   ├── horizon_scan_heatmap.py
│   │   ├── individual_histograms.py
│   │   ├── jump_analysis.py
│   │   ├── jump_footprint.py
│   │   ├── mean_std_analysis.py
│   │   ├── noise_robustness.py
│   │   ├── persistence_landscape.py
│   │   ├── phase_volume.py
│   │   ├── summary_dashboard.py
│   │   ├── surface_3d_projection.py
│   │   ├── symbol_grid.py
│   │   ├── threshold_comparison.py
│   │   └── tsne_analysis.py
│   └── utils/               # Shared utilities
│       ├── image_utils.py   # Image processing & color conversions
│       ├── viz_utils.py     # Matplotlib plotting & visualization helpers
│       ├── path_utils.py    # Path & directory management
│       ├── tensor_utils.py  # PyTorch tensor padding & utilities
│       ├── delta_precompute.py
│       ├── clean_output.py
│       └── metrics.py       # Performance timing decorators
├── tests/                   # Unit & integration tests
│   ├── test_math.py
│   └── test_integration.py
└── .idea/                   # JetBrains IDE configuration
```

## Nucleus: Deterministic Knowledge System

### Key Principles

1. **Deterministic Patterns**: Instead of chaotic weights → deterministic eigenvectors
2. **Fixed Relationships**: Instead of static values → deterministic relationship matrices
3. **Model as Function**: The model becomes a deterministic function of patterns

### Data Flow

```
Weights (111GB)
    ↓ SVD
Patterns (k=32 per layer)
    ↓ Geometric Analysis
Topology Graph
    ↓ Correlation Engine
Seed System → Knowledge Generation
```

### API Usage

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
    KnowledgeNavigator,
    PatternNode, GeometricExtractor,
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

> **Note**: All nucleus classes are exported via `src/nucleus/__init__.py`. Import from `nucleus` (the package), not
> individual files.

## Environment Variables

### Pipeline Variables

| Variable          | Purpose                                        |
|-------------------|------------------------------------------------|
| `VIZ_SOURCE`      | Data source: `mnist`, `png`, `cmyk`, `fashion` |
| `VIZ_SOURCE_FILE` | Specific file for `png` source                 |
| `VIZ_OUTPUT_DIR`  | Output directory for visualizations            |
| `VIZ_DATA_DIR`    | Custom path to data directory            |
| `VIZ_WORKERS`     | Number of parallel workers (default: auto)     |
| `PYTHONPATH`      | Auto-set by `generate.py` to include `src/`    |

### Nucleus / LLM Variables

| Variable          | Purpose                                        |
|-------------------|------------------------------------------------|
| `LLM_API_URL`     | Local LLM endpoint (default: `http://localhost:11434/api/generate`) |
| `LLM_MODEL`       | Model name (default: `llama2`)                 |
| `LOG_LEVEL`       | DEBUG/INFO/WARNING/ERROR                       |
| `CACHE_DIR`       | Intermediate results cache directory           |
| `OUTPUT_DIR`      | Generated files output directory               |

Create `.env` manually if needed.

## Development

### Code Quality

```bash
ruff check .          # Lint
ruff format .         # Format
mypy src/             # Type check
pytest tests/         # Tests
```

### Adding New Components

**New Renderer** (delta field pipeline):
1. Create `src/renderers/my_new_plot.py`
2. Export a `render(data: VisualizationData, sweep: SweepResults, out_dir: str) -> None` function
3. Run `python3 generate.py` — the new renderer is auto-discovered

**New Module** (nucleus system):
Create a new Python file under `src/nucleus/` following the existing module conventions.

### Development Conventions

- **Line length**: 100 characters (ruff config)
- **Typing**: `disallow_untyped_defs = false` but `check_untyped_defs = true`
- **Imports**: Uses direct imports (e.g., `from core.sweep import ...`, `from data.loaders import ...`)
- **Caching**: Session-level cache prevents redundant computation within `generate.py`
- **Parallel rendering**: `ProcessPoolExecutor` with up to 8 workers for visualization modules
- **Parallel sweep**: `ThreadPoolExecutor` for per-class histogram computation (MPS falls back to sequential)
- **Comments**: Mix of English and Russian — Russian comments explain algorithmic rationale

## Performance Notes

- **SVD Parallelization**: Uses ProcessPoolExecutor for heavy computations
- **GPU Support**: Automatic CUDA/MPS detection in data loaders
- **Caching**: Global cache prevents re-loading data within session
- **Memory**: 8-worker limit prevents OOM with large datasets

## Testing

```bash
python3 -m pytest tests/ -v
```

- `tests/test_math.py` — Verifies delta field transformation and sweep logic
- `tests/test_integration.py` — End-to-end integration tests

## IDE Integration

This project includes JetBrains IDE configuration:

- **Project Structure**: `src` and `tests` directories are properly marked for optimal indexing.
- **Excluded Folders**: `output`, `venv`, and `.idea` folders are excluded from indexing.

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

### Module Not Found (Nucleus)

Import from the nucleus package (not `src.nucleus`):

```python
from nucleus import DeterministicKnowledgeCore  # ✓ correct
# from src.nucleus import ...  # ✗ incorrect — use nucleus package directly
```

## Clean

```bash
rm -rf output/ __pycache__
```

## License

This project is licensed under the CC-BY-NC 4.0 International License — see the [LICENSE.md](LICENSE.md) file for details.
