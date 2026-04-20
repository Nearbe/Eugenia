# MNIST 100% 10 samples.

[![Easy](easy_mnist.png)](easy_mnist.png)

This repository contains a high-performance visualization pipeline for analyzing the topological features of images
using a **Delta Field** transformation and threshold sweep algorithm.

[![Easy](easy_mnist_animation.gif)](easy_mnist_animation.gif)

## Overview

The core objective is to map image pixel values $X \in [0, 255]$ into a continuous real-valued "delta
field" $D \in [-5.546, 5.546]$, then perform a high-resolution threshold sweep to identify "jump events" where the
connectivity and occupancy of the image change significantly.

### Key Mathematical Concept: Delta Field

The transformation is defined as:
$$D = \log(X + 1) - \log(256 - X)$$

Key properties:

- $\log(1) - \log(256) \approx -5.545$
- $\log(256) - \log(1) \approx 5.545$
- Values centered around 0 represent mid-gray contrast.
- Positive values represent brighter-than-mid-gray regions, and negative values represent darker-than-mid-gray regions.

## Stack & Prerequisites

- **Python**: 3.11+ (target version in ruff/mypy config)
- **Primary Framework**: PyTorch (with Apple Metal Performance Shaders (MPS) support for macOS acceleration)
- **Key Dependencies**:
    - `numpy`, `scipy`, `matplotlib`, `Pillow`
    - `torch`
    - `scikit-learn` (for t-SNE)

## Installation

Create a virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install torch numpy scipy matplotlib Pillow scikit-learn
```

## Data Setup

The pipeline supports four primary data sources, each requiring specific files:

1. **MNIST**: Requires `data/mnist.npz` (with `x_train` and `y_train`).
2. **Fashion-MNIST**: Requires `data/fashion_mnist.npz` (same format as MNIST).
3. **PNG**: Expects image files (e.g., `eng_alphabetical.jpg`, `Rus-alfabita.png`) in the project root. Extracted via
   connected components.
4. **CMYK**: Reads `Eugene_cmyk.tiff` from the project root — 4 channels (C, M, Y, K) treated as separate classes.

> Datasets can also be loaded from a custom path via the `VIZ_DATA_DIR` environment variable.

## Usage

The main entry point is `generate.py`. It handles orchestration, source selection, and parallel processing.

```bash
# Generate for all sources (mnist, png, cmyk, fashion)
python3 generate.py

# Generate for a single source
python3 generate.py --source mnist
python3 generate.py --source png --file eng_alphabetical
python3 generate.py --source cmyk
python3 generate.py --source fashion

# Run sources in parallel (faster on multi-core CPUs)
python3 generate.py --parallel

# Limit parallel workers
python3 generate.py --parallel --workers 4

# Custom sweep parameters
python3 generate.py --source mnist --sweep-min -6.0 --sweep-max 6.0 --sweep-step 0.0005 --jump-threshold 0.5

# Run specific renderers only
python3 generate.py --source mnist --renderers betti_0_components,tsne_analysis
```

### CLI Arguments

- `--source`: Specify the data source (`mnist`, `png`, `cmyk`, `fashion`, or `all`). Default: `all`.
- `--file`: Optional specific file to use for the `png` source (e.g., `eng_alphabetical`, `Rus-alfabita`).
- `--parallel`: Use `ProcessPoolExecutor` to run multiple sources in parallel.
- `--workers`: Number of parallel workers for rendering (default: auto-detected).
- `--sweep-min`: Minimum threshold value for sweep.
- `--sweep-max`: Maximum threshold value for sweep.
- `--sweep-step`: Step size for sweep thresholds.
- `--jump-threshold`: Jump detection threshold in percent.
- `--renderers`: Comma-separated list of renderer names to run (e.g., `betti_0_components,tsne_analysis`).

## Output Structure

Results are saved to `output/{source}/`. Each run generates **23 visualization files** (22 PNG + 1 GIF) per source:

- **delta_histograms_by_class.png**: Distribution of delta values per class.
- **horizon_scan_heatmap.png**: 2D heatmaps of the delta field for all classes.
- **horizon_scan_animation.gif**: Animated threshold sweep across the delta field.
- **mean_std_analysis.png**: Statistical distribution of delta values.
- **jump_analysis.png**: Detection of significant occupancy changes between threshold steps.
- **tsne_analysis.png**: t-SNE visualization of binary occupancy profiles.
- **surface_3d_projection.png**: 3D mesh representation of the delta field.
- **cumulative_distribution.png**: Cumulative distribution functions of delta values.
- **topological_entropy.png**: Shannon entropy across the threshold sweep.
- **symbol_grid.png**: Visual grid of source symbols.
- **betti_0_components.png**: Betti-0 number (connected components) persistence.
- **betti_1_holes.png**: Betti-1 number (holes) persistence.
- **euler_characteristic.png**: Euler characteristic and topological complexity curves.
- **persistence_landscape.png**: Topological landscapes across the sweep.
- **gradient_stress.png**: Gradient magnitude and localized "stress" in the delta field.
- **phase_volume.png**: Analysis of state transition volumes in the delta field.
- **class_correlation.png**: Correlation between class labels and delta values.
- **individual_histograms/**: Directory with individual high-resolution histograms for each symbol.
- **jump_footprint.png**: Jump event footprint analysis.
- **noise_robustness.png**: Noise robustness testing results.
- **topological_capacity.png**: Topological capacity analysis.
- **threshold_comparison.png**: Threshold comparison visualization.
- **summary_dashboard.png**: Summary dashboard of all metrics.

> Note: `threshold_comparison.py` and `summary_dashboard.py` are excluded from mypy type checking.

## Project Structure

```text
.
├── AGENTS.md           # Advanced developer guide
├── generate.py         # Main entry point (CLI)
├── pyproject.toml      # Project metadata, deps, tool config
├── output/             # Generated visualizations
├── src/                # Core logic and visualization modules
│   ├── orchestrator.py     # Pipeline orchestration
│   ├── core/               # Sweep algorithms, math utilities, delta operations (21 modules)
│   │   ├── sweep.py
│   │   ├── division.py (safe_divide)
│   │   ├── potential.py (resolve_potential)
│   │   ├── delta.py
│   │   └── ... (17 more modules)
│   ├── data/               # Data loaders (MNIST, PNG, CMYK)
│   │   └── loaders.py
│   ├── models/             # Configuration & types
│   │   ├── config.py
│   │   └── types.py
│   ├── nucleus/            # Deterministic knowledge system
│   ├── utils/              # Shared utilities
│   │   ├── image_utils.py  # Image processing
│   │   ├── viz_utils.py    # Plotting & visualization
│   │   ├── path_utils.py   # Path management
│   │   ├── tensor_utils.py # Tensor manipulations
│   │   ├── delta_precompute.py
│   │   ├── clean_output.py
│   │   └── metrics.py          # Performance timing decorators
│   └── renderers/          # Visualization modules (22 files)
├── tests/                # Unit & integration tests
├── data/                 # Dataset files (mnist.npz, etc.)
└── venv/                 # Python virtual environment
```

## Project Architecture

- `generate.py`: CLI entry point. Parses arguments, spawns subprocesses for each source.
- `src/orchestrator.py`: Orchestrates loading, sweeping, and rendering. Uses global caching (`_cached_data`,
  `_cached_sweep`).
- `src/core/sweep.py`: Core algorithm for thresholding the delta field at high resolution (~111k steps).
- `src/core/division.py` (`safe_divide`), `src/core/potential.py` (`resolve_potential`): Low-level math utilities.
- `src/data/loaders.py`: Source-specific data loading (MNIST, Fashion-MNIST, PNG extraction via connected components,
  CMYK channel separation).
- `src/models/config.py`: Central `CONFIG` dataclass containing all numeric constants and visualization parameters.
- `src/models/types.py`: Typed dataclasses (`VisualizationData`, `SweepResults`).
- `src/nucleus/`: Deterministic knowledge system (pattern extraction, SVD compression, seed systems).
- `src/utils/image_utils.py`: Image processing and color conversions.
- `src/utils/viz_utils.py`: Matplotlib plotting and visualization helpers.
- `src/utils/path_utils.py`: Path and directory management.
- `src/utils/tensor_utils.py`: PyTorch tensor padding and utilities.
- `src/utils/delta_precompute.py`: Pre-computation of delta fields for performance.
- `src/renderers/*.py`: 23 visualization modules, each exporting a `render(data, sweep, out_dir)` function.

## Environment Variables

The pipeline uses the following internal environment variables (set automatically by `generate.py`):

- `VIZ_SOURCE`: Data source (`mnist`, `png`, `cmyk`, `fashion`).
- `VIZ_SOURCE_FILE`: Specific filename for the `png` source.
- `VIZ_OUTPUT_DIR`: Directory where visualizations will be saved.
- `VIZ_DATA_DIR`: Custom path for the `data/` directory containing dataset files.
- `PYTHONPATH`: Auto-set by `generate.py` to include `src/`.

## Testing

Verify the core math engine and sweep logic using pytest:

```bash
pytest tests/
```

## Automation

Common commands (no Makefile present):

- **Setup**: `python3 -m venv venv && source venv/bin/activate && pip install -e ".[dev]"`
- **Test**: `pytest tests/`
- **Run all**: `python3 generate.py`
- **Lint**: `ruff check .`
- **Format**: `ruff format .`
- **Typecheck**: `mypy src/`
- **Clean**: `rm -rf output/ __pycache__`

## IDE Integration

This project includes JetBrains IDE configuration:

- **Project Structure**: `src` and `tests` directories are properly marked for optimal indexing.
- **Excluded Folders**: `output`, `venv`, and `.idea` folders are excluded from indexing.

## License

This project is licensed under the CC-BY-NC 4.0 International License - see the [LICENSE.md](LICENSE.md) file for
details.
