# AGENTS.md — Eugenia Contributor Guide

Eugenia combines a delta-field visualization pipeline with the Nucleus deterministic knowledge system. This guide is the short reference for anyone (human or agent) contributing to the repository.

## Project Structure & Module Organization

- `generate.py` — CLI entry point for the delta-field pipeline (auto-discovers renderers, sets `PYTHONPATH`).
- `src/` — main package, layout-imported as top-level modules:
  - `src/core/` — sweep algorithms (`sweep.py`) and math helpers (`division.py`).
  - `src/data/` — dataset loaders (MNIST, Fashion-MNIST, PNG, CMYK).
  - `src/models/` — `CONFIG` dataclass and typed result containers (`VisualizationData`, `SweepResults`).
  - `src/renderers/` — one `render(...)` function per file; add new modules here to extend outputs.
  - `src/nucleus/` — deterministic knowledge system; import via `from nucleus import ...`.
  - `src/extractors/`, `src/utils/` — weight extraction and shared image/viz/path/tensor helpers.
- `tests/` — pytest suite (`test_math.py`, `test_integration.py`, `test_nucleus_*.py`).
- `data/` — input datasets (`mnist.npz`, `fashion_mnist.npz`); override with `VIZ_DATA_DIR`.
- `output/{source}/` — generated PNG/GIF artifacts (gitignored).
- `plan/`, `conductor/`, `Physics/`, `Universe/` — design notes and research; not part of the runtime package.

## Build, Test, and Development Commands

```bash
python3 -m venv venv && source venv/bin/activate
pip install -e ".[dev]"           # install runtime + dev deps (ruff, mypy, pytest)

python3 generate.py               # run full pipeline for all sources
python3 generate.py --source mnist --parallel --workers 4
python3 generate.py --renderers betti_0_components,tsne_analysis

ruff check . && ruff format .     # lint + format (line-length 100)
mypy src/                         # strict type check (py3.14 target)
python3 -m pytest tests/ -v       # run full test suite
```

No Makefile is shipped — invoke tooling directly. `generate.py` injects `src/` into `PYTHONPATH`; import nucleus code as `from nucleus import ...`, never `from src.nucleus`.

## Coding Style & Naming Conventions

- Python 3.14, 4-space indent, line length **100** (ruff `target-version = "py314"`).
- `snake_case` for modules/functions, `PascalCase` for classes/dataclasses, `UPPER_SNAKE` for constants.
- Renderer modules: lowercase filename matching the produced artifact (e.g. `betti_0_components.py` → `betti_0_components.png`) and must export `render(data, sweep, out_dir)`.
- Prefer typed dataclasses from `src/models/types.py`; mypy runs in `strict = true` mode.
- Comments in English or Russian — Russian is reserved for algorithmic rationale.

## Testing Guidelines

- Framework: `pytest` (+ `pytest-mpl`); config in `pyproject.toml` (`testpaths = ["tests"]`, `python_files = "test_*.py"`).
- Name new tests `tests/test_<area>.py`; nucleus tests follow `test_nucleus_<component>.py`.
- Run a single file/test: `pytest tests/test_math.py -v` or `pytest tests/test_math.py::test_name`.
- Add tests alongside any change to `src/core`, `src/nucleus`, or renderer output contracts.

## Commit & Pull Request Guidelines

- Commit subjects follow Conventional-Commit-ish prefixes seen in history: `feat:`, `fix:`, `docs:`, `style:`, `chore:`, `Refactor:`, optionally scoped (`chore(conductor): ...`). Keep the subject imperative and ≤72 chars; elaborate in the body when touching multiple modules.
- One logical change per commit; do not mix formatting-only and behavior changes.
- PRs must include: concise description, linked issue (if any), reproduction/validation commands (`pytest`, `ruff`, relevant `generate.py` invocation), and before/after screenshots for renderer changes (PNGs from `output/`).
- Ensure `ruff check .`, `mypy src/`, and `pytest` pass before requesting review.

## Environment & Security Notes

- Key env vars: `VIZ_SOURCE`, `VIZ_SOURCE_FILE`, `VIZ_DATA_DIR`, `VIZ_OUTPUT_DIR`, `VIZ_WORKERS`; nucleus/LLM: `LLM_API_URL`, `LLM_MODEL`, `CACHE_DIR`, `OUTPUT_DIR`.
- Do not commit datasets, model weights, `output/`, `venv/`, caches (`.mypy_cache`, `.ruff_cache`, `.pytest_cache`), or `actions-runner/` credentials.
- GPU selection (CUDA/MPS) is automatic; cap workers with `VIZ_WORKERS` if OOM occurs.
