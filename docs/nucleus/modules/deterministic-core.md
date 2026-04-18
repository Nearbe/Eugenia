# deterministic_core.py

**Source:** `src/nucleus/deterministic_core.py`

Extracts eigenpatterns from weight matrices via SVD. This is the primary core module exported via `__init__.py`.

## Classes

### `SemanticPattern`

```python
@dataclass
class SemanticPattern:
    vector: np.ndarray      # (d_model,) eigenvector
    singular: float         # singular value = importance
    capacity: float         # information capacity (singular * log2(d))
    phase: float            # orientation in radians [0, 2π)
```

**⚠️ Bug:** The dataclass defines `capacity` as the third field, but `DeterministicKnowledgeCore.learn()` passes
`entropy` as the third argument. The serialization/deserialization also use `entropy`. This is a field naming mismatch —
`SemanticPattern` instances will have an `entropy` attribute (set by learn()), not `capacity`.

### `PatternRelationship`

```python
@dataclass
class PatternRelationship:
    layer_from: str         # source layer name
    layer_to: str           # target layer name
    matrix: np.ndarray      # (k, k) cross-correlation matrix
```

### `DeterministicKnowledgeCore`

```python
class DeterministicKnowledgeCore:
    def __init__(self, d_model: int = 4096, k: int = 32)

    def learn(self, weights: Dict[str, np.ndarray]) -> "DeterministicKnowledgeCore"
        # Extracts patterns from each weight matrix via SVD
        # Stores top-k patterns per layer
        # Builds relationships between adjacent layers
        # Generates deterministic signature
        # Returns self (fluent)

    def forward(self, input_vec: np.ndarray, layer: str) -> np.ndarray
        # Projects input through pattern for given layer
        # Returns deterministic output

    def get_signature(self) -> str
        # Returns 16-char hex SHA-256 of all pattern vectors

    def verify_determinism(self, test_input: np.ndarray, n_runs: int = 100) -> Dict
        # Runs forward() n_runs times, checks all outputs identical
        # Returns {"is_deterministic": bool, "max_variation": float, "signature": str}

    def get_compressed_size(self) -> int
        # Returns total bytes of all patterns + relationships
```

## Serialization

### `serialize(core)` → `bytes`

Binary format:
`<d_model><k><n_patterns><name_len><name><vector><singular><entropy><phase>...><n_rels><name_len><name><matrix>...><signature>`

### `deserialize(data: bytes)` → `DeterministicKnowledgeCore`

Reconstructs core from serialized bytes. Uses `float16` for vectors.

## Key Implementation Details

- `learn()` uses `np.linalg.svd(W, full_matrices=False)` for each layer
- Top-k patterns: `U[:, :k].flatten()[:d_model]` (may truncate if k*d_model > vector size)
- Singular value: `S[0]` (most important only, not all k)
- Relationships: computed between adjacent layers via `_compute_cross_relation()` (absolute dot product of normalized
  vectors)
- Signature: SHA-256 of concatenated pattern vectors + singular values, first 16 hex chars
