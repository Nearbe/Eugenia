# AGENTS.md — Eugenia

## Commands

```bash
pip install -e ".[dev]"
ruff check src tests
ruff format --check src tests
mypy src tests
pytest tests/ -v --tb=short
PYTHONPATH=src pytest tests/
```

Run single test:
```bash
pytest tests/test_core_operators.py -v
```

Notes:
- `pip install -e ".[dev]"` — install in editable mode with dev deps
- `ruff check src tests` — lint
- `ruff format --check src tests` — format check
- `mypy src tests` — type check (strict, Python 3.14 target)
- `PYTHONPATH=src pytest tests/` — run tests without editable install

## Setup

- **Python**: Requires 3.14+ (per pyproject.toml). CI tests on 3.11–3.13 (mismatch).
- **Submodules**: Initialize before working:
  ```bash
  git submodule update --init --recursive
  ```
  Submodules: `Universe` (math foundations), `Formatter` (code formatting), `Physics` (research notes).
- **External repos**: `llama.cpp/` and `whisper.cpp/` are present but not submodules. Build separately with cmake if C++ binaries needed.

## Structure

- `src/core/` — U-algebra, calculus, operators, foundations
- `src/nucleus/` — Higher-level systems, knowledge maps, LLM analysis
- `src/extractors/` — GGUF, correlation extractors, CLI
- `src/renderers/` — Visualization (matplotlib, topological analysis)
- `src/models/` — Config and data models
- `src/utils/` — Shared utilities
- `src/data/` — Data loaders (MNIST, etc.)
- `tests/` — Tests use `pytest-mpl` for matplotlib visualizations

## Quirks

- **Runtime settings** in `Eugenia.py` / `Eugenia_v0.py`:
  - `setrecursionlimit(3)` — extremely low recursion depth
  - `setswitchinterval(1e-17)` — near-zero thread switching
  - `set_int_max_str_digits(0)` — no limit on int string conversion
- **Multilingual**: Comments and docs in Russian, English, and Greek
- **pytest-mpl**: Used for tests involving matplotlib output verification
- **Line length**: 100 chars (see pyproject.toml `[tool.ruff]`)
- **Type checking**: Strict mypy with `mypy_path = "src"`

## CI Order

CI runs: lint → format check → type check → test → benchmark (after test passes)
