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

- **Python**: 3.14+ (tested with 3.14)
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

The pipeline supports three primary data sources, each requiring specific files:

1. **MNIST**: Requires `../eugenia_data/mnist.npz` (with `x_train` and `y_train`).
2. **PNG**: Expects image files (e.g., `cyrillic.png`, `latin.png`) in the project root.
3. **CMYK**: Reads `Eugene.jpeg` from the project root and converts it to a CMYK TIFF (`src/Eugene_cmyk.tiff`).

## Usage

The main entry point is `generate.py`. It handles orchestration, source selection, and parallel processing.

```bash
# Generate for all sources (mnist, png, cmyk)
python3 generate.py

# Generate for a single source
python3 generate.py --source mnist
python3 generate.py --source png --file latin
python3 generate.py --source cmyk

# Run sources in parallel (faster on multi-core CPUs)
python3 generate.py --parallel
```

### CLI Arguments

- `--source`: Specify the data source (`mnist`, `png`, `cmyk`, or `all`). Default: `all`.
- `--file`: Optional specific file to use for the `png` source (e.g., `cyrillic`, `latin`).
- `--parallel`: Use `ProcessPoolExecutor` to run multiple sources in parallel.

## Output Structure

Results are saved to `output/{source}/`. Each run generates 17 different visualizations:

- **00a_delta_histograms_by_class.png**: Distribution of delta values per class.
- **01_horizon_heatmap.png**: 2D heatmaps of the delta field for all classes.
- **02_horizon_animation.gif**: Animated threshold sweep across the delta field.
- **03_scatter_mean_std.png**: Statistical distribution of delta values.
- **04_jumps_analysis.png**: Detection of significant occupancy changes between threshold steps.
- **05_tsne_binary_profiles.png**: t-SNE visualization of binary occupancy profiles.
- **06_3d_surface.png**: 3D mesh representation of the delta field.
- **07_cdf_by_class.png**: Cumulative distribution functions of delta values.
- **08_entropy_analysis.png**: Shannon entropy across the threshold sweep.
- **09_original_vs_binary.png**: Visual comparison between source images and thresholded binary masks.
- **10_betti0_components.png**: Betti-0 number (connected components) persistence.
- **11_betti1_holes.png**: Betti-1 number (holes) persistence.
- **12_euler_persistence_complexity.png**: Euler characteristic and topological complexity curves.
- **13_persistence_landscape.png**: Topological landscapes across the sweep.
- **14_stress_map.png**: Gradient magnitude and localized "stress" in the delta field.
- **15_phase_volume.png**: Analysis of state transition volumes in the delta field.
- **individual_hists/**: Individual high-resolution histograms for each symbol.

## Project Structure

```text
.
├── AGENTS.md           # Advanced developer guide
├── generate.py         # Main entry point
├── output/             # Generated visualizations
├── src/                # Core logic and visualization modules
│   ├── common.py       # Pipeline orchestration
│   ├── loaders.py      # Data ingestion
│   ├── params.py       # Configuration constants
│   ├── sweep.py        # Threshold sweep algorithm
│   ├── utils/          # Shared utilities
│   │   ├── image_utils.py  # Image processing
│   │   ├── viz_utils.py    # Plotting & visualization
│   │   ├── path_utils.py   # Path management
│   │   └── tensor_utils.py # Tensor manipulations
│   └── renderers/      # Visualization modules
└── venv/               # Python virtual environment
```

## Project Architecture

- `generate.py`: Unified entry point. Parses arguments and spawns subprocesses.
- `src/common.py`: Orchestrates loading, sweeping, and rendering.
- `src/loaders.py`: Source-specific data loading (MNIST, PNG extraction via connected components, CMYK channel
  separation).
- `src/params.py`: Central `CONFIG` dataclass containing all numeric constants and visualization parameters.
- `src/sweep.py`: Core algorithm for thresholding the delta field at high resolution (~111k steps).
- `src/utils/image_utils.py`: Image processing and color conversions.
- `src/utils/viz_utils.py`: Matplotlib plotting and visualization helpers.
- `src/utils/path_utils.py`: Path and directory management.
- `src/utils/tensor_utils.py`: PyTorch tensor padding and utilities.
- `src/renderers/*.py`: Individual visualization modules, each exporting a `render()` function.

## Environment Variables

The pipeline uses the following internal environment variables (set automatically by `generate.py`):

- `VIZ_SOURCE`: Data source (e.g., `mnist`, `png`, `cmyk`).
- `VIZ_SOURCE_FILE`: Specific filename for the `png` source.
- `VIZ_OUTPUT_DIR`: Directory where visualizations will be saved.

## Testing

Verify the core math engine and sweep logic using pytest:

```bash
pytest tests/
```

## IDE Integration

This project includes JetBrains IDE configuration:

- **Run Configurations**: Pre-defined configurations for all data sources and tests (found in
  `.idea/runConfigurations`).
    - `Generate ALL`: Runs the full pipeline.
    - `Generate MNIST/PNG/CMYK`: Source-specific runs.
    - `Lint Code (Ruff)`: Fast linting.
    - `Type Check (Mypy)`: Static analysis.
    - `Clean Output`: Deletes all generated files.
    - `Pytest in tests`: Runs all tests.
- **Project Structure**: `src` and `tests` directories are properly marked for optimal indexing and testing.
- **Excluded Folders**: `output`, `venv`, and `.idea` folders are excluded from indexing to improve performance.
- **Environment Variables**: Use `VIZ_DATA_DIR` to specify a custom location for the `eugenia_data` folder.

## Automation with Makefile

A `Makefile` is provided for common tasks:

- `make setup`: Set up virtual environment and install dependencies.
- `make test`: Run all tests.
- `make run-all`: Run the full visualization pipeline.
- `make lint`: Run Ruff linter.
- `make typecheck`: Run Mypy type checker.
- `make local-env`: Create `.env` from template for local LLM integration.
- `make clean`: Clear the `output/` directory.

## License

This project is licensed under the CC-BY-NC 4.0 International License - see the [LICENSE.md](LICENSE.md) file for
details.
