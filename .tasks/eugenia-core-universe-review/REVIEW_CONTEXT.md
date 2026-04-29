# REVIEW_CONTEXT.md

## 1. Architectural Dependencies & Integrations

### Overview
The implementation (`src`) maps theoretical concepts from the `Universe` documentation into computational modules via a "Universal Geometric Knowledge Machine" architecture.

### Component Mapping (Theory $\rightarrow$ Implementation)
- **Universal Normalizer**: Scales input data to $[0, 1]$.
- **Binary Sweep/Jump Detector**: Extracts geometric density profiles and identifies topological transitions using thresholds on binary states.
- **Topology Extractor**: Approximates Betti numbers ($b_0$, $b_1$) from state transitions in `GeometricExtractor`.
- **Pattern Fusion**: Aggregates multiple metrics (cosine similarity, jump event density, Betti signature distance) into a single $144$-dimensional `GeometricProfile`.
- **Pattern Graph Engine**: Manages knowledge via pattern synthesis and inter-correlations within `src/nucleus`.

### Dependency Flow
`Data Ingestion` $\rightarrow$ `Universal Normalizer` $\rightarrow$ `Geometric Extraction (Sweep, Jump, Topology)` $\rightarrow$ `Pattern Fusion` $\rightarrow$ `Pattern Graph Engine`.

## 2. Testing & Project Conventions

### Focus Areas
- **Mathematical Invariant Verification**: Ensuring algebraic axioms hold (e.g., $H(D(x)) \approx x$).
- **Edge Case/Contract Enforcement**: Validating stability at mathematical singularities ($0$, $\infty$) and sentinel value handling.
- **Precision Management**: Use of `pytest.approx` to handle floating-point errors in geometric computations.

## 3. Key Risks & Unknowns
- **Floating Point Drift**: Cumulative error in long chains of algebraic/topological operations.
- **Singularity Handling**: Robustness of the "Universal Normalizer" and logarithmic mappings when encountering zero or near-zero values.
- **Theory-Implementation Lag**: Risk of code diverging from evolving research in `Universe`.

---
*Generated during Ask-Context phase.*
