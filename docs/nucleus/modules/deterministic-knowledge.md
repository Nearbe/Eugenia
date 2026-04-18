# deterministic_knowledge.py

**Source:** `src/nucleus/deterministic_knowledge.py`

Alternative deterministic core implementation. **Not exported** in `__init__.py` — the `DeterministicKnowledgeCore` from
`deterministic_core.py` is the primary one.

## Classes

### `DeterministicPattern`

```python
@dataclass
class DeterministicPattern:
    vector: np.ndarray      # (d_model, k) — pattern matrix
    singular: np.ndarray    # (k,) — singular values
    phase: float            # phase for alignment
```

### `DeterministicKnowledgeCore`

```python
class DeterministicKnowledgeCore:
    def __init__(self, d_model: int, k: int = 32)

    def learn(self, weight_matrices: dict) -> "DeterministicKnowledgeCore"
        # SVD per layer, stores DeterministicPattern objects
        # Computes cross-layer relationships

    def forward(self, x: np.ndarray) -> np.ndarray
        # Sequential projection through all patterns

    def apply_deterministic(self, x: np.ndarray, layer_idx: int) -> np.ndarray
        # Apply specific layer's transformation

    def get_deterministic_signature(self) -> str
        # Returns "d{d_model}_k{k}_sig{total_singular:.6f}_ph{phase:.4f}"

    def verify_determinism(self, x: np.ndarray, n_tests: int = 10) -> Tuple[bool, float]
```

### `DeterministicFunction`

```python
class DeterministicFunction:
    def __init__(self, k: int = 32)

    def fit(self, weights: dict) -> "DeterministicFunction"
    def __call__(self, x: np.ndarray) -> np.ndarray
    def apply(self, x: np.ndarray, layer: int) -> np.ndarray
    def verify(self, test_input: np.ndarray, n: int = 100) -> dict
```

## Key Differences from deterministic_core.py

| Aspect              | deterministic_core                | deterministic_knowledge         |
|---------------------|-----------------------------------|---------------------------------|
| Pattern type        | `SemanticPattern` (single vector) | `DeterministicPattern` (matrix) |
| Exported            | Yes (in `__init__.py`)            | No                              |
| Serialization       | `serialize()`/`deserialize()`     | None                            |
| `learn()` signature | `weights: Dict[str, np.ndarray]`  | `weight_matrices: dict`         |
| Signature format    | SHA-256 hex                       | Template string                 |
