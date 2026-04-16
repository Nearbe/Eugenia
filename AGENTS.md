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

### src/loaders.py

1. Contains source-specific data loading logic (MNIST, PNG, CMYK).
2. Supports `VIZ_DATA_DIR` environment variable for the `eugenia_data` path.
3. Implements connected components algorithm for sprite extraction.

### src/sweep.py

- Uses `torch.histc` for high-performance histogram computation.
- Works on both CPU and Apple MPS (GPU).
- Detects **jump events**: where occupancy changes >1% between adjacent thresholds.

## Core Math

### Delta field (line 97 in src/common.py)

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

- Uses Apple MPS (Metal Performance Shaders) via PyTorch (line 87 in src/common.py)
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
├── 18_class_correlation.png
├── 19_jump_footprints.png
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

## Testing

The project uses `pytest` for unit and integration testing.

### Running Tests

```bash
pytest tests/
```

- `tests/test_math.py`: Verifies the Delta Field transformation and Sweep algorithm structure.
- `tests/test_integration.py`: Verifies data loading and end-to-end pipeline components for MNIST and PNG sources.

## Local LLM Integration (Junie CLI)

To save tokens and use Junie with a local model (e.g., Ollama, LM Studio) via terminal:

1. **Setup Environment**:
   ```bash
   make local-env
   ```
   This creates a `.env` file from `.env.example`. Edit it to point to your local API.

2. **Configure Local API**:
    - For **Ollama**: Use `http://localhost:11434/v1` as `JUNIE_API_BASE`.
    - For **LM Studio**: Use `http://192.168.1.91:1234/v1` as `JUNIE_API_BASE`.
    - **API Key**: `sk-lm-fp4sIXzQ:Ero2vvZ3skty30Ul8rnT`

3. **Available Models (LM Studio)**:
    - `qwen3-32b-merge-math4-science4-submath05-med05-other1-mlx` (Recommended)
    - `gemma-4-e4b-it-mlx`
    - `gemma-4-26b-a4b-it-mlx`
    - `google/gemma-4-26b-a4b`
    - `google/gemma-4-e2b`
    - `gpt-oss-120b-mlx-crack`
    - `harmonic-hermes-9b-mlx`
    - `zai-org/glm-4.7-flash`
    - `liquid/lfm2-1.2b`
    - `crow-9b-heretic-4.6`
    - `liquid/lfm2-24b-a2b`
    - `text-embedding-nomic-embed-text-v1.5`

4. **Running**:
   Ensure your local LLM server is running and the model is loaded.

   The project includes a pre-configured model definition for Junie CLI in `.junie/models/qwen-local.json`.
   To use it, you can run:
   ```bash
   junie --model qwen-local "Ваша задача"
   ```

   If you want to use it as the default, you can set `JUNIE_MODEL` in your `.env` and the CLI will pick it up (if
   supported by your version) or use the `--model` flag.

## IDE Integration

This project is optimized for JetBrains IDEs (PyCharm, IntelliJ IDEA with Python plugin).

### Run Configurations

Pre-defined Run Configurations are available in the `.idea/runConfigurations/` folder:

- **Generate ALL**: Runs `generate.py` for all data sources.
- **Generate MNIST**: Runs `generate.py --source mnist`.
- **Generate PNG**: Runs `generate.py --source png`.
- **Generate CMYK**: Runs `generate.py --source cmyk`.
- **Pytest in tests**: Runs all tests in the `tests/` directory.

### Project Structure

- **Source Root**: The `src/` directory is marked as a source root for proper module resolution.
- **Test Root**: The `tests/` directory is marked as a test source root.
- **Excluded Folders**: `output/`, `venv/`, and `.idea/` are excluded from indexing to maintain performance.

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
- `src/renderers/*.py`: 21 visualization modules
