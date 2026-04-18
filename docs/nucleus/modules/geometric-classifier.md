# universal_geometric_classifier.py

**Source:** `src/nucleus/universal_geometric_classifier.py`

Geometry-based few-shot classification. Works on any data type via binary sweep + topological features.

## Classes

### `GeometricProfile`

```python
@dataclass
class GeometricProfile:
    binary_histogram: np.ndarray      # sweep histogram (n_thresholds,)
    jump_events: List[Tuple[float, float, float, float]]  # (threshold, before, after, jump_size)
    betti_signature: np.ndarray        # [betti0_profile, betti1_profile]
    capacity: float                    # information capacity
    phase_signature: np.ndarray        # first 10 FFT phase coefficients
```

### `GeometricExtractor`

> ⚠️ **Not to be confused with** `GeometricExtractor` in `nucleus_knowledge_system.py` — that one accepts **any data
type** (strings, arrays, numbers) and returns a raw `np.ndarray`. This one works only on numpy arrays and returns a
`GeometricProfile` dataclass.

```python
class GeometricExtractor:
    def __init__(self, n_thresholds: int = 100, jump_threshold: float = 1.0)

    def extract(self, data: np.ndarray) -> GeometricProfile
        # 1. Flatten + normalize to [0,1]
        # 2. Binary sweep: binary_histogram[i] = mean(data > thresholds[i])
        # 3. Jump events: |diff(binary_histogram)| > jump_threshold/100
        # 4. Betti signature: simplified region counting at subsampled thresholds
        # 5. Capacity: S[0] / S.sum() from SVD
        # 6. Phase: angle(FFT(data)[:10])

    def _count_regions_simplified(self, binary: np.ndarray) -> Dict[str, int]
        # Counts connected components via flood fill
        # Approximates betti1 from transition count
```

### `UniversalGeometricClassifier`

```python
class UniversalGeometricClassifier:
    def __init__(self, n_thresholds: int = 100)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "UniversalGeometricClassifier"
        # For each unique class: extracts profile from X[y==cls][0]
        # Stores in self.class_profiles[int(cls)]
        # Returns self (fluent)

    def predict(self, x: np.ndarray) -> int
        # Extracts profile, returns class with highest similarity score

    def _similarity(self, p1: GeometricProfile, p2: GeometricProfile) -> float
        # score = 0.4*corr(hist1, hist2) + 0.2*jump_sim + 0.3*betti_sim + 0.1*cap_sim
        # jump_sim = 1 - min(|n1-n2|, 10) / 10
        # betti_sim = 1 - ||b1-b2|| / (||b1|| + 1e-10)
        # cap_sim = 1 - |c1-c2| / max(c1,c2) + 1e-10

    def get_compressed_size(self) -> int
        # Returns total bytes of all class profiles
```

## Key Implementation Details

- `fit()` uses only the FIRST sample per class (not averaging)
- `_count_regions_simplified()` uses flood fill on flattened array (not 2D)
- `predict()` returns `int` class label
- `signature`: SHA-256 of binary_histogram + capacity per class, first 16 hex chars
- `test_mnist_classification()` demo uses synthetic data (no real MNIST loading)
