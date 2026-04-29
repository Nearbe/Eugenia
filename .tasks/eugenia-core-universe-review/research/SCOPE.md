# Scope Definition: Eugenia Core & Universe Review

## 1. Analysis of Structures

### `Universe` (Foundational Theory)
- **Type**: A theoretical knowledge base and research repository (primarily `.md`).
- **Key Subdirectories**:
    - `architecture/`: High-level design principles for the system.
    - `Essentials/`: Core mathematical/physical axioms.
    - `analytic/`: Research findings and discussions on specific implementations (e.g., tokenization, optimization).
    - `Everything/`: An expansive library of scientific and mathematical concepts (probability, thermodynamics, quantum mechanics, etc.) acting as a reference for the system's logic.

### `src` (Implementation Layer)
- **Type**: The Python implementation of the theoretical foundations.
- **Key Modules**:
    - `core/`: Implementation of U-algebra, calculus, combinatorics, fractal analysis, and dynamics. This is the mathematical engine.
    - `nucleus/`: The integration layer where core math is applied to "knowledge" (knowledge maps, LLM crisis analysis, pattern synthesis).
    - `extractors/`, `renderers/`, `models/`, `utils/`, `data/`: Support modules for data ingestion, visualization, configuration, and utilities.

## 2. Review Target Definition

To ensure a high-impact review within reasonable constraints, the scope is defined by the **Logic-Theory Alignment**.

### ✅ In Scope
- **Mathematical Core (`src/core/*`)**: Verification that implemented algebras (dual numbers), calculus operators, and fractal algorithms strictly adhere to the principles defined in `Universe`.
- **Foundational Architecture (`Universe/architecture/`, `Universe/Essentials/`)**: Reviewing the coherence of the theoretical framework that dictates how the code should behave.
- **Intelligence Logic (`src/nucleus/*`)**: Checking if high-level systems (knowledge maps, pattern synthesizers) correctly utilize the mathematical primitives from `core`.
- **Bridging Research (`Universe/analytic/`)**: Ensuring implementation choices (like tokenization or compression strategies) are documented and justified by research.

### ❌ Out of Scope
- **Peripheral Implementation**: Standard boilerplate in `src/utils/`, data loading in `src/data/`, and CLI/parsing in `src/extractors/`.
- **Visualization Mechanics**: The implementation details of matplotlib or plotting logic in `src/renderers/` (focus only on the *mathematical accuracy* of what is being plotted).
- **Configuration & Data Types**: Purely structural code in `src/models/`.
- **The "Everything" Library (`Universe/Everything/`)**: This directory acts as a reference. We will not review its completeness, but rather use it to verify the logic in `core`.

## 3. Potential Gaps & Ambiguities

- **Review Objective**: It is unclear if the primary goal is *mathematical verification* (proof vs code), *code quality/optimization*, or *completeness of documentation*.
- **Universe Breadth**: The `Everything` directory is massive. A review of "Universe" could be interpreted as reviewing every markdown file, which is impractical. This scope assumes `Universe` refers to the *active principles* driving the software.
- **Alignment Direction**: Should we identify code that violates theory, or theoretical gaps that existing code has already filled?
