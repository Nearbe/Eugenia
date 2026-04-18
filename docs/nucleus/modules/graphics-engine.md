# nucleus_graphics.py

**Source:** `src/nucleus/nucleus_graphics.py`

Geometric rendering engine. Renders fractals and topological visualizations from pattern profiles.

## Classes

### `RenderMode` (Enum)

```python
class RenderMode(Enum):
    SDF = "sdf"
    FRACTAL = "fractal"
    HORIZON = "horizon"
    PHASE = "phase"
    TOPOLOGY = "topology"
```

### `GeometricProfile`

```python
@dataclass
class GeometricProfile:
    bits: np.ndarray          # (n_thresholds, H, W) binary layers
    thresholds: np.ndarray    # (n_thresholds,) threshold values
    centroids: np.ndarray     # (n_components, 2) component centroids
    betti: Tuple[int, int]    # (betti0, betti1)
    euler: int                # euler characteristic
    capacity: float           # information capacity
    complexity: float         # complexity score
```

### `RenderParams`

```python
@dataclass
class RenderParams:
    width: int = 512
    height: int = 512
    zoom: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    iterations: int = 100
    escape_radius: float = 4.0
    Julia_c: Optional[complex] = None
```

### `GeometricEngine`

```python
class GeometricEngine:
    def __init__(self)
        # self.profiles = {}
        # self.correlations = {}
        # self.render_cache = {}
        # self._svd_basis = None

    def register_profile(self, name: str, profile: GeometricProfile)
    def boost_correlation(self, name: str, boost: float = 0.1)
    def get_correlation_strength(self, name: str) -> float

    def compute_profile(self, data: np.ndarray, n_thresholds: int = 50) -> GeometricProfile
        # Binary sweep → GeometricProfile

    def render_sdf(self, params: RenderParams, profile: Optional[GeometricProfile] = None) -> np.ndarray
        # SDF rendering with profile overlay

    def render_fractal(self, formula: str = "mandelbrot", params: RenderParams = None,
                       profile: Optional[GeometricProfile] = None, boost: bool = True) -> np.ndarray
        # Supports: "mandelbrot", "julia", "burning_ship", "newton"
        # Returns (H, W, 3) uint8 image

    def render_horizon(self, profile: GeometricProfile, params: RenderParams = None) -> np.ndarray
        # Threshold layer visualization

    def compress_profiles(self, k: int = 16) -> dict
        # SVD of all profile bits → self._svd_basis

    def generate_from_basis(self, coefficients: np.ndarray, params: RenderParams = None) -> np.ndarray
        # Reconstruct from SVD basis coefficients
```

## Key Implementation Details

- `compute_betti_numbers`, `compute_euler_characteristic`, `compute_information_capacity` imported from `src.core.math`
  if available, else local stubs
- `_count_components()` uses iterative flood fill (not scipy.ndimage)
- `_render_mandelbrot()` uses element-wise operations (not vectorized)
- `_color_by_capacity()` uses sinusoidal color mapping
- `boost_correlation()` caps strength at 10.0
- `demo_unified()` in `nucleus_unified.py` references `eugenia` variable (bug)
