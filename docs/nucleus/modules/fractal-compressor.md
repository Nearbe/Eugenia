# fractal_compressor.py

**Source:** `src/nucleus/fractal_compressor.py`

Iterative multi-level SVD compressor (radical compression).

## Class

### `RadicalCompressor`

```python
class RadicalCompressor:
    def __init__(self, levels=4, base_k=4)

    def compress(self, W) -> Tuple[list, float]
        # Returns (components, first_error)
        # components: list of dicts per level
        #   each: {"U": (m,k) float16, "S": (k,) float16, "V": (k,n) float16, "k": k, "shape": (m,n)}
        # first_error: ||residual_1|| / ||W||
        # k decreases exponentially: k_i = base_k * 2^(levels-i-1)

    def decompress(self) -> np.ndarray
        # Returns sum of all level reconstructions as float32
        # W = Σ_i (U_i @ diag(S_i) @ V_i)
```

## Key Implementation Details

- k at each level: `base_k * 2^(levels - level - 1)`, capped at `min(residual.shape) - 1`
- Breaks loop if k < 2
- Components stored as float16 (2x compression vs float32)
- `compress()` resets `self.components = []` at start
- No pattern matching or deduplication implemented (despite docstring claims)
- `test_radical()`, `realistic_llm_weights()`, `final_analysis()` are demo functions
