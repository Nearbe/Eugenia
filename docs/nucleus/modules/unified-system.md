# nucleus_unified.py

**Source:** `src/nucleus/nucleus_unified.py`

Unified system combining pattern extraction, geometric rendering, and duality.

## Classes

### `TaskMode` (Enum)

```python
class TaskMode(Enum):
    INFERENCE = "inference"     # Deterministic generation
    EXPLORATION = "exploration" # Random exploration
    HYBRID = "hybrid"           # Balanced
```

### `NucleusState`

```python
@dataclass
class NucleusState:
    duality: DualState
    graphics_engine: GeometricEngine
    pattern_extractor: PatternExtractor
    loaded_profiles: Dict[str, ModelProfile]
    active_model: Optional[str]
```

### `NucleusUnified`

```python
class NucleusUnified:
    def __init__(self, k: int = 16)

    def load_model(self, model_path: str) -> bool
        # Discovers model format, loads layers, extracts SVD patterns
        # Registers profiles in graphics engine
        # Returns True on success

    def _profile_to_geo(self, model_profile: ModelProfile) -> GeometricProfile
        # Converts ModelProfile → GeometricProfile
        # Creates synthetic binary representation from singular values

    def generate(self, prompt: str, mode: TaskMode = TaskMode.HYBRID,
                 width: int = 512, height: int = 512,
                 formula: str = "mandelbrot") -> np.ndarray
        # Uses duality for exploration factor
        # Renders fractal with profile boost
        # Returns (height, width, 3) uint8 image

    def learn_from_feedback(self, success: bool, boost: float = 0.1)
        # Updates duality state, boosts graphics correlations

    def _update_stats(self)
        # Updates total_patterns, compression_ratio

    def get_state(self) -> dict
        # Returns current system state snapshot
```

## Key Implementation Details

- `generate()` uses first available model profile regardless of prompt
- `_profile_to_geo()` creates synthetic 2D binary representation from singular values
- `load_model()` only supports `.safetensors` and `.npy` directly
- Bug: `demo_unified()` references `eugenia` instead of `nucleus` variable name
