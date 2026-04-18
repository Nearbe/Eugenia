# nucleus_hybrid.py

**Source:** `src/nucleus/nucleus_hybrid.py`

DET/RND/HYBRID mode system for flexible computation.

## Classes

### `Mode` (Enum)

```python
class Mode(Enum):
    DET = "deterministic"   # Exact, reproducible
    RND = "random"          # Variable, creative
    HYBRID = "hybrid"       # Combination
```

### `HybridProcessor`

```python
@dataclass
class HybridProcessor:
    mode: Mode = Mode.HYBRID
    seed_value: int = 42

    def __init__(self, mode: Mode = Mode.HYBRID, seed: int = 42)
        # Initializes self._rng = np.random.default_rng(seed)

    def set_mode(self, mode: Mode)

    def compute_correlation(self, a: str, b: str) -> float
        # DET: returns base hash (deterministic)
        # RND: base + uniform(-0.1, 0.1)
        # HYBRID: 50/50 RND or base

    def find_path(self, from_node: str, to_node: str, max_hops: int = 3) -> List[str]
        # DET: [from_node, to_node]
        # RND: [from_node, intermediate_0..N, to_node]
        # HYBRID: 50/50 DET or HYBRID path

    def evaluate(self, node: str) -> float
        # DET: deterministic hash score
        # RND/HYBRID: score + normal(0, 0.1) noise
```

## Key Implementation Details

- `compute_correlation()` base: SHA-256 of (a+b), first 4 bytes as big-endian int, mod 1000 / 1000
- `evaluate()` base: SHA-256 of node, first 4 bytes as big-endian int, mod 100 / 100
- `find_path()` RND uses `self._rng.integers(0, 100)` for intermediate node names
- `find_path()` HYBRID uses `self._rng.random() > 0.5` to choose between DET path and bridge path
