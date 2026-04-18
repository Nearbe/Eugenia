# correlation_compressor.py

**Source:** `src/nucleus/correlation_compressor.py`

Four weight compression strategies via correlation analysis.

## Class

### `CorrelationCompressor`

```python
class CorrelationCompressor:
    def __init__(self)
        # self.delta = None
        # self.correlation_eigen = None
        # self.graph = None

    def compress_delta(self, W, init_type="random") -> Tuple[np.ndarray, np.ndarray]
        # Returns (delta, W_init)
        # init_type: "random" (N(0,0.01)), "zeros", "xavier" (N(0, sqrt(2/(m+n))))

    def compress_correlation_svd(self, W, k=None) -> dict
        # Stores in self.correlation_eigen
        # Returns {"U": U[:,:k] (float16), "S": S[:k] (float16), "Vt": Vt[:k,:] (float16), "k": k, "shape": W.shape}
        # Default k = min(32, min(m, n))

    def decompress_correlation_svd(self) -> np.ndarray
        # Returns U @ diag(S) @ Vt (float32)

    def compress_graph(self, W, threshold=0.5) -> Tuple[bytes, float]
        # Returns (binary_data, sparsity_ratio)
        # Stores sparse weights as: <m,n><n_edges><row,col pairs><scale><quantized_values>

    def compress_hessian_pattern(self, W) -> np.ndarray
        # Returns H = W @ W.T (correlation/curvature approximation)
```

## Key Implementation Details

- `compress_correlation_svd()` stores SVD in instance variable, not return value only
- `compress_graph()` uses int8 quantization with scale factor
- All random init types use `np.random.randn()` — not seeded
- `decompress_correlation_svd()` converts float16 back to float32 before reconstruction
