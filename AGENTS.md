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

| --source | Module | Data source | Classes |
|---------|--------|-----------|---------|
| `mnist` (default) | `common.py` | MNIST npz | 10 digits |
| `png` | `common_png.py` | PNG sprites | extracted via connected components |
| `cmyk` | `common_cmyk.py` | CMYK images | 4 channels (C,M,Y,K) |

### common.py (MNIST)

1. Loads `mnist.npz` → one sample per digit (10 total)
2. Computes **Δ-field**: `D = log(X+1) - log(256-X)` (line 48)
3. Runs **sweep**: thresholds -5.546 to 5.546, step 0.0001 (111K thresholds)
4. For each threshold: computes `% of pixels where D > threshold` per class
5. Detects **jump events**: where occupancy changes >1% between adjacent thresholds

### common_png.py (PNG sprites)

1. Loads PNG sprite sheet (e.g., `cyrillic.png`, `latin.png`, `Eugene.jpeg`)
2. Extracts **symbols** by connected components in Δ-field (Δ > -4.0 threshold)
3. Each symbol becomes a "class"
4. Runs same sweep algorithm

### common_cmyk.py (CMYK images)

- Loads 4-channel CMYK image (Cyan, Magenta, Yellow, Key)
- Each channel treated as a separate "symbol"
- No symbol extraction (whole image)

## Core Math

### Delta field (line 48 in common.py)

```python
D = log(X + 1) - log(256 - X)
```

Interpretation: logarithmic contrast transformation mapping [0,255] → ℝ.

### Sweep algorithm

```
for threshold in sweep_range:
    binary = (D > threshold)
    bits[c] = % of pixels in class c where binary == True
```

- Output: `bits_tr_all` shape `(n_thresholds, n_classes)`
- Jump detection: `abs(bits[t+1] - bits[t]) > jump_threshold`

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
├── 01_horizon_heatmap.png        # bits_tr_all as heatmap
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
├── anim_frames/                # 60 PNG frames for animation
└── script/                    # source files
```

## Render function signature

Each visualization script exports:

```python
def render(data, sweep, out_dir):
    ...
```

Where:
- `data`: dict with keys `symbols_delta`, `n_classes`, `H`, `W`, `viz`
- `sweep`: dict with keys `thresholds`, `bits_tr_all`, `jump_events`
- `out_dir`: output directory (root, NOT script/)

## Key configuration (params.py)

- `SolenoidVizParams` dataclass at `script/params.py:12`
- Sweep range: `sweep_min=-5.546`, `sweep_max=5.546`, `sweep_step=0.0001`
- Jump threshold: `1.0` (percent)
- Fig sizes defined per visualization type

## Adding a new visualization

1. Create `script/XX_name.py`
2. Export `render(data, sweep, out_dir)` function
3. Add to `scripts` list in `common.py` or corresponding common module
4. Run: `python generate_all.py`

## Debugging

- Add `print()` statements ( flushed, timestamps via `time.strftime('%H:%M:%S')`)
- Check `script/__pycache__/` for cached modules
- Re-run with: `python generate_all.py`

## Files

- `generate.py`: Unified entry point (use `--source` flag)
- `script/common.py`: MNIST data loader + sweep
- `script/common_png.py`: PNG sprite loader
- `script/common_cmyk.py`: CMYK image loader
- `script/params.py`: Configuration dataclass
- `script/*.py`: 16 visualization modules