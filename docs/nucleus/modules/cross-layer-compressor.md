# cross_layer_compressor.py

**Source:** `src/nucleus/cross_layer_compressor.py`

Cross-layer compression via eigenstructure. Standalone functions (no class).

## Functions

### `compress_layer(W, k)` → `dict`

```python
def compress_layer(W, k):
    # SVD → {U: U[:,:k] (float16), S: S[:k] (float16), Vt: Vt[:k,:] (float16)}
    # Returns dict with keys: "U", "S", "Vt"
```

### `decompress_layer(layer)` → `np.ndarray`

```python
def decompress_layer(layer):
    # Returns (U @ diag(S) @ Vt) as float32
    # layer must have keys "U", "S", "Vt"
```

### `cross_layer_pattern(layer1, layer2, k)` → `np.ndarray`

```python
def cross_layer_pattern(layer1, layer2, k):
    # u1 = layer1["U"] * layer1["S"]  # (d, k) — column-wise multiply
    # u2 = layer2["U"] * layer2["S"]  # (d, k)
    # cross = u1.T @ u2  # (k, k)
    # Returns cross.astype(np.float16)
```

## Key Implementation Details

- `cross_layer_pattern()` computes `(U1 * S1).T @ (U2 * S2)`, NOT `(U1*S1).T @ (U2*S2)` with proper broadcasting
- `compress_layer()` uses `full_matrices=False` SVD
- No validation that k <= min(m, n)
- No class wrapper — all standalone functions
- `test_full_model()` and `realistic_llm()` are demo functions at module level
