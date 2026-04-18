# Eugenia — Delta Field Visualization Pipeline

## Directory Overview

This project is a high-performance **topological image analysis pipeline** written in Python. It maps pixel intensity values into a continuous **"delta field"** using a logarithmic transformation, then performs a high-resolution threshold sweep (~111k steps) to detect topological "jump events" — moments where image connectivity and occupancy change significantly. The pipeline produces **22 distinct visualizations** per data source, covering histograms, heatmaps, Betti numbers, Euler characteristics, t-SNE embeddings, and more.

## Key Files

| File / Directory | Purpose |
|---|---|
| `generate.py` | CLI entry point — orchestrates source selection, parallel processing, and output |
| `src/orchestrator.py` | Core orchestration: data loading, sweep computation, dynamic renderer discovery |
| `src/core/math.py` | Low-level math utilities (safe division, normalization, potential resolution) |
| `src/core/sweep.py` | Threshold sweep algorithm — computes occupancy rates and jump events |
| `src/data/loaders.py` | Data ingestion: MNIST, Fashion-MNIST, PNG sprite sheets, CMYK channels |
| `src/models/config.py` | Central `CONFIG` dataclass — all numeric constants, visualization params, colors |
| `src/models/types.py` | Typed dataclasses: `VisualizationData`, `SweepResults` |
| `src/renderers/*.py` | 22 individual visualization modules, each with a `render(data, sweep, out_dir)` function |
| `src/utils/` | Image processing, path management, tensor padding, viz helpers, delta precompute |
| `tests/test_math.py` | Unit tests for delta field math and sweep logic |
| `tests/test_integration.py` | Integration tests |
| `pyproject.toml` | Project metadata, dependencies, ruff/mypy/pytest config |
| `Makefile` | Common tasks: setup, test, run, lint, typecheck, clean |
| `Eugene.jpeg` / `Eugene_cmyk.tiff` | Sample CMYK image for the `cmyk` data source |
| `eng_alphabetical.jpg` | Sample PNG sprite sheet for the `png` data source |
| `Dockerfile` | Container configuration |

## Project Architecture

```
Eugenia/
├── generate.py              # CLI: --source [mnist|png|cmyk|fashion] --parallel
├── src/
│   ├── orchestrator.py      # load_data() → compute_sweep() → run_all_visualizations()
│   ├── core/
│   │   ├── math.py          # safe_divide, normalize_vector_safe, resolve_potential
│   │   └── sweep.py         # compute_sweep(): histogram-based occupancy + jump detection
│   ├── data/
│   │   └── loaders.py       # load_mnist_data, load_fashion_data, load_png_image, load_cmyk_image
│   ├── models/
│   │   ├── config.py        # CONFIG dataclass (sweep params, colors, figure sizes, etc.)
│   │   └── types.py         # VisualizationData, SweepResults dataclasses
│   ├── renderers/           # 22 visualization modules (each exports render())
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
│   │   ├── topological_entropy.py
│   │   └── tsne_analysis.py
│   └── utils/
│       ├── clean_output.py
│       ├── delta_precompute.py
│       ├── image_utils.py
│       ├── path_utils.py
│       ├── tensor_utils.py
│       └── viz_utils.py
├── tests/
│   ├── test_math.py
│   └── test_integration.py
├── output/                  # Generated visualizations (gitignored)
├── data/ / eugenia_data/   # Dataset files (mnist.npz, fashion_mnist.npz, etc.)
└── venv/                    # Python virtual environment (gitignored)
```

### Core Algorithm

1. **Delta Field Transformation**: `D = log(X + 1) - log(256 - X)` maps pixel values X ∈ [0, 255] to D ∈ [-5.546, 5.546]
2. **Threshold Sweep**: ~111k threshold levels spanning the delta field range
3. **Occupancy Rates**: Histogram-based computation of % of pixels above each threshold per class
4. **Jump Detection**: Occupancy changes > 1% between adjacent thresholds flagged as events
5. **Dynamic Renderer Discovery**: All `src/renderers/*.py` modules are auto-discovered and executed in parallel

### Data Sources

| Source | Input | Classes |
|---|---|---|
| `mnist` | `eugenia_data/mnist.npz` | 10 digits |
| `fashion` | `eugenia_data/fashion_mnist.npz` | 10 clothing categories |
| `png` | `Eugene.jpeg` (or `--file latin/cyrillic`) | Extracted via connected components |
| `cmyk` | `Eugene_cmyk.tiff` | 4 channels (C, M, Y, K) |

## Building and Running

### Setup
```bash
make setup          # Create venv + install deps (including dev)
```

### Run Pipeline
```bash
make run-all        # Full pipeline for all sources
python3 generate.py --source mnist    # Single source
python3 generate.py --source png --file latin   # PNG with specific file
python3 generate.py --parallel        # Parallel execution across sources
python3 generate.py --renderers betti_0_components,tsne_analysis  # Selective renderers
```

### Custom Sweep Parameters
```bash
python3 generate.py --sweep-min -6.0 --sweep-max 6.0 --sweep-step 0.0005 --jump-threshold 0.5
```

### Testing
```bash
make test           # Run pytest
python3 -m pytest tests/ -v
```

### Code Quality
```bash
make lint           # Ruff check
make format         # Ruff format
make typecheck      # Mypy
```

### Clean
```bash
make clean          # Remove output/ and __pycache__
```

## Data Directory

Datasets are loaded from `eugenia_data/` (or a custom path via `VIZ_DATA_DIR` env var). Required files:

- `mnist.npz` — must contain `x_train` and `y_train` keys
- `fashion_mnist.npz` — same format

## Environment Variables

| Variable | Purpose |
|---|---|
| `VIZ_SOURCE` | Data source: `mnist`, `png`, `cmyk`, `fashion` |
| `VIZ_SOURCE_FILE` | Specific file for `png` source |
| `VIZ_OUTPUT_DIR` | Output directory for visualizations |
| `VIZ_DATA_DIR` | Custom path to `eugenia_data/` directory |
| `PYTHONPATH` | Auto-set by `generate.py` to include `src/` |

## Development Conventions

- **Python 3.14+** required (target version in ruff/mypy config)
- **PyTorch** with MPS (macOS) or CUDA acceleration for tensor computations
- **Line length**: 100 characters (ruff config)
- **Typing**: `disallow_untyped_defs = false` but `check_untyped_defs = true`
- **Imports**: Uses absolute imports via `eugenia.` package prefix (e.g., `from core.sweep import ...`)
- **Caching**: Global `_cached_data` and `_cached_sweep` in `orchestrator.py` prevent redundant computation within a session
- **Parallel rendering**: `ProcessPoolExecutor` with up to 8 workers for visualization modules
- **Parallel sweep**: `ThreadPoolExecutor` for per-class histogram computation (MPS falls back to sequential)
- **Output**: 22 PNG/GIF files per source in `output/{source}/`
- **Comments**: Mix of English and Russian — Russian comments explain algorithmic rationale

## Adding a New Renderer

1. Create `src/renderers/my_new_plot.py`
2. Export a `render(data: VisualizationData, sweep: SweepResults, out_dir: str) -> None` function
3. Run `python3 generate.py` — the new renderer is auto-discovered

## Testing

- `tests/test_math.py` — Verifies delta field transformation and sweep logic
- `tests/test_integration.py` — End-to-end integration tests
- Run with: `make test` or `pytest tests/`

## Dependencies

**Runtime**: numpy, scipy, matplotlib, Pillow, torch, tqdm, scikit-learn
**Dev**: pytest, pytest-mpl, ruff, mypy
