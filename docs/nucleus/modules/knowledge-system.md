# nucleus_knowledge_system.py

**Source:** `src/nucleus/nucleus_knowledge_system.py`

Core knowledge absorption and generation system. Absorbs any data type, builds correlation graph, generates related
patterns.

## Classes

### `PatternNode`

```python
@dataclass
class PatternNode:
    node_id: str                # unique identifier
    pattern: np.ndarray         # geometric profile
    correlations: Dict[str, float] = field(default_factory=dict)  # node_id → strength
    usage_count: int = 0
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
```

### `GeometricExtractor`

> ⚠️ **Not to be confused with** `GeometricExtractor` in `universal_geometric_classifier.py` — that one extracts
`GeometricProfile` (dataclass) from numpy arrays only. This `GeometricExtractor` accepts **any data type** (strings,
> arrays, numbers) and returns a raw `np.ndarray` profile.

```python
class GeometricExtractor:
    def __init__(self, n_thresholds: int = 64)

    def extract(self, data: Any) -> np.ndarray
        # Normalizes any input to [0,1]
        # Binary sweep: thresholds = linspace(0, 1, n_thresholds)
        # Computes: binary_profile + jumps * 10 + topology[:16]
        # Returns concatenated profile array

    def _normalize(self, data: Any) -> np.ndarray
        # str → ord(c) normalized
        # np.ndarray → flatten, normalize to [0,1]
        # else → float(data), normalize

    def similarity(self, p1: np.ndarray, p2: np.ndarray) -> float
        # Cosine similarity
```

### `KnowledgeSystem`

```python
class KnowledgeSystem:
    def __init__(self, similarity_threshold: float = 0.7)

    def absorb(self, data: Any, label: Optional[str] = None) -> str
        # Extracts pattern, creates PatternNode, auto-relates to existing
        # Returns node_id

    def _auto_relate(self, node_id: str)
        # Compares new node to all existing nodes
        # If similarity > threshold, creates bidirectional correlation

    def relate(self, source_id: str, target_id: str, strength: float = 1.0)
        # Creates bidirectional correlation

    def strengthen(self, node_id: str)
        # Increments usage_count, boosts related correlations by 5%

    def generate(self, context_node_id: str, max_nodes: int = 5) -> List[str]
        # Returns top-k related node_ids by correlation strength
        # Also strengthens returned nodes

    def find_similar(self, data: Any, top_k: int = 3) -> List[Tuple[str, float]]
        # Extracts query pattern, returns [(node_id, similarity), ...]

    def query(self, data: Any) -> Dict[str, Any]
        # Full query: find similar → strengthen → generate
        # Returns {"status": "new"|"existing", ...}

    def get_stats(self) -> Dict[str, Any]
        # Returns {"total_nodes", "total_correlations", "most_used_node", "most_used_count"}
```

## Key Implementation Details

- `GeometricExtractor` uses a simplified topology (region counting, not real Betti numbers)
- `KnowledgeSystem._auto_relate()` only connects nodes with similarity > 0.7
- `strengthen()` boosts correlations multiplicatively (1.05x), capped at 1.0
- `generate()` strengthens returned nodes (feedback loop)
- `demo()` function at module level
