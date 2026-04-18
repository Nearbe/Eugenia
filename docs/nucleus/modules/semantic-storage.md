# semantic_knowledge_storage.py

**Source:** `src/nucleus/semantic_knowledge_storage.py`

Semantic storage operators, knowledge graph, retrieval, and runtime reconstruction.

## Classes

### `SemanticOperators` (static methods)

```python
class SemanticOperators:
    @staticmethod
    def D_pattern(pattern: np.ndarray) -> np.ndarray
        # Returns np.concatenate([pattern, pattern])  # doubling

    @staticmethod
    def H_pattern(pattern: np.ndarray, target_len: int) -> np.ndarray
        # Averages blocks to target length

    @staticmethod
    def L_pattern(pattern: np.ndarray) -> float
        # Returns log2(sum(pattern^2)) — "depth of structure"
```

### `EigenPattern`

```python
@dataclass
class EigenPattern:
    vector: np.ndarray          # compressed pattern (float16)
    singular_value: float       # importance
    phase: float                # phase angle
    entropy: float              # complexity
```

### `SemanticPatternExtractor`

```python
class SemanticPatternExtractor:
    def __init__(self, k_patterns: int = 32)

    def extract_from_weights(self, W: np.ndarray) -> List[EigenPattern]
        # SVD → list of EigenPattern (k patterns)
        # vector = U[:, i] (float16)
        # phase = angle(U[0,i] + 1j*U[1,i])
        # entropy = -sum(p*log(p)) where p = |v|^2 / sum(|v|^2)

    def extract_relationships(self) -> np.ndarray
        # Returns (k, k) cosine similarity matrix between patterns
```

### `KnowledgeGraph`

> ⚠️ **Not to be confused with** `KnowledgeGraph` in `knowledge_graph.py` — that one works on a **single weight matrix**
> for eigenstructure extraction. This `KnowledgeGraph` builds a multi-layer semantic graph from all model weights and
> stores `EigenPattern` nodes.

```python
class KnowledgeGraph:
    def __init__(self)

    def build_from_model(self, model_weights: Dict[str, np.ndarray],
                         k: int = 32) -> "KnowledgeGraph"
        # For each layer: extracts patterns + relationships
        # Stores in self.nodes (list of EigenPattern)
        # self.edges = np.block(all_relationships)
        # self.layer_index = {layer_name: start_index}

    def semantic_similarity(self, pattern_a: int, pattern_b: int) -> float
    def find_related_patterns(self, pattern_idx: int, top_k: int = 5) -> List[Tuple[int, float]]
    def get_knowledge_structure(self) -> Dict
        # Returns {"n_patterns", "n_relationships", "total_entropy", "layers"}
```

### `SemanticRetrieval`

```python
class SemanticRetrieval:
    def __init__(self, knowledge_graph: KnowledgeGraph)

    def search_by_vector(self, query: np.ndarray, top_k: int = 5) -> List[Tuple[int, float, float]]
        # Returns [(pattern_idx, score, entropy), ...]
        # score = cosine(query, pattern) * log(importance + 1)

    def search_by_layer(self, layer_name: str, top_k: int = 5) -> List[int]
    def semantic_expand(self, pattern_idx: int) -> List[int]
```

### `RuntimeReconstructor`

```python
class RuntimeReconstructor:
    def __init__(self, knowledge_graph: KnowledgeGraph)

    def reconstruct_layer(self, layer_name: str, d_model: int, d_out: int) -> np.ndarray
        # W += importance * outer(vector, vector) for each pattern

    def efficient_forward(self, layer_name: str, x: np.ndarray) -> np.ndarray
        # O(k*d) forward pass via pattern projection
```

### `SemanticStorageFormat` (static methods)

```python
class SemanticStorageFormat:
    @staticmethod
    def serialize(graph: KnowledgeGraph) -> bytes
    @staticmethod
    def deserialize(data: bytes) -> KnowledgeGraph
```

## Key Implementation Details

- `KnowledgeGraph` in this module is DIFFERENT from `KnowledgeGraph` in `knowledge_graph.py`
- `SemanticPatternExtractor` stores patterns as instance attribute `self.patterns`
- `RuntimeReconstructor.reconstruct_layer()` uses outer product reconstruction (approximate)
- `SemanticStorageFormat` uses hardcoded `vec_len = 32` in deserialize (assumes k=32)
- `test_semantic_system()` demo at module level
