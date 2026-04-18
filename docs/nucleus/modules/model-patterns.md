# nucleus_model_patterns.py

**Source:** `src/nucleus/nucleus_model_patterns.py`

Model weight loading and pattern extraction. Supports GGUF, MLX, safetensors, PyTorch formats.

## Classes

### `ModelProfile`

```python
@dataclass
class ModelProfile:
    name: str
    svd_U: np.ndarray      # (m, k)
    svd_S: np.ndarray      # (k,)
    svd_Vt: np.ndarray     # (k, n)
    k: int
    original_shape: Tuple[int, ...]
    layer_type: str
    n_params: int

    @property
    def compression_ratio(self) -> float
        # Returns: k * (m + n) / (m * n)

    def save(self, path: str)
        # Saves to .npz format

    @classmethod
    def load(cls, path: str) -> "ModelProfile"
        # Loads from .npz format
```

### `ModelLoader`

```python
class ModelLoader:
    SUPPORTED_FORMATS = {".gguf", ".mlx", ".safetensors", ".pt", ".pth"}

    def __init__(self, model_dir: str)

    def discover_models(self) -> List[Dict]
        # Returns [{"path", "name", "parent", "format", "size"}, ...]

    def load_safetensors(self, path: str) -> Dict[str, np.ndarray]
        # Uses safetensors.safe_open if available, falls back to _load_generic

    def _load_generic(self, path: str) -> Dict[str, np.ndarray]
        # Tries np.load with allow_pickle

    def load_layer(self, path: str, layer_name: Optional[str] = None) -> Optional[np.ndarray]
        # Extracts single layer by name or returns first layer
```

### `PatternExtractor`

```python
class PatternExtractor:
    def __init__(self, k: int = 16)

    def extract_from_weights(self, weights: np.ndarray, layer_name: str = "linear",
                             layer_type: str = "linear") -> ModelProfile
        # SVD → ModelProfile with top-k components

    def extract_all_layers(self, layers: Dict[str, np.ndarray],
                           k: Optional[int] = None) -> Dict[str, ModelProfile]

    def compress_weights(self, profile: ModelProfile,
                         coefficients: Optional[np.ndarray] = None) -> np.ndarray
        # Returns U @ (coefficients * Vt)

    def get_pattern_geometry(self, profile: ModelProfile) -> dict
        # Returns {"name", "layer_type", "k", "n_params", "singular_values",
        #          "singular_norm", "entropy", "energy_concentration",
        #          "original_shape", "compression_ratio"}

    def generate_profile_image(self, profile: ModelProfile,
                               size: int = 128) -> np.ndarray
        # Generates (size, size, 3) RGB visualization of singular values
```

## Key Implementation Details

- `ModelLoader` uses `safetensors.safe_open` for safetensors files
- `PatternExtractor.compress_weights()` reconstructs as `U @ (coefficients * Vt)`, NOT `U @ diag(coefficients) @ Vt`
- `generate_profile_image()` creates a colorful visualization from singular values
- `demo_extraction()` at module level searches `~/.lmstudio/models/` for Gemma models
