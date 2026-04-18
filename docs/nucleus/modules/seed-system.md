# nucleus_seed_system.py

**Source:** `src/nucleus/nucleus_seed_system.py`

Deterministic correlation-based pattern generation from geometric seeds.

## Data

### `BASE_SEEDS`

```python
BASE_SEEDS = {
    "point":    np.array([1.0, 0.0, 0.0, 0.0]),
    "line":     np.array([0.0, 1.0, 0.0, 0.0]),
    "angle":    np.array([0.0, 0.0, 1.0, 0.0]),
    "plane":    np.array([0.0, 0.0, 0.0, 1.0]),
    "circle":   np.array([1.0, 1.0, 0.0, 0.0]),
    "square":   np.array([1.0, 0.5, 0.5, 0.0]),
    "triangle": np.array([0.0, 1.0, 1.0, 0.0]),
    "sphere":   np.array([1.0, 1.0, 1.0, 0.0]),
    "chain":    np.array([0.0, 0.5, 0.5, 1.0]),
    "tree":     np.array([0.0, 0.0, 0.0, 0.5]),
    "ring":     np.array([1.0, 1.0, 0.0, 0.5]),
    "net":      np.array([0.0, 0.0, 1.0, 1.0]),
}
```

## Classes

### `Seed`

```python
@dataclass
class Seed:
    seed_id: str
    representation: np.ndarray
    description: str
    basic: bool = True
```

### `CorrelationEngine`

```python
class CorrelationEngine:
    def __init__(self, base_dim: int = 4)
        # Initializes 12 seeds from BASE_SEEDS

    def get_correlation(self, a: str, b: str) -> float
        # Cosine similarity between seed vectors
        # For unknown patterns: deterministic SHA-256 hash → vector
        # Truncates to min dimension

    def _get_vector(self, pattern_id: str) -> np.ndarray
        # Returns seed representation or deterministic hash vector

    def expand_seed(self, base_seed_id: str, depth: int = 3) -> List[Tuple[str, float]]
        # Returns top patterns correlated with seed (|corr| > 0.1)
        # Returns [(name, correlation), ...] sorted by |corr|

    def find_bridges(self, from_seed: str, to_seed: str, max_hops: int = 3) -> Dict
        # Returns {"from", "to", "bridges": set, "strength": list, "common_count": int}
```

### `Explorer`

```python
class Explorer:
    def __init__(self)
        # self.engine = CorrelationEngine()
        # self.found_correlations = {}
        # self.explored_seeds = set()

    def explore_from(self, seed_id: str, depth: int = 2) -> Dict
        # Returns {target: {"correlation": float, "is_seed": bool}, ...}

    def discover_path(self, from_id: str, to_id: str) -> List[Tuple[str, float]]
        # Direct if |corr| > 0.5, else via bridges

    def query(self, concept: str) -> Dict
        # Returns correlations with all BASE_SEEDS (|corr| > 0.2)
```

## Key Implementation Details

- Unknown pattern vectors: SHA-256 of name → first 16 bytes as uint8 → float → normalize → pad to `base_dim + 12`
- `expand_seed()` returns `depth * 3` top correlated seeds
- `find_bridges()` computes intersection of expanded sets from both ends
- `demo()` function at module level
