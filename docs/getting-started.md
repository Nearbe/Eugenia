# Getting Started

## What is Eugenia?

Eugenia is a **deterministic knowledge system** that transforms neural network weights into structured, interpretable
patterns. Instead of storing raw weights (111GB), it extracts eigenpatterns through SVD, compresses them, and builds a
correlation graph — reducing storage to ~50MB while preserving the model's semantic structure.

The visualization pipeline (`generate.py`) is a secondary experimental surface for topological analysis of images. The
primary value is the **Nucleus** system.

## Quick Start

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run the nucleus knowledge pipeline (GGUF → SVD → patterns → graph)
# (requires a GGUF model file)

# Run visualization pipeline (experimental)
python3 generate.py --source mnist
```

## Prerequisites

- **Python**: 3.11+ (CI tests 3.11, 3.12, 3.13)
- **Hardware acceleration**: PyTorch with CUDA or MPS
- **Disk space**: ~2 GB for dependencies

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

**Runtime deps**: `numpy`, `scipy`, `matplotlib`, `Pillow`, `torch`, `tqdm`, `scikit-learn`, `safetensors`
**Dev deps**: `pytest`, `pytest-mpl`, `ruff`, `mypy`

## Project Structure

```
.
├── generate.py              # CLI entry (visualization pipeline, secondary)
├── pyproject.toml           # Project metadata, deps, tool config
├── src/
│   ├── orchestrator.py      # Visualization pipeline orchestration
│   ├── core/                # Sweep algorithms, math utilities, delta operations (21 modules)
│   ├── data/                # Data loaders (MNIST, Fashion, PNG, CMYK)
│   ├── models/              # Config & typed dataclasses
│   ├── nucleus/             # 🔥 Deterministic knowledge system (19 modules)
│   ├── renderers/           # 22 visualization modules
│   └── utils/               # Shared utilities
├── tests/                   # Unit & integration tests
├── data/                    # Dataset files
├── output/                  # Generated visualizations (gitignored)
└── venv/                    # Python virtual environment (gitignored)
```

## Next Steps

- [Nucleus Overview](/nucleus/) — What the system does and why
- [Architecture](/nucleus/architecture/) — Module map and data flow
- [Module Reference](/nucleus/modules/) — Per-module API
- [Visualizations](/visualizations/) — Experimental delta field pipeline
