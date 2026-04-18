# universal_knowledge_protocol.py

**Source:** `src/nucleus/universal_knowledge_protocol.py`

Layer-specific universal knowledge protocol. Extends `UniversalKnowledgeMap` with per-layer maps and serialization.

## Classes

### `UniversalMap`

```python
@dataclass
class UniversalMap:
    P: np.ndarray          # (d_model, k) — eigenvectors (float16)
    S: np.ndarray          # (k,) — singular values (float16)
    k: int                 # number of patterns
    d: int                 # input dimension
```

### `UniversalKnowledgeProtocol`

```python
class UniversalKnowledgeProtocol:
    def __init__(self, k: int = 32)

    def learn(self, weights: Dict[str, np.ndarray]) -> "UniversalKnowledgeProtocol"
        # For each layer: SVD → UniversalMap(P=U[:,:k], S=S[:k], k=k, d=layer_dim)
        # Stores in self.maps[layer_name]
        # Generates signature

    def encode(self, layer: str, x: np.ndarray) -> np.ndarray
        # Returns: P.T @ x.astype(float32) * S.astype(float32)
        # Uses safe_divide and has_potential/resolve_potential from core.math

    def similarity(self, layer: str, x1: np.ndarray, x2: np.ndarray) -> float
        # Encodes both, computes cosine similarity
        # Returns 1.0 if both zero, 0.0 if one zero

    def cluster(self, layer: str, items: List[np.ndarray], n_clusters: int = 5) -> List[List[int]]
        # Simplified: assigns items[i] to cluster i % n_clusters

    def get_compressed_size(self) -> int
        # Sum of P.nbytes + S.nbytes for all maps

    def save(self) -> bytes
        # Binary: <k><n_maps><name_len><name><d><P_bytes><S_bytes>...><signature>

    @classmethod
    def load(cls, data: bytes) -> "UniversalKnowledgeProtocol"
        # Deserializes from binary format
```

## Key Implementation Details

- Uses `src.core.math.safe_divide`, `has_potential`, `resolve_potential` for edge cases
- `cluster()` is a placeholder — does round-robin assignment, not real clustering
- Signature: SHA-256 of all P + S bytes, first 16 hex chars
- `demo()` function at module level
