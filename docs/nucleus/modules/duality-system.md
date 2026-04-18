# nucleus_duality.py

**Source:** `src/nucleus/nucleus_duality.py`

Omega (Ω, potential) ↔ Pi (Π, completeness) duality system. Models the transition between uncertainty and determinism.

## Classes

### `DualState`

```python
@dataclass
class DualState:
    omega: float    # uncertainty (potential)
    pi: float       # determinism (completeness)
```

**Properties:**

- `delta` → `np.log(abs(pi / omega))` via `safe_divide`
- `is_deterministic` → `self.pi > self.omega`
- `is_exploratory` → `self.omega > self.pi`

### `UnifiedSystem`

```python
class UnifiedSystem:
    def __init__(self, balance: float = 0.5)
        # balance 0 = full chaos (omega=1), 1 = full determinism (pi=1)

    def transition(self, input_data: str, exploration_factor: float = 0.1) -> Tuple[str, DualState]
        # Returns (result, new_state)
        # DET mode: stable result, strengthens pi
        # RND mode: result + sinusoidal variation, weakens pi
        # HYBRID mode: result + small variation, stable pi

    def measure(self) -> dict
        # Returns {"omega", "pi", "delta", "mode", "history_length"}
```

## `_compute_base()` — deterministic computation

```python
h = sum(ord(c) * (i + 1) for i, c in enumerate(data))
return (h % 1000) / 1000.0
```

## `_compute_variation()` — "vibration" computation

```python
h = sum(ord(c) for c in data)
phase = h / 100.0
variation = np.sin(phase) * omega * factor
```

## Key Implementation Details

- `transition()` updates `self.state` AFTER computing result (uses old state for computation)
- `transition_history` stores last 20 chars of input, balance before/after, delta
- `is_deterministic` and `is_exploratory` are mutually exclusive (equal → neither)
- Uses `safe_divide` and `is_potential` from `src.core.math`
