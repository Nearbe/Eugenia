# Visualizations (Experimental)

> The visualization pipeline is a secondary experimental surface. The primary value of Eugenia is the **Nucleus**
> deterministic knowledge system. See [Nucleus Overview](/nucleus/) for the main documentation.

## Quick Start

```bash
# Generate visualizations for all sources
python3 generate.py

# Single source
python3 generate.py --source mnist
python3 generate.py --source png --file eng_alphabetical
python3 generate.py --source cmyk
python3 generate.py --source fashion

# Parallel execution
python3 generate.py --parallel

# Custom sweep parameters
python3 generate.py --source mnist --sweep-min -6.0 --sweep-max 6.0 --sweep-step 0.0005 --jump-threshold 0.5

# Selective renderers
python3 generate.py --source mnist --renderers betti_0_components,tsne_analysis
```

## CLI Arguments

| Flag               | Purpose                                                                   |
|--------------------|---------------------------------------------------------------------------|
| `--source`         | Data source: `mnist`, `png`, `cmyk`, `fashion`, or `all`                  |
| `--file`           | Specific file for `png` source (e.g., `eng_alphabetical`, `Rus-alfabita`) |
| `--parallel`       | Run sources in parallel via `ProcessPoolExecutor`                         |
| `--workers`        | Number of parallel workers (default: auto-detected)                       |
| `--sweep-min`      | Minimum threshold for delta field sweep                                   |
| `--sweep-max`      | Maximum threshold for sweep                                               |
| `--sweep-step`     | Step size for sweep thresholds                                            |
| `--jump-threshold` | Jump detection threshold in percent                                       |
| `--renderers`      | Comma-separated list of renderer names to run                             |

## Data Sources

| Source    | Input File                                                | Classes                            |
|-----------|-----------------------------------------------------------|------------------------------------|
| `mnist`   | `data/mnist.npz` (`x_train`, `y_train`)                   | 10 digits                          |
| `fashion` | `data/fashion_mnist.npz` (same format)                    | 10 clothing categories             |
| `png`     | `eng_alphabetical.jpg`, `Rus-alfabita.png` (project root) | Extracted via connected components |
| `cmyk`    | `Eugene_cmyk.tiff` (project root)                         | 4 channels (C, M, Y, K)            |

## Output

22 PNG files + 1 GIF per source in `output/{source}/`:

- `delta_histograms_by_class.png` — Delta value distribution per class
- `horizon_scan_heatmap.png` — 2D delta field heatmaps
- `horizon_scan_animation.gif` — Animated threshold sweep
- `mean_std_analysis.png` — Statistical distribution
- `jump_analysis.png` — Occupancy change detection
- `tsne_analysis.png` — t-SNE of binary occupancy profiles
- `surface_3d_projection.png` — 3D delta field mesh
- `cumulative_distribution.png` — CDFs of delta values
- `topological_entropy.png` — Shannon entropy across sweep
- `symbol_grid.png` — Visual symbol grid
- `betti_0_components.png` — Betti-0 persistence
- `betti_1_holes.png` — Betti-1 persistence
- `euler_characteristic.png` — Euler characteristic curves
- `persistence_landscape.png` — Topological landscapes
- `gradient_stress.png` — Gradient magnitude and stress
- `phase_volume.png` — State transition volumes
- `class_correlation.png` — Class-label correlation
- `jump_footprint.png` — Jump event footprint
- `noise_robustness.png` — Noise robustness testing
- `individual_histograms/` — Directory of per-symbol histograms
- `threshold_comparison.png` — Threshold comparison
- `summary_dashboard.png` — Summary dashboard

> `threshold_comparison.py` and `summary_dashboard.py` are excluded from mypy type checking.

## Core Algorithm

1. **Delta Field**: `D = log(X + 1) - log(256 - X)` maps pixel values X ∈ [0, 255] to D ∈ [-5.546, 5.546]
2. **Threshold Sweep**: ~111k threshold levels across delta field range
3. **Occupancy Rates**: Histogram-based computation of % pixels above each threshold per class
4. **Jump Detection**: Occupancy changes > 1% between adjacent thresholds flagged as events

## Configuration

All numeric parameters are in `src/models/config.py` via the `CONFIG` dataclass. Key parameters:

| Parameter                | Default | Purpose                      |
|--------------------------|---------|------------------------------|
| `sweep_min`              | -5.546  | Minimum sweep threshold      |
| `sweep_max`              | 5.546   | Maximum sweep threshold      |
| `sweep_step`             | 0.0001  | Threshold step size          |
| `jump_threshold`         | 1.0     | Jump detection threshold (%) |
| `histogram_bins`         | 100     | Histogram bin count          |
| `tsne_perplexity`        | 30      | t-SNE perplexity             |
| `topology_threshold_min` | -5.0    | Topology analysis min        |
| `topology_threshold_max` | 4.5     | Topology analysis max        |

## Environment Variables

| Variable                   | Purpose                                 |
|----------------------------|-----------------------------------------|
| `VIZ_SOURCE`               | Data source (mnist, png, cmyk, fashion) |
| `VIZ_SOURCE_FILE`          | Specific file for png source            |
| `VIZ_OUTPUT_DIR`           | Output directory                        |
| `VIZ_DATA_DIR`             | Custom path to data directory           |
| `EUGENIA_PRECOMPUTE_DELTA` | If "true", load delta from `delta.npy`  |

## Testing

```bash
make test        # pytest
make lint        # ruff check
make format      # ruff format
make typecheck   # mypy
```
