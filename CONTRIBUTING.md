# Contributing to Eugenia

Thank you for your interest in Eugenia! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Code Style](#code-style)
- [Testing](#testing)
- [Adding a New Renderer](#adding-a-new-renderer)
- [Nucleus Modules](#nucleus-modules)
- [Reporting Bugs](#reporting-bugs)
- [Pull Request Process](#pull-request-process)

## Project Structure

Eugenia consists of two separate systems:

```
Eugenia/
├── generate.py              # CLI entry point
├── src/
│   ├── orchestrator.py      # Core orchestration
│   ├── core/                # Math utilities, sweep algorithm
│   ├── data/                # Data loaders (MNIST, PNG, CMYK)
│   ├── models/              # Config dataclass, type definitions
│   ├── renderers/           # 22 visualization modules
│   ├── utils/               # Image/path/tensor/viz utilities
│   └── nucleus/             # Knowledge compression system (research)
├── tests/                   # Unit and integration tests
├── data/                    # Dataset files (MNIST, etc.)
└── output/                  # Generated visualizations
```

## Getting Started

### Prerequisites

- Python >= 3.11
- pip or conda

### Setup

```bash
# Install dependencies
make setup

# Run tests
make test

# Run linter
make lint

# Run type checker
make typecheck
```

## Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

```bash
# Format code
make format

# Check linting
make lint
```

### Guidelines

- **Line length**: 100 characters
- **Type hints**: Use for function signatures where helpful
- **Docstrings**: Use Google-style docstrings for all public functions
- **Comments**: Explain *why*, not *what*
- **Naming**: Descriptive names, `snake_case` for functions/variables, `PascalCase` for classes

## Testing

### Running Tests

```bash
make test
# or
python -m pytest tests/ -v
```

### Writing Tests

- Place tests in `tests/` with `test_` prefix
- Use `pytest` fixtures for setup
- Test both happy paths and edge cases
- Aim for >80% coverage on new code

```python
def test_delta_field_symmetry():
    """Delta field should be symmetric around 0.5."""
    x = np.linspace(0, 255, 256)
    delta = np.log(x + 1) - np.log(256 - x)
    # Symmetry check
    assert np.allclose(delta, -np.flip(delta))
```

## Adding a New Renderer

1. Create `src/renderers/my_new_plot.py`
2. Export a `render(data, sweep, out_dir) -> None` function
3. The renderer is auto-discovered — no registration needed
4. Add a test in `tests/test_renderers.py`
5. Update README with a description of the visualization

```python
"""My New Visualization

Describes what the visualization shows and its purpose.
"""

import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt


def render(data, sweep: SweepResults, out_dir: str) -> None:
    """
    Render my new visualization.

    Args:
        data: VisualizationData with computed values
        sweep: SweepResults with threshold sweep data
        out_dir: Output directory for the visualization
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Your visualization code here
    ax.plot(sweep.occupancy_rates)
    ax.set_title("My New Visualization")

    out_path = Path(out_dir) / "my_new_plot.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
```

## Nucleus Modules

The `src/nucleus/` directory contains research-grade modules for LLM weight compression and knowledge representation.
These are **experimental** and not integrated with the visualization pipeline.

### Current Status

| Module                              | Status        | Notes                             |
|-------------------------------------|---------------|-----------------------------------|
| `deterministic_core.py`             | Prototype     | SVD-based pattern extraction      |
| `universal_knowledge_map.py`        | Prototype     | Universal knowledge compression   |
| `knowledge_graph.py`                | Prototype     | Eigenstructure graph              |
| `correlation_compressor.py`         | Prototype     | 4 compression methods             |
| `nucleus_knowledge_system.py`       | Prototype     | Absorb/generate/relate system     |
| `nucleus_seed_system.py`            | Prototype     | Seed-based correlation engine     |
| `universal_geometric_classifier.py` | Prototype     | Few-shot geometric classification |
| `fractal_compressor.py`             | Prototype     | Iterative SVD compression         |
| `cross_layer_compressor.py`         | Prototype     | Cross-layer eigenstructure        |
| `llm_crisis_analysis.py`            | Documentation | Analysis only, no executable code |

### Adding to Nucleus

1. Create the module in `src/nucleus/`
2. Add a `demo()` function with `if __name__ == "__main__": demo()`
3. Document the scientific basis and mathematical formalization
4. Add tests in `tests/nucleus/`
5. Update `src/nucleus/__init__.py` exports

## Reporting Bugs

Please report bugs with:

1. **Environment**: Python version, OS, installed packages
2. **Reproduction steps**: Exact commands to reproduce the issue
3. **Expected vs actual output**: Full error messages or unexpected results
4. **Data files**: Which data source (MNIST/PNG/CMYK) was used

Use the `/bug` command or open an issue on GitHub.

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** from `main` for your changes
3. **Make your changes** following the code style guidelines
4. **Add tests** for new functionality
5. **Run all checks**: `make lint && make typecheck && make test`
6. **Write a clear commit message** following [Conventional Commits](https://www.conventionalcommits.org/):
    - `feat:` new functionality
    - `fix:` bug fix
    - `docs:` documentation changes
    - `refactor:` code refactoring
    - `test:` test additions or changes
    - `chore:` maintenance tasks
7. **Submit a PR** with:
    - Clear description of changes
    - Link to related issues
    - Screenshots for visualization changes
    - Test results

## Development Workflow

```bash
# 1. Setup
make setup

# 2. Make changes
# ... edit files ...

# 3. Check your work
make lint && make typecheck && make test

# 4. Commit
git add .
git commit -m "feat: add new visualization"

# 5. Push and create PR
git push origin your-branch
```

## Questions?

Feel free to open an issue or ask questions. All contributions are welcome!
