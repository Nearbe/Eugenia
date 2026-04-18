# universal_knowledge_map.py

**Source:** `src/nucleus/universal_knowledge_map.py`

Universal pattern projection system. Projects any input through a learned pattern matrix to a fixed-dimensional space.

## Classes

### `UniversalKnowledgeMap`

```python
@dataclass
class UniversalKnowledgeMap:
    pattern_matrix: np.ndarray   # (d_model, k) — learned eigenvectors
    singular_values: np.ndarray  # (k,) — importance weights
```

**Note:** `self.k` IS set from `len(singular_values)` in `__init__`. `self.d` is NOT set — the docstring claims it but
the code doesn't store it.

```python
ukm = UniversalKnowledgeMap(pattern_matrix, singular_values)

# Methods:
ukm.project(x: np.ndarray) -> np.ndarray
    # Returns: P^T @ x * s  (shape: k,)

ukm.similarity(x1: np.ndarray, x2: np.ndarray) -> float
    # Cosine similarity of projections in range [0, 1]
    # Returns 0.0 if either norm < 1e-10

ukm.encode(x: np.ndarray) -> np.ndarray
    # Alias for project()

ukm.decode(pattern_coords: np.ndarray) -> np.ndarray
    # Returns: pattern_matrix @ pattern_coords
```

### `KnowledgeNavigator`

```python
class KnowledgeNavigator:
    def __init__(self, knowledge_map: UniversalKnowledgeMap)

    def find_similar(self, query: np.ndarray, candidates: List[np.ndarray], top_k: int = 5) -> List[tuple]
        # Returns [(index, similarity, candidate_projection), ...]
        # Sorted by similarity descending

    def cluster(self, items: List[np.ndarray]) -> List[List[int]]
        # Simple clustering by first two projection dimensions
        # Key: (int(p[0]*2), int(p[1]*2))

    def dimension_analysis(self, item: np.ndarray) -> Dict
        # Returns {"pattern_dims": [...], "pattern_weights": [...], "total_activation": float, "dimensionality": float}
```

## Key Implementation Details

- `project()` does NOT normalize — raw dot product scaled by singular values
- `similarity()` uses raw dot product in `KnowledgeNavigator.find_similar()`, NOT cosine
- `cluster()` uses a very simplified approach (first 2 dims, coarse binning)
- `demonstrate_universal_mapping()` demo function at module level
- `demonstrate_gpt_embedding()` docstring comparison function at module level
