# Repository Guidelines

This repository contains a high-performance visualization pipeline for analyzing the topological features of images
using a **Delta Field** transformation and threshold sweep algorithm.

## Project Structure & Module Organization

The project is organized into the following structure:

- : The main entry point for running the visualization pipeline.
- : Contains all core logic and visualization modules.
    - : Pipeline orchestration.
    - : Data ingestion modules (e.g., MNIST, PNG, CMYK).
    - : Individual visualization modules.
    - : Shared utility functions (image processing, plotting, etc.).
- : Unit and integration tests.
- : Local datasets used for testing and generation.
- : Directory where generated visualizations are stored.
- : Automation and helper scripts.

## Build, Test, and Development Commands

The project uses a to manage common tasks. All commands should be run within a virtual environment ().

- python3 -m venv venv
  venv/bin/pip install --upgrade pip
  Requirement already satisfied: pip in ./venv/lib/python3.14/site-packages (26.0.1)
  venv/bin/pip install -e ".[dev]"
  Obtaining file:///Users/nearbe/Eugenia
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Checking if build backend supports build_editable: started
  Checking if build backend supports build_editable: finished with status 'done'
  Getting requirements to build editable: started
  Getting requirements to build editable: finished with status 'done'
  Preparing editable metadata (pyproject.toml): started
  Preparing editable metadata (pyproject.toml): finished with status 'done'
  Requirement already satisfied: numpy in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (2.4.4)
  Requirement already satisfied: scipy in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (1.17.1)
  Requirement already satisfied: matplotlib in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (3.10.8)
  Requirement already satisfied: Pillow in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (12.2.0)
  Requirement already satisfied: torch in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (2.11.0)
  Requirement already satisfied: tqdm in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (4.67.3)
  Requirement already satisfied: scikit-learn in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (1.8.0)
  Requirement already satisfied: pytest in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (9.0.3)
  Requirement already satisfied: pytest-mpl in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (0.19.0)
  Requirement already satisfied: ruff in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (0.15.10)
  Requirement already satisfied: mypy in ./venv/lib/python3.14/site-packages (from Eugenia==0.1.0) (1.20.1)
  Requirement already satisfied: contourpy>=1.0.1 in ./venv/lib/python3.14/site-packages (from matplotlib->
  Eugenia==0.1.0) (1.3.3)
  Requirement already satisfied: cycler>=0.10 in ./venv/lib/python3.14/site-packages (from matplotlib->Eugenia==0.1.0) (
  0.12.1)
  Requirement already satisfied: fonttools>=4.22.0 in ./venv/lib/python3.14/site-packages (from matplotlib->
  Eugenia==0.1.0) (4.62.1)
  Requirement already satisfied: kiwisolver>=1.3.1 in ./venv/lib/python3.14/site-packages (from matplotlib->
  Eugenia==0.1.0) (1.5.0)
  Requirement already satisfied: packaging>=20.0 in ./venv/lib/python3.14/site-packages (from matplotlib->
  Eugenia==0.1.0) (26.1)
  Requirement already satisfied: pyparsing>=3 in ./venv/lib/python3.14/site-packages (from matplotlib->Eugenia==0.1.0) (
  3.3.2)
  Requirement already satisfied: python-dateutil>=2.7 in ./venv/lib/python3.14/site-packages (from matplotlib->
  Eugenia==0.1.0) (2.9.0.post0)
  Requirement already satisfied: six>=1.5 in ./venv/lib/python3.14/site-packages (from python-dateutil>=2.7->
  matplotlib->Eugenia==0.1.0) (1.17.0)
  Requirement already satisfied: typing_extensions>=4.6.0 in ./venv/lib/python3.14/site-packages (from mypy->
  Eugenia==0.1.0) (4.15.0)
  Requirement already satisfied: mypy_extensions>=1.0.0 in ./venv/lib/python3.14/site-packages (from mypy->
  Eugenia==0.1.0) (1.1.0)
  Requirement already satisfied: pathspec>=1.0.0 in ./venv/lib/python3.14/site-packages (from mypy->Eugenia==0.1.0) (
  1.0.4)
  Requirement already satisfied: librt>=0.8.0 in ./venv/lib/python3.14/site-packages (from mypy->Eugenia==0.1.0) (0.9.0)
  Requirement already satisfied: iniconfig>=1.0.1 in ./venv/lib/python3.14/site-packages (from pytest->Eugenia==0.1.0) (
  2.3.0)
  Requirement already satisfied: pluggy<2,>=1.5 in ./venv/lib/python3.14/site-packages (from pytest->Eugenia==0.1.0) (
  1.6.0)
  Requirement already satisfied: pygments>=2.7.2 in ./venv/lib/python3.14/site-packages (from pytest->Eugenia==0.1.0) (
  2.20.0)
  Requirement already satisfied: Jinja2>=2.10.2 in ./venv/lib/python3.14/site-packages (from pytest-mpl->
  Eugenia==0.1.0) (3.1.6)
  Requirement already satisfied: MarkupSafe>=2.0 in ./venv/lib/python3.14/site-packages (from Jinja2>=2.10.2->
  pytest-mpl->Eugenia==0.1.0) (3.0.3)
  Requirement already satisfied: joblib>=1.3.0 in ./venv/lib/python3.14/site-packages (from scikit-learn->
  Eugenia==0.1.0) (1.5.3)
  Requirement already satisfied: threadpoolctl>=3.2.0 in ./venv/lib/python3.14/site-packages (from scikit-learn->
  Eugenia==0.1.0) (3.6.0)
  Requirement already satisfied: filelock in ./venv/lib/python3.14/site-packages (from torch->Eugenia==0.1.0) (3.28.0)
  Requirement already satisfied: setuptools<82 in ./venv/lib/python3.14/site-packages (from torch->Eugenia==0.1.0) (
  81.0.0)
  Requirement already satisfied: sympy>=1.13.3 in ./venv/lib/python3.14/site-packages (from torch->Eugenia==0.1.0) (
  1.14.0)
  Requirement already satisfied: networkx>=2.5.1 in ./venv/lib/python3.14/site-packages (from torch->Eugenia==0.1.0) (
  3.6.1)
  Requirement already satisfied: fsspec>=0.8.5 in ./venv/lib/python3.14/site-packages (from torch->Eugenia==0.1.0) (
  2026.3.0)
  Requirement already satisfied: mpmath<1.4,>=1.1.0 in ./venv/lib/python3.14/site-packages (from sympy>=1.13.3->torch->
  Eugenia==0.1.0) (1.3.0)
  Building wheels for collected packages: Eugenia
  Building editable for Eugenia (pyproject.toml): started
  Building editable for Eugenia (pyproject.toml): finished with status 'done'
  Created wheel for Eugenia: filename=eugenia-0.1.0-0.editable-py3-none-any.whl size=4491
  sha256=9c7fcccaea7162fbe85751d75daf61bc4a807288bdad7bb7bff5f515b8a310f4
  Stored in directory:
  /private/var/folders/34/5600hh790m527lzqmt3j8zwm0000gn/T/pip-ephem-wheel-cache-g1vltlgr/wheels/82/ed/68/e0427ab01dce76f9033e50ff042f0a074564b57aa52fae7cc9
  Successfully built Eugenia
  Installing collected packages: Eugenia
  Attempting uninstall: Eugenia
  Found existing installation: Eugenia 0.1.0
  Uninstalling Eugenia-0.1.0:
  Successfully uninstalled Eugenia-0.1.0
  Successfully installed Eugenia-0.1.0: Create a virtual environment and install all dependencies.
- venv/bin/python3 -m pytest tests/
  [1m============================= test session starts ==============================[0m
  platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
  Matplotlib: 3.10.8
  Freetype: 2.6.1
  rootdir: /Users/nearbe/Eugenia
  configfile: pyproject.toml
  plugins: mpl-0.19.0
  collected 7 items

tests/test_integration.py [33ms[0m[32m.[0m[32m                                             [ 28%][0m
tests/test_math.py [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[
32m                                                 [100%][0m

[32m========================= [32m[1m6 passed[0m, [33m1 skipped[0m[32m in 0.60s[0m[32m
=========================[0m: Run the test suite using [1m============================= test session starts
==============================[0m
platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
Matplotlib: 3.10.8
Freetype: 2.6.1
rootdir: /Users/nearbe/Eugenia
configfile: pyproject.toml
testpaths: tests
plugins: mpl-0.19.0
collected 7 items

tests/test_integration.py [33ms[0m[32m.[0m[32m                                             [ 28%][0m
tests/test_math.py [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[
32m                                                 [100%][0m

[32m========================= [32m[1m6 passed[0m, [33m1 skipped[0m[32m in 0.61s[0m[32m
=========================[0m.

- venv/bin/python3 generate.py --source all
  CWD: /Users/nearbe/Eugenia
  PIL test: <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=640x640 at 0x10D3F4AD0>
  Generating 60 animation frames...
  Assembling GIF...
  CWD: /Users/nearbe/Eugenia
  PIL test: <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=640x640 at 0x111240AD0>
  Loading Eugene
  Initial path: /Users/nearbe/Eugenia/Eugene, exists: False
  Trying Eugene.png -> /Users/nearbe/Eugenia/Eugene.png, exists: False
  Trying Eugene.jpeg -> /Users/nearbe/Eugenia/Eugene.jpeg, exists: True
  Final path: /Users/nearbe/Eugenia/Eugene.jpeg
  About to open: /Users/nearbe/Eugenia/Eugene.jpeg, type: <class 'str'>
  Generating 60 animation frames...
  Assembling GIF...
  CWD: /Users/nearbe/Eugenia
  PIL test: <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=640x640 at 0x10E6ECAD0>
  Generating 60 animation frames...
  Assembling GIF...
  CWD: /Users/nearbe/Eugenia
  PIL test: <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=640x640 at 0x10CB58AD0>: Execute the full
  visualization pipeline for all data sources.
- venv/bin/python3 -m ruff check src tests
  [1m[91mF811 [0m[[1m[96m*[0m] [1mRedefinition of unused `compute_gradient_magnitude` from line 74[0m
  [1m[94m-->[0m src/renderers/gradient_stress.py:74:31
  [1m[94m|[0m
  [1m[94m72 |[0m import numpy as np
  [1m[94m73 |[0m
  [1m[94m74 |[0m from utils.image_utils import compute_gradient_magnitude
  [1m[94m|[0m [1m[33m--------------------------[0m [1m[33mprevious definition of `compute_gradient_magnitude`
  here[0m
  [1m[94m75 |[0m from utils.viz_utils import save_visualization, get_symbol_label
  [1m[94m76 |[0m from utils.image_utils import compute_gradient_magnitude
  [1m[94m|[0m [1m[91m^^^^^^^^^^^^^^^^^^^^^^^^^^[0m [1m[91m`compute_gradient_magnitude` redefined here[0m
  [1m[94m|[0m
  [1m[96mhelp[0m: [1mRemove definition: `compute_gradient_magnitude`[0m

Found 1 error.
[[36m*[0m] 1 fixable with the `--fix` option.: Run the Ruff linter to check code quality.

- venv/bin/python3 -m ruff format src tests
  40 files left unchanged: Format the codebase using Ruff.
- venv/bin/python3 -m mypy src tests
  src/renderers/topological_entropy.py:111: error: No overload variant of "int" matches argument type "
  object"  [call-overload]
  src/renderers/topological_entropy.py:111: note: Possible overload variants:
  src/renderers/topological_entropy.py:111: note:     def int(str | Buffer | SupportsInt | SupportsIndex = ..., /) ->
  int
  src/renderers/topological_entropy.py:111: note:     def int(str | bytes | bytearray, /, base: SupportsIndex) -> int
  src/renderers/threshold_comparison.py:108: error: Argument 2 to "from_list" of "LinearSegmentedColormap" has
  incompatible type "list[Sequence[object]]"; expected "Buffer | _SupportsArray[dtype[Any]] | _NestedSequence[_
  SupportsArray[dtype[Any]]] | complex | bytes | str | _NestedSequence[complex | bytes | str] | Sequence[tuple[float,
  tuple[float, float, float] | str | str | tuple[float, float, float, float] | tuple[tuple[float, float, float] | str,
  float] | tuple[tuple[float, float, float, float], float]]]"  [arg-type]
  src/renderers/surface_3d_projection.py:173: error: "Axes" has no attribute "set_zlabel"  [attr-defined]
  src/renderers/summary_dashboard.py:72: error: Argument 2 to "from_list" of "LinearSegmentedColormap" has incompatible
  type "list[Sequence[object]]"; expected "Buffer | _SupportsArray[dtype[Any]] | _NestedSequence[_SupportsArray[
  dtype[Any]]] | complex | bytes | str | _NestedSequence[complex | bytes | str] | Sequence[tuple[float,
  tuple[float, float, float] | str | str | tuple[float, float, float, float] | tuple[tuple[float, float, float] | str,
  float] | tuple[tuple[float, float, float, float], float]]]"  [arg-type]
  src/renderers/gradient_stress.py:128: error: "Axes" has no attribute "set_zlabel"  [attr-defined]
  src/orchestrator.py:246: error: Argument 2 to "get" of "_Environ" has incompatible type "Path"; expected "str |
  None"  [arg-type]
  src/orchestrator.py:283: error: Argument 3 to "submit" of "Executor" has incompatible type "Path"; expected "
  str"  [arg-type]
  src/orchestrator.py:286: error: Argument 6 to "submit" of "Executor" has incompatible type "str | None"; expected "
  str"  [arg-type]
  Found 8 errors in 6 files (checked 40 source files): Run static type checking with Mypy.
- rm -rf output/*
  rm -rf src/**/__pycache__
  rm -rf tests/__pycache__: Clear the directory and cache files.

## Coding Style & Naming Conventions

- **Language**: Python 3.14+
- **Style**: The project follows standard PEP 8 guidelines, supplemented by for linting and formatting.
- **Naming**:
    - Use for functions, methods, and variables.
    - Use for classes.
    - Use for constants.
- **Typing**: Explicit type hinting is required for all function signatures to ensure clarity and support static
  analysis with Mypy.

## Testing Guidelines

- **Framework**: [1m============================= test session starts ==============================[0m
  platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
  Matplotlib: 3.10.8
  Freetype: 2.6.1
  rootdir: /Users/nearbe/Eugenia
  configfile: pyproject.toml
  testpaths: tests
  plugins: mpl-0.19.0
  collected 7 items

tests/test_integration.py [33ms[0m[32m.[0m[32m                                             [ 28%][0m
tests/test_math.py [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[
32m                                                 [100%][0m

[32m========================= [32m[1m6 passed[0m, [33m1 skipped[0m[32m in 0.64s[0m[32m
=========================[0m is used for all testing.

- **Coverage**: Tests should cover core mathematical logic, data loading, and individual renderer modules.
- **Execution**: Run tests using venv/bin/python3 -m pytest tests/
  [1m============================= test session starts ==============================[0m
  platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
  Matplotlib: 3.10.8
  Freetype: 2.6.1
  rootdir: /Users/nearbe/Eugenia
  configfile: pyproject.toml
  plugins: mpl-0.19.0
  collected 7 items

tests/test_integration.py [33ms[0m[32m.[0m[32m                                             [ 28%][0m
tests/test_math.py [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[
32m                                                 [100%][0m

[32m========================= [32m[1m6 passed[0m, [33m1 skipped[0m[32m in 0.61s[0m[32m
=========================[0m.

## Commit & Pull Request Guidelines

- **Commit Messages**: Follow the conventional commits format (e.g., , , ).
- **Pull Requests**:
    - Ensure all tests pass before submitting a PR.
    - Include a brief description of the changes and any new visualizations generated.
    - If applicable, provide screenshots or links to the directory for visual review.
