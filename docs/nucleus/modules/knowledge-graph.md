# knowledge_graph.py

**Source:** `src/nucleus/knowledge_graph.py`

SVD graph builder for a **single weight matrix**. Extracts eigenstructure from one layer's weights and builds a node
vector representation.

> ⚠️ **Not to be confused with** `KnowledgeGraph` in `semantic_knowledge_storage.py` — that one builds a graph from *
*all model layers** and stores `EigenPattern` nodes. This class works on a single `W` matrix and stores embeddings as
> dicts.

## Class

### `KnowledgeGraph`

```python
class KnowledgeGraph:
    def __init__(self)
        # self.nodes = None
        # self.edges = None
        # self.embeddings = None

    def build_from_weights(self, W, k=32) -> dict
        # SVD of single weight matrix
        # Returns {"left": U[:,:k] (float16), "singular": S[:k] (float16), "right": Vt[:k,:] (float16)}
        # Also stores in self.embeddings

    def get_node_vector(self, idx) -> np.ndarray
        # Returns embeddings['left'][idx] * embeddings['singular']
        # idx must be < left.shape[0]

    def similarity(self, i, j) -> float
        # Cosine similarity between node vectors i and j
        # Returns value in [-1, 1]
```

## Key Implementation Details

- `build_from_weights()` uses `full_matrices=False` SVD
- Embeddings stored as float16 (2x compression)
- `get_node_vector()` computes weighted representation: `U[idx,:] * S`
- `similarity()` uses `+ 1e-10` denominator for numerical stability
- `nodes`, `edges` attributes are never set — they remain `None` (unused)
- `extract_knowledge_structure()`, `knowledge_retrieval()`, `memory_efficient_inference()` are standalone demo functions

## Role in Pipeline

**Phase: Weight Analysis** — extracts eigenstructure from individual weight matrices. Used for compression analysis and
pattern extraction from a single layer. Not used for multi-layer knowledge graph construction.
