# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2026-04-16

### Added

- Added `class_correlation.py` renderer for topological similarity analysis between classes.
- Added `jump_footprint.py` renderer for spatial localization of significant topology changes.
- Added `scikit-learn` to project dependencies.

### Fixed

- Fixed invalid escape sequence warnings in `noise_robustness.py`.

## [0.1.3] - 2026-04-16

### Added

- Added `noise_robustness.py` renderer for topological stability analysis under Gaussian noise.
- Implemented `load_fashion_data` in `src/loaders.py` to support Fashion-MNIST.
- Added new CLI arguments to `generate.py`: `--sweep-min`, `--sweep-max`, `--sweep-step`, `--jump-threshold`, and
  `--renderers`.
- Support for selecting specific renderers via comma-separated list.

### Changed

- Made `VisualizationConfig` in `src/params.py` mutable to allow dynamic updates from CLI.
- Refactored `src/loaders.py` to use a generic `_load_npz_dataset` helper.

## [0.1.2] - 2026-04-16

### Added

- Implemented `test_core.py` to verify Delta Field transformation and Sweep logic.
- Added dynamic visualization module discovery in `script/common.py`.

### Changed

- Optimized `script/sweep.py` using `torch.histc` for significantly faster threshold sweeps (especially on MPS/GPU).
- Improved `generate.py` to show real-time output from subprocesses.
- Enhanced `script/common.py` to recursively move all data to CPU before parallel rendering.
- Optimized topological visualization modules (`betti0`, `betti1`, `euler`) by pre-converting tensors to NumPy.

## [0.1.1] - 2026-04-16

### Added

- Comprehensive documentation of mathematical transforms and visualization logic across all scripts. [f791522]
- Enhanced `generate.py` with `VIZ_SOURCE` environment variable support and unified orchestration. [7dee58a]

### Changed

- Major codebase refactor for improved structural clarity and readability. [cf8cb20]
- Centralized configuration parameters in `script/params.py` and standardized module naming. [471c065]

### Fixed

- Resolved duplicate function definitions and consolidated shared logic into `script/utils.py`. [471c065]

## [0.1.0] - 2026-04-16

### Added

- Initial core visualization pipeline with support for MNIST, PNG, and CMYK data sources. [25a565a]
