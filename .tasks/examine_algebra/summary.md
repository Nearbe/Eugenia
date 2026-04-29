# Summary of src/core/algebra Files

## Overview
The `src/core/algebra` directory contains the implementation of U-algebra, dual numbers, and related operations. The files are organized into helper functions for type checking and operation implementations.

## File Summaries

### `__init__.py`
- ** Purpose **: Public API for the algebra module.
- ** Key Definitions **: 
  - Exports functions: `branch`, `compress`, `add`, `multiply`, `divide`, `power`, `lift`, `is_omega`, `is_identity`, `IDENTITY`.
  - Exports classes: `BranchingOperator`.
  - Exports constants: `branching_operator`, `SCALAR_BASIS_SIZE`, `DUAL_BASIS_SIZE`.

### `_dual_number.py`
- ** Purpose **: Helper to check if a value is a dual number.
- ** Key Definitions **:
  - Function `_dual_number(value)`: Returns the value as a `DualNumber` if it is one, otherwise `None`.

### `_complex_fullness.py`
- ** Purpose **: Helper to check if a value is a complex fullness.
- ** Key Definitions **:
  - Function `_complex_fullness(value)`: Returns the value as a `ComplexFullness` if it is one, otherwise `None`.

### `_complex_state.py`
- ** Purpose **: Helper to check if a value is a complex state.
- ** Key Definitions **:
  - Function `_complex_state(value)`: Returns the value as a `ComplexState` if it is one, otherwise `None`.

### `_fullness_share.py`
- ** Purpose **: Helper to check if a value is a fullness share.
- ** Key Definitions **:
  - Function `_fullness_share(value)`: Returns the value as a `FullnessShare` if it is one, otherwise `None`.

### `_participation_ratio.py`
- ** Purpose **: Helper to check if a value is a participation ratio.
- ** Key Definitions **:
  - Function `_participation_ratio(value)`: Returns the value as a `ParticipationRatio` if it is one, otherwise `None`.

### `_spine_level.py`
- ** Purpose **: Helper to check if a value is a spine level.
- ** Key Definitions **:
  - Function `_spine_level(value)`: Returns the value as a `SpineLevel` if it is one, otherwise `None`.

### `add.py`
- ** Purpose **: Implements U-addition with type dispatching.
- ** Key Definitions **:
  - Function `add(left, right)`: 
    - Handles dual numbers, fullness shares, complex fullness, complex states, participation ratios, and fullness (PI) with specific rules.
    - Falls back to ordinary addition for finite values.

### `branch.py`
- ** Purpose **: Implements the branching operator D(value) = value : Ω.
- ** Key Definitions **:
  - Function `branch(value)`: 
    - Dispatches to the appropriate branching method based on the type of value (dual, share, complex, spine, participation ratio, fullness).
    - For finite values, multiplies by the constant `D_ID`.

### `compress.py`
- ** Purpose **: Implements the compression operator H(value) = value : D(Id).
- ** Key Definitions **:
  - Function `compress(value)`: 
    - Similar dispatching as `branch` but uses compression methods.
    - For finite values, divides by the constant `D_ID`.

### `divide.py`
- ** Purpose **: Implements U-division with specific rules.
- ** Key Definitions **:
  - Function `divide(numerator, denominator)`: 
    - Implements the rules:
      - `a : Ω = D(a)` for active finite `a`.
      - `Ω : b = Ω` for finite `b`.
      - `Ω : Ω = Ω`.
      - `Π : Ω = Π`, `Π : D(Id) = Π`, `Π : Π = Id`.
      - Otherwise ordinary real division.
    - Handles dual numbers, fullness shares, complex fullness, complex states, participation ratios, and fullness/omega constants.

### `identity.py`
- ** Purpose **: Defines the identity constant.
- ** Key Definitions **:
  - Constant `IDENTITY = 1.0`.

### `is_identity.py`
- ** Purpose **: Checks if a value is the finite identity.
- ** Key Definitions **:
  - Function `is_identity(value)`: 
    - Returns True if value equals `IDENTITY` or if it is a spine level with depth 0.

### `is_omega.py`
- ** Purpose **: Checks if a value is the U-system potential Ω.
- ** Key Definitions **:
  - Function `is_omega(value)`: 
    - Returns True if value is a numeric type (int/float, not bool) and equals the constant `OMEGA`.

### `lift.py`
- ** Purpose **: Lifts a scalar operation to finite scalars or vectors.
- ** Key Definitions **:
  - Function `lift(value, operation)`: 
    - Applies the operation to finite scalars or vectors using vectorization utilities.

### `multiply.py`
- ** Purpose **: Implements U-multiplication with type dispatching.
- ** Key Definitions **:
  - Function `multiply(left, right)`: 
    - Handles dual numbers, fullness shares, complex fullness, complex states, participation ratios.
    - Returns `OMEGA` if either operand is Ω.
    - Returns `PI` if either operand is fullness (Π).
    - Falls back to ordinary multiplication for finite values.

### `power.py`
- ** Purpose **: Implements U-power with special cases for Ω and Π.
- ** Key Definitions **:
  - Function `power(base, exponent)`: 
    - Handles dual numbers and spine levels with special returns for Ω and Π exponents.
    - Returns `PI` if base is fullness.
    - Returns `OMEGA` if both base and exponent are Ω.
    - Returns `IDENTITY` if exponent is Ω (for finite base).
    - Returns `PI` if exponent is fullness (for finite base).
    - Falls back to ordinary power for finite values.

### `branching_operator.py`
- ** Purpose **: Defines the branching operator class and constants.
- ** Key Definitions **:
  - Constants `SCALAR_BASIS_SIZE = 1`, `DUAL_BASIS_SIZE = 2`.
  - Class `BranchingOperator`:
    - Attributes: `eigenvalue` (default `D_ID`).
    - Methods: `apply` (branching), `inverse` (compression), `eigen_class`, `kernel`, `image_is_carrier`, `scalar_matrix`, `dual_matrix`, `is_linear_on_pair`.
  - Instance `D_OPERATOR` and function `branching_operator()` to return it.

## Observations
- The algebra is built around a type dispatching system where each operation checks the type of its arguments (via helper functions) and delegates to the appropriate type-specific method.
- The types involved include dual numbers, fullness shares, complex fullness, complex states, participation ratios, spine levels, and the special constants Ω (omega) and Π (pi).
- The constants `D_ID` and `OMEGA` are imported from `..constants.constants`.
- The implementation follows the U-algebra principles as described in the project's foundations.

## Next Steps for Refactoring
To refactor based on Universe foundations, we would need to:
1. Replace the current type dispatching with a more formal algebraic structure based on the Universe module.
2. Ensure that the operations align with the mathematical definitions from the Universe foundations.
3. Possibly introduce new types or restructure existing ones to match the foundational concepts.
