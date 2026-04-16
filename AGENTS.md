# AGENTS.md

## Quick start

```bash
cd /Users/nearbe/EvgeniaML/visualizations
python3 generate.py              # ALL sources → output/{source}/
python3 generate.py --source mnist # single source
python3 generate.py --source png
python3 generate.py --source cmyk
```

## Output

```
output/
├── mnist/   # 15 PNG, 1 GIF
├── png/     # 15 PNG, 1 GIF
└── cmyk/    # 15 PNG, 1 GIF
```

## Data

- Data lives in sibling directory `eugenia_data/` (not in this repo)
- Required file: `eugenia_data/mnist.npz` with `x_train`, `y_train` keys
- If missing, visualizations will fail

## Architecture

Single entry point `generate.py` with `--source` flag:

| --source          | Loader       | Data source | Classes                            |
|-------------------|--------------|-------------|------------------------------------|
| `mnist` (default) | `loaders.py` | MNIST npz   | 10 digits                          |
| `fashion`         | `loaders.py` | Fashion-MN  | 10 clothing types                  |
| `png`             | `loaders.py` | PNG sprites | extracted via connected components |
| `cmyk`            | `loaders.py` | CMYK images | 4 channels (C,M,Y,K)               |

### generate.py

1. Parses CLI arguments (`--source`, `--file`, `--parallel`, `--workers`, `--sweep-min`, `--sweep-max`, `--sweep-step`,
   `--jump-threshold`, `--renderers`).
2. Orchestrates source processing by calling `src/common.py` as a subprocess.
3. Passes parameters via command-line arguments to ensure clean isolation between sources.

### src/common.py

1. Provides a parameterized API for loading data, computing sweeps, and rendering.
2. Supports CLI arguments for standalone execution.
3. Uses `logging` for unified output.
4. Uses `pathlib` for robust path management.

### src/sweep.py

- Uses `torch.histc` for high-performance histogram computation.
- Works on both CPU and Apple MPS (GPU).
- Detects **jump events**: where occupancy changes >1% between adjacent thresholds.

## Core Math

### Delta field (line 95 in common.py)

```python
delta_field = log(images + 1) - log(256 - images)
```

Interpretation: logarithmic contrast transformation mapping [0,255] → ℝ.

### Sweep algorithm

```
for threshold in sweep_range:
    binary = (delta_field > threshold)
    occupancy[c] = % of pixels in class c where binary == True
```

- Output: `occupancy_rates` shape `(num_thresholds, number_of_classes)`
- Jump detection: `abs(occupancy[t+1] - occupancy[t]) > jump_threshold`

### Topological features

Uses `scipy.ndimage`:

- `ndimage.label()`: connected components (Betti-0)
- Hole detection via morphological operations (Betti-1)

## Device

- Uses Apple MPS (Metal Performance Shaders) via PyTorch (line 32 in common.py)
- Falls back to CPU if MPS unavailable
- All heavy computation on GPU

## Output structure

```
root/
├── 00a_delta_histograms_by_class.png
├── 01_horizon_heatmap.png        # occupancy_rates as heatmap
├── 02_horizon_animation.gif     # 60-frame sweep
├── 03_scatter_mean_std.png
├── 04_jumps_analysis.png
├── 05_tsne_binary_profiles.png
├── 06_3d_surface.png
├── 07_cdf_by_class.png
├── 08_entropy_analysis.png
├── 09_original_vs_binary.png
├── 10_betti0_components.png
├── 11_betti1_holes.png
├── 12_euler_persistence_complexity.png
├── 13_persistence_landscape.png
├── 14_stress_map.png
├── 15_phase_volume.png
├── 16_beauty_vision.png
├── 17_noise_robustness.png
├── anim_frames/                # 60 PNG frames for animation
├── Eugene_cmyk.tiff            # CMYK source image
└── src/                       # core logic
    ├── utils/                 # shared utilities
    └── renderers/             # visualization modules
```

## Render function signature

Each visualization script exports:

```python
def render(data, sweep, out_dir):
    ...
```

Where:

- `data`: `VisualizationData` object with `symbol_delta_fields`, `number_of_classes`, `height`, `width`, `config`
- `sweep`: `SweepResults` object with `thresholds`, `occupancy_rates`, `jump_events`
- `out_dir`: output directory (root, NOT script/)

## Key configuration (params.py)

- `VisualizationConfig` dataclass at `src/params.py` (Mutable)
- Sweep range: `sweep_min=-5.546`, `sweep_max=5.546`, `sweep_step=0.0001` (Adjustable via CLI)
- Jump threshold: `1.0` (percent)
- Fig sizes defined per visualization type

## Adding a new visualization

1. Create `src/renderers/name.py`
2. Export `render(data, sweep, out_dir)` function
3. Run: `python3 generate.py`

## Debugging

- Uses `logging` module for all messages.
- Configure logging level and format in `generate.py` or `common.py`.
- Check `src/__pycache__/` for cached modules if imports fail.

## Files

- `generate.py`: Unified entry point (use `--source` flag)
- `src/common.py`: MNIST data loader + sweep orchestration
- `src/loaders.py`: Source-specific loaders (MNIST, PNG, CMYK)
- `src/models.py`: Data models and types
- `src/params.py`: Configuration dataclass
- `src/sweep.py`: Optimized threshold sweep logic
- `src/utils/image_utils.py`: Image processing and color conversions
- `src/utils/viz_utils.py`: Plotting & visualization
- `src/utils/path_utils.py`: Path management
- `src/utils/tensor_utils.py`: Tensor manipulations
- `src/renderers/*.py`: 19 visualization modules
