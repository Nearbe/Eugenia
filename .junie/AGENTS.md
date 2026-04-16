# AGENTS.md

This document provides technical details for advanced developers working on the Visualizations project.

## Quick Start

```bash
cd /Users/nearbe/EvgeniaML/visualizations
python3 generate.py              # ALL sources → output/{source}/
python3 generate.py --source mnist # single source
python3 generate.py --source png
python3 generate.py --source cmyk
```

## Build & Configuration

### Prerequisites

- **Python 3.14+** (tested with 3.14)
- **PyTorch** (with MPS support for macOS)
- **Dependencies**: `numpy`, `scipy`, `matplotlib`, `Pillow`, `torch`

### Data Setup

- Data lives in a sibling directory `../eugenia_data/` (outside this repo).
- **MNIST**: Requires `../eugenia_data/mnist.npz` with `x_train` and `y_train` keys.
- **PNG**: Reads from files like `cyrillic.png`, `latin.png`, or `Eugene.jpeg` in the project root.
- **CMYK**: Reads `script/Eugene_cmyk.tiff`.

### Device Configuration

- The project automatically detects and uses **Apple MPS (Metal Performance Shaders)** if available.
- Fallback to **CPU** is automatic if MPS is not detected.
- Heavy computations (Δ-field, large tensors) should stay on the GPU/MPS device.

## Testing Information

### Running Tests

There are no formal test frameworks (like pytest) integrated yet, but core logic can be verified using standalone
scripts.

To run a basic verification of the math engine:

```bash
python3 test_core.py
```

### Adding New Tests

When adding new features or refactoring core math (Δ-field, sweep), create a standalone script that imports
`script.params.CONFIG` and verify against known values.

### Test Example (Core Math)

```python
import torch
from script.params import CONFIG

def test_delta_field():
    # X in [0, 255]
    X = torch.tensor([0.0, 127.5, 255.0])
    # D = log(X + 1) - log(256 - X)
    D = torch.log(X + 1.0) - torch.log(256.0 - X)
    
    assert torch.allclose(D[1], torch.tensor(0.0), atol=1e-5)
    assert D[0] < -5.545  # log(1) - log(256)
    assert D[2] > 5.545   # log(256) - log(1)
    print("Delta Field verification successful")

if __name__ == "__main__":
    test_delta_field()
```

## Architecture & Development Info

### Entry Point: `generate.py`

- Parses CLI arguments.
- Sets `VIZ_SOURCE` environment variable.
- Calls `script.common.run_all_visualizations()`.

### Core Orchestration: `script/common.py`

- Handles data loading via `loaders.py`.
- Computes the **Δ-field**: `D = log(X + 1) - log(256 - X)`.
- Triggers the **Sweep algorithm** in `sweep.py`.
- Uses `ProcessPoolExecutor` for parallel rendering of visualization modules.

### Sweep Algorithm (`script/sweep.py`)

- Range: -5.546 to 5.546 (defined in `params.py`).
- Step: 0.0001 (~111K thresholds).
- Efficiency: Uses `np.histogram` and `np.cumsum` for $O(N)$ occupancy calculation instead of $O(N \times T)$
  thresholding.
- **Jump Events**: Detected when occupancy changes $> 1\%$ between adjacent steps.

### Visualization Modules

- Each module in `script/*.py` must export a `render(data, sweep, out_dir)` function.
- `data` contains delta fields and metadata.
- `sweep` contains thresholds and occupancy rates (`bits_tr_all`).

### Code Style & Best Practices

- **Concurrency**: Use `ProcessPoolExecutor` for CPU-bound rendering and `ThreadPoolExecutor` for I/O or NumPy-heavy
  tasks (which release the GIL).
- **Memory**: Move large tensors to CPU before passing them to child processes to avoid MPS/CUDA context issues in
  forks.
- **Logging**: Use `time.strftime('%H:%M:%S')` in print statements and always use `flush=True`.

## Files

- `generate.py`: Unified entry point.
- `script/common.py`: MNIST data loader + sweep orchestration.
- `script/loaders.py`: Specific data loaders (MNIST, PNG, CMYK).
- `script/params.py`: Configuration dataclass (`CONFIG`).
- `script/sweep.py`: Core threshold sweep logic.
- `script/utils.py`: Shared visualization utilities.
