# Eugenia Project Structure and Math Foundations Exploration

## 1. Overall Directory Structure

The Eugenia project root contains:
- `src/` - Main source code
- `Universe/` - Submodule with math foundations
- `Formatter/` - Submodule (code formatting)
- `Physics/` - Submodule (research notes)
- Configuration files (AGENTS.md, pyproject.toml, README.md, etc.)
- External repos: `llama.cpp/`, `whisper.cpp/` (not submodules)

### src/ Structure
- `src/core/` - U-algebra, calculus, operators, foundations (heavily subdivided)
- `src/data/` - Data loaders
- `src/extractors/` - GGUF, correlation extractors, CLI
- `src/models/` - Config and data models
- `src/nucleus/` - Higher-level systems, knowledge maps, LLM analysis
- `src/renderers/` - Visualization (matplotlib, topological analysis)
- `src/utils/` - Shared utilities

## 2. Current State of Math Implementation in src/

The `src/core/` module implements a custom U-algebra with:
- Algebraic operations: add, multiply, branch, compress, etc.
- Dual numbers (ε² = Ω) with OMEGA = 0.0, D_ID = 2.0
- Algebraic fullness state Π (infinity module)
- Supporting types: complex states, participation ratios, fullness shares, spine levels
- The math implementation appears to be a concrete realization of some Universe axioms, particularly dual numbers and branching/compression operations.

## 3. Universe Submodule (Math Foundations)

The Universe submodule contains extensive mathematical documentation covering:
- **Axioms of Being**: Identity, Law of Life (Id = Ω), Act (Id : Ω), Law of Branching (a : Ω = D(a) = a ⊕ a), Compression (H(a) = ret(a))
- **Geometry of the Carrier**: 𝕌 = Im ∩ Re, spine H^n = D^n(Id), fabric r = p : q
- **Operations**: ⊕ (shift/accumulation), ⊗ (intersection of rows)
- **Flow Plane**: Complex states z = x + i·y
- **Logarithm**: L(a) as level metric
- **Dual Numbers**: Z = x + v·ε with ε² = Ω
- **Limits**: Π (fullness), Ω (potential)
- **Ontological Identity**: Id ≡ D(Id) ≡ Π ≡ Π : Π
- **Function Reactions**: How functions respond to : Ω
- **Equations and Systems**: Scale invariance, quadratic equations
- **Differentiation**: Via dual numbers
- **Gödel-Turing Inversion**: D ∘ H = Id
- **Integral**: As accumulation
- **Fractal Geometry**: Scaling with D
- **Computability**: Recursion → regression → inversion
- **Evolution**: As debugging (Δ → Ω)
- **Numbers**: D(Id) as atom, combinatorics, probability as branch fraction
- **Scale Invariance**: Operator : as renormalization group step
- **Information**: As depth or length of address
- **Wave Function**: Ψ = Re + i·Im
- **Mass and Energy**: M = Σ|Ψ|², E = M, and I ≡ M ≡ E

## 4. Areas Needing Refactoring for True Math Implementation

While src/core/algebra has some Universe-inspired elements, it does not fully implement the axioms. Key gaps:

### Refactoring Targets in src/core/algebra:
1. **Law of Life (Id = Ω)**: Currently OMEGA = 0.0 and D_ID = 2.0 imply Id ≠ Ω. Need to align definitions.
2. **Operations ⊕ and ⊗**: Current add/multiply may not match Universe definitions (⊕ as shift by Ω, ⊗ as intersection of rows).
3. **Carrier 𝕌 = Im ∩ Re**: Not implemented.
4. **Spine and Fabric**: Concepts H^n = D^n(Id) and r = p : q missing.
5. **Logarithm L(a)**: Level metric not present.
6. **Dual Numbers**: ε² = Ω currently uses OMEGA = 0.0 (standard dual numbers); may need Ω ≠ 0.
7. **Limits Π and Ω**: PI implemented as fullness; Ω as potential only as constant 0.0.
8. **Ontological Identity**: Not enforced (Id ≡ D(Id) ≡ Π ≡ Π : Π).
9. **Function Application**: No general mechanism for f(a : Ω) derived from f(a).
10. **Scale Invariance**: Operator : not fully utilized as renormalization group.
11. **Information Measure**: Missing depth/length of address interpretation.
12. **Wave Function, Mass, Energy**: Absent from core (may be in nucleus/renderers).

### Other src/core Modules:
- Calculus, topology, number theory, etc., should be derived from refactored algebra and Universe principles.
- Ensure consistency across constants, infinity, states, etc.

### Higher-Level Systems:
- Refactor src/nucleus and src/renderers to use the refactored math core for knowledge systems and visualization.

## Conclusion

The Eugenia project has a partial implementation of U-algebra that draws from the Universe math foundations but requires significant refactoring to fully embody the axioms. The Universe submodule provides a comprehensive mathematical framework that should be the basis for refactoring src/ to achieve true math implementation.

Next steps: Examine specific files in src/core/ to detail current implementations and map them to Universe concepts, then plan refactoring accordingly.
