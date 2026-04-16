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
| `png`             | `loaders.py` | PNG sprites | extracted via connected components |
| `cmyk`            | `loaders.py` | CMYK images | 4 channels (C,M,Y,K)               |

### generate.py

1. Parses CLI arguments.
2. Sets environment variables (`VIZ_SOURCE`, `VIZ_OUTPUT_DIR`).
3. Runs subprocess for each source to ensure isolation and clean resource handling.

### script/common.py

1. Calls `loaders.py` functions to load data.
2. Computes **delta field**: `delta_field = log(X+1) - log(256-X)`.
3. Runs **sweep**: thresholds -5.546 to 5.546, step 0.0001 (~111K thresholds).
4. Dynamically discovers visualization modules in `script/visualizations/*.py`.
5. Uses `ProcessPoolExecutor` for parallel rendering of modules.

### script/sweep.py

- Uses `torch.histc` for high-performance histogram computation.
- Works on both CPU and Apple MPS (GPU).
- Detects **jump events**: where occupancy changes >1% between adjacent thresholds.

## Core Math

### Delta field (line 89 in common.py)

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
├── anim_frames/                # 60 PNG frames for animation
├── Eugene_cmyk.tiff            # CMYK source image
└── script/                    # core logic
    └── visualizations/        # visualization modules
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

- `VisualizationConfig` dataclass at `script/params.py:49`
- Sweep range: `sweep_min=-5.546`, `sweep_max=5.546`, `sweep_step=0.0001`
- Jump threshold: `1.0` (percent)
- Fig sizes defined per visualization type

## Adding a new visualization

1. Create `script/visualizations/name.py`
2. Export `render(data, sweep, out_dir)` function
3. Run: `python3 generate.py`

## Debugging

- Add `print()` statements ( flushed, timestamps via `time.strftime('%H:%M:%S')`)
- Check `script/__pycache__/` for cached modules
- Re-run with: `python generate_all.py`

## Files

- `generate.py`: Unified entry point (use `--source` flag)
- `script/common.py`: MNIST data loader + sweep orchestration
- `script/loaders.py`: Source-specific loaders (MNIST, PNG, CMYK)
- `script/models.py`: Data models and types
- `script/params.py`: Configuration dataclass
- `script/sweep.py`: Optimized threshold sweep logic
- `script/utils.py`: Shared utilities
- `script/visualizations/*.py`: 18 visualization modules
