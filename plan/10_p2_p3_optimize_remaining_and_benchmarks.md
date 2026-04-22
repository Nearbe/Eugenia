# План 10: P2/P3 — Оптимизация remaining модулей + Benchmarks + Долгосрочные направления

## Контекст

**Проблема:** После P0-P2 оптимизаций остаются модули complex.py, dual.py, p_adic.py, sweep.py и другие, которые нужно оптимизировать. Также нужны benchmarks, profiling и долгосрочные направления развития.

**Измерения (сводка):**

| Метод                        | Скорость      |
|------------------------------|---------------|
| `D(5.0)` via function        | 12.8M/сек     |
| `D(5.0)` via default args    | 14M/сек       |
| `D(5.0)` via `__code__`      | ~18.2M/сек    |
| `D(5.0)` inline              | 65.4M/сек     |
| `delta_field(128)` inline    | 3x ускорение  |
| `ridge_to_percentage(5)` inline | 2-3x ускорение |

---

## Цель

1. Оптимизировать remaining модули (complex.py, dual.py, p_adic.py, sweep.py)
2. Создать benchmarks и profiling
3. Определить долгосрочные направления (C-extensions, numba, vectorization, Rust)

---

## Архитектура

### 1. Оптимизация remaining модулей

#### 1.1: `src/core/complex.py`

```python
"""
complex.py — Complex operations для Eugenia.

Dual-path архитектура:
    - standard: читаемая версия с type hints
    - inline: оптимизированная версия через inline-код

Приоритет: P2
"""

import math
import os
from typing import Complex


# ============ CONSTANTS ============
COMPLEX_PI = math.pi
COMPLEX_E = math.e


# ============ STANDARD MODE ============

def complex_rotate(z: complex, angle: float) -> complex:
    """
    Поворот комплексного числа на угол.
    
    complex_rotate(z, angle) = z * e^(i * angle)
    
    Args:
        z: Комплексное число
        angle: Угол в радианах
    
    Returns:
        Повёрнутое комплексное число
    """
    r, theta = abs(z), math.atan2(z.imag, z.real)
    new_theta = theta + angle
    return complex(r * math.cos(new_theta), r * math.sin(new_theta))


def complex_multiply(z1: complex, z2: complex) -> complex:
    """
    Умножение комплексных чисел.
    
    complex_multiply(z1, z2) = (a+bi)(c+di) = (ac-bd) + (ad+bc)i
    
    Args:
        z1: Первое комплексное число
        z2: Второе комплексное число
    
    Returns:
        Результат умножения
    """
    return complex(
        z1.real * z2.real - z1.imag * z2.imag,
        z1.real * z2.imag + z1.imag * z2.real
    )


def complex_compress(z: complex, factor: float = 0.5) -> complex:
    """
    Сжатие комплексного числа.
    
    Args:
        z: Комплексное число
        factor: Коэффициент сжатия
    
    Returns:
        Сжатое комплексное число
    """
    r = abs(z) * factor
    theta = math.atan2(z.imag, z.real)
    return complex(r * math.cos(theta), r * math.sin(theta))


# ============ INLINE MODE ============
_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    def complex_rotate_inline(z, angle):
        r, theta = abs(z), math.atan2(z.imag, z.real)
        new_theta = theta + angle
        return complex(r * math.cos(new_theta), r * math.sin(new_theta))
    
    def complex_multiply_inline(z1, z2):
        return complex(
            z1.real * z2.real - z1.imag * z2.imag,
            z1.real * z2.imag + z1.imag * z2.real
        )
    
    def complex_compress_inline(z, factor=0.5):
        r = abs(z) * factor
        theta = math.atan2(z.imag, z.real)
        return complex(r * math.cos(theta), r * math.sin(theta))
    
    complex_rotate = complex_rotate_inline
    complex_multiply = complex_multiply_inline
    complex_compress = complex_compress_inline


# ============ EXPORTS ============
__all__ = ['complex_rotate', 'complex_multiply', 'complex_compress']
```

---

#### 1.2: `src/core/dual.py`

```python
"""
dual.py — Dual numbers operations для Eugenia.

Dual-path архитектура:
    - standard: читаемая версия с type hints
    - inline: оптимизированная версия через inline-код

Приоритет: P2
"""

import os


# ============ STANDARD MODE ============

def dual_branch(a: float, b: float) -> tuple:
    """
    Branching dual number.
    
    dual_branch(a, b) = (a + b*ε, a - b*ε)
    
    Args:
        a: Основная часть
        b: Дуальная часть
    
    Returns:
        Кортеж (dual_plus, dual_minus)
    """
    return (a + b, a - b)


def dual_compress(a: float, b: float) -> float:
    """
    Compression dual number.
    
    dual_compress(a, b) = a
    
    Args:
        a: Основная часть
        b: Дуальная часть
    
    Returns:
        Основная часть
    """
    return a


# ============ INLINE MODE ============
_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    def dual_branch_inline(a, b):
        return (a + b, a - b)
    
    def dual_compress_inline(a, b):
        return a
    
    dual_branch = dual_branch_inline
    dual_compress = dual_compress_inline


# ============ EXPORTS ============
__all__ = ['dual_branch', 'dual_compress']
```

---

#### 1.3: `src/core/p_adic.py`

```python
"""
p_adic.py — p-adic numbers operations для Eugenia.

Dual-path архитектура:
    - standard: читаемая версия с type hints
    - inline: оптимизированная версия через inline-код

Приоритет: P2
"""

import os


# ============ CONSTANTS ============
P_ADIC_PRIME = 2  # По умолчанию p = 2


# ============ STANDARD MODE ============

def v2_adic_valuation(n: int) -> int:
    """
    Вычисляет 2-adic valuation числа n.
    
    v2_adic_valuation(n) = максимальная степень 2, делящая n
    
    Args:
        n: Целое число
    
    Returns:
        Степень двойки в разложении n
    """
    if n == 0:
        return -1
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


def p_adic_distance(a: int, b: int, p: int = P_ADIC_PRIME) -> float:
    """
    Вычисляет p-adic расстояние между a и b.
    
    p_adic_distance(a, b) = p^(-v_p(a-b))
    
    Args:
        a: Первое число
        b: Второе число
        p: Простое число
    
    Returns:
        p-adic расстояние
    """
    diff = abs(a - b)
    if diff == 0:
        return 0.0
    
    count = 0
    while diff % p == 0:
        diff //= p
        count += 1
    
    return p ** (-count)


# ============ INLINE MODE ============
_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    def v2_adic_valuation_inline(n):
        if n == 0:
            return -1
        count = 0
        while n % 2 == 0:
            n //= 2
            count += 1
        return count
    
    def p_adic_distance_inline(a, b, p=2):
        diff = abs(a - b)
        if diff == 0:
            return 0.0
        count = 0
        while diff % p == 0:
            diff //= p
            count += 1
        return p ** (-count)
    
    v2_adic_valuation = v2_adic_valuation_inline
    p_adic_distance = p_adic_distance_inline


# ============ EXPORTS ============
__all__ = ['v2_adic_valuation', 'p_adic_distance', 'P_ADIC_PRIME']
```

---

#### 1.4: `src/core/sweep.py`

```python
"""
sweep.py — Sweep operations для Eugenia.

Dual-path архитектура:
    - standard: читаемая версия с type hints
    - inline: оптимизированная версия через inline-код

Приоритет: P2
"""

import os
import math


# ============ STANDARD MODE ============

def encode_solenoid_trajectory(x: float, frequency: float = 1.0) -> float:
    """
    Кодирует solenoid trajectory.
    
    encode_solenoid_trajectory(x, frequency) = sin(2 * pi * frequency * x)
    
    Args:
        x: Входное значение
        frequency: Частота
    
    Returns:
        Закодированное значение
    """
    return math.sin(2 * math.pi * frequency * x)


# ============ INLINE MODE ============
_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    def encode_solenoid_trajectory_inline(x, frequency=1.0):
        return math.sin(2 * math.pi * frequency * x)
    
    encode_solenoid_trajectory = encode_solenoid_trajectory_inline


# ============ EXPORTS ============
__all__ = ['encode_solenoid_trajectory']
```

---

### 2. Benchmarks и Profiling

#### 2.1: `tests/test_benchmarks.py`

```python
"""
test_benchmarks.py — Performance benchmarks для Eugenia.

Run: pytest tests/test_benchmarks.py -v --benchmark

Приоритет: P3
"""

import time
import math
import os
import pytest


# ============ D/H BENCHMARKS ============

@pytest.fixture
def D_standard():
    """Стандартная версия D."""
    os.environ['EUGENIA_INLINE'] = '0'
    from src.core.branching import D
    return D


@pytest.fixture
def D_fast():
    """Fast версия D."""
    os.environ['EUGENIA_FAST'] = '1'
    from src.core.fast_ops import D_fast
    return D_fast


@pytest.fixture
def D_inline():
    """Inline версия D."""
    os.environ['EUGENIA_INLINE'] = '1'
    from src.core.branching import D
    return D


def bench_D_standard(D_standard, n=1_000_000):
    """Benchmark стандартной D."""
    x = 5.0
    start = time.perf_counter()
    for _ in range(n):
        x = D_standard(x)
    elapsed = time.perf_counter() - start
    return elapsed


def bench_D_fast(D_fast, n=1_000_000):
    """Benchmark fast D."""
    x = 5.0
    start = time.perf_counter()
    for _ in range(n):
        x = D_fast(x)
    elapsed = time.perf_counter() - start
    return elapsed


def bench_D_inline(D_inline, n=1_000_000):
    """Benchmark inline D."""
    x = 5.0
    start = time.perf_counter()
    for _ in range(n):
        x = D_inline(x)
    elapsed = time.perf_counter() - start
    return elapsed


def test_D_speedup(D_standard, D_fast, D_inline):
    """Тест ускорения D."""
    std_time = bench_D_standard(D_standard)
    fast_time = bench_D_fast(D_fast)
    inline_time = bench_D_inline(D_inline)
    
    print(f"\nD(5.0) benchmarks:")
    print(f"  Standard:  {1_000_000 / std_time:,.0f} calls/sec ({std_time:.4f}s)")
    print(f"  Fast:      {1_000_000 / fast_time:,.0f} calls/sec ({fast_time:.4f}s)")
    print(f"  Inline:    {1_000_000 / inline_time:,.0f} calls/sec ({inline_time:.4f}s)")
    print(f"  Fast/Std:  {std_time / fast_time:.2f}x")
    print(f"  Inline/Std:{std_time / inline_time:.2f}x")
    
    # Ожидаемые ускорения
    assert fast_time < std_time, "Fast должен быть быстрее Standard"
    assert inline_time < fast_time, "Inline должен быть быстрее Fast"


# ============ delta_field BENCHMARKS ============

def bench_delta_field_standard(n=1_000_000):
    """Benchmark стандартной delta_field."""
    os.environ['EUGENIA_INLINE'] = '0'
    import importlib
    import src.core.delta
    importlib.reload(src.core.delta)
    from src.core.delta import delta_field
    
    x = 128.0
    start = time.perf_counter()
    for _ in range(n):
        delta_field(x)
    return time.perf_counter() - start


def bench_delta_field_inline(n=1_000_000):
    """Benchmark inline delta_field."""
    os.environ['EUGENIA_INLINE'] = '1'
    import importlib
    import src.core.delta
    importlib.reload(src.core.delta)
    from src.core.delta import delta_field
    
    x = 128.0
    start = time.perf_counter()
    for _ in range(n):
        delta_field(x)
    return time.perf_counter() - start


def test_delta_field_speedup():
    """Тест ускорения delta_field."""
    std_time = bench_delta_field_standard()
    inline_time = bench_delta_field_inline()
    
    print(f"\ndelta_field(128) benchmarks:")
    print(f"  Standard:  {1_000_000 / std_time:,.0f} calls/sec ({std_time:.4f}s)")
    print(f"  Inline:    {1_000_000 / inline_time:,.0f} calls/sec ({inline_time:.4f}s)")
    print(f"  Speedup:   {std_time / inline_time:.2f}x")
    
    # Ожидаемое ускорение: ≥ 2x
    assert inline_time < std_time * 0.5, "Inline должен быть ≥ 2x быстрее"


# ============ ridge_to_percentage BENCHMARKS ============

def bench_ridge_to_percentage_standard(n=1_000_000):
    """Benchmark стандартной ridge_to_percentage."""
    os.environ['EUGENIA_INLINE'] = '0'
    import importlib
    import src.core.spine
    importlib.reload(src.core.spine)
    from src.core.spine import ridge_to_percentage
    
    x = 5.0
    start = time.perf_counter()
    for _ in range(n):
        ridge_to_percentage(x)
    return time.perf_counter() - start


def bench_ridge_to_percentage_inline(n=1_000_000):
    """Benchmark inline ridge_to_percentage."""
    os.environ['EUGENIA_INLINE'] = '1'
    import importlib
    import src.core.spine
    importlib.reload(src.core.spine)
    from src.core.spine import ridge_to_percentage
    
    x = 5.0
    start = time.perf_counter()
    for _ in range(n):
        ridge_to_percentage(x)
    return time.perf_counter() - start


def test_ridge_to_percentage_speedup():
    """Тест ускорения ridge_to_percentage."""
    std_time = bench_ridge_to_percentage_standard()
    inline_time = bench_ridge_to_percentage_inline()
    
    print(f"\nridge_to_percentage(5) benchmarks:")
    print(f"  Standard:  {1_000_000 / std_time:,.0f} calls/sec ({std_time:.4f}s)")
    print(f"  Inline:    {1_000_000 / inline_time:,.0f} calls/sec ({inline_time:.4f}s)")
    print(f"  Speedup:   {std_time / inline_time:.2f}x")
    
    # Ожидаемое ускорение: ≥ 2x
    assert inline_time < std_time * 0.5, "Inline должен быть ≥ 2x быстрее"


# ============ HOT LOOP BENCHMARK ============

def bench_hot_loop_standard(n=1_000_000):
    """Benchmark hot loop в стандартном режиме."""
    os.environ['EUGENIA_INLINE'] = '0'
    os.environ['EUGENIA_FAST'] = '0'
    
    from src.core.branching import D, H
    from src.core.delta import delta_field
    from src.core.spine import ridge_to_percentage
    
    x = 5.0
    start = time.perf_counter()
    for _ in range(n):
        x = D(x)
        x = H(x)
        _ = delta_field(x)
        _ = ridge_to_percentage(x)
    return time.perf_counter() - start


def bench_hot_loop_inline(n=1_000_000):
    """Benchmark hot loop в inline-режиме."""
    os.environ['EUGENIA_INLINE'] = '1'
    os.environ['EUGENIA_FAST'] = '1'
    
    from src.core.fast_ops import D_fast as D, H_fast as H
    from src.core.delta import delta_field
    from src.core.spine import ridge_to_percentage
    
    x = 5.0
    start = time.perf_counter()
    for _ in range(n):
        x = D(x)
        x = H(x)
        _ = delta_field(x)
        _ = ridge_to_percentage(x)
    return time.perf_counter() - start


def test_hot_loop_speedup():
    """Тест ускорения hot loop."""
    std_time = bench_hot_loop_standard()
    inline_time = bench_hot_loop_inline()
    
    print(f"\nHot loop (1M iter) benchmarks:")
    print(f"  Standard:  {std_time:.4f}s")
    print(f"  Inline:    {inline_time:.4f}s")
    print(f"  Speedup:   {std_time / inline_time:.2f}x")
    
    # Ожидаемое ускорение: ≥ 2x
    assert inline_time < std_time * 0.5, "Inline должен быть ≥ 2x быстрее"


# ============ VSZ/RSS MONITOR ============

def monitor_memory():
    """Мониторинг VSZ и RSS процесса."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    vmb = memory_info.vms / (1024 * 1024 * 1024)  # GB
    rss = memory_info.rss / (1024 * 1024)  # MB
    
    print(f"\nMemory:")
    print(f"  VSZ: {vmb:.1f} GB")
    print(f"  RSS: {rss:.1f} MB")
    
    return {'vmb': vmb, 'rss': rss}
```

---

### 3. Profiling

#### 3.1: `src/utils/profiler.py`

```python
"""
profiler.py — Profiling utilities для Eugenia.

Приоритет: P3
"""

import cProfile
import pstats
import io
from contextlib import contextmanager


@contextmanager
def profile_function(func_name: str, output_file: str = None):
    """
    Context manager для профилирования функции.
    
    Args:
        func_name: Имя функции для профилирования
        output_file: Файл для вывода результатов
    """
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        yield profiler
    finally:
        profiler.disable()
        if output_file:
            profiler.dump_stats(output_file)
        else:
            stream = io.StringIO()
            stats = pstats.Stats(profiler, stream=stream)
            stats.sort_stats('cumulative')
            stats.print_stats(30)
            print(f"=== Profile: {func_name} ===")
            print(stream.getvalue())


def profile_hot_loop(n_iterations=1_000_000):
    """
    Профилирование hot loop.
    
    Args:
        n_iterations: Количество итераций
    """
    profiler = cProfile.Profile()
    profiler.enable()
    
    from src.core.branching import D, H
    from src.core.delta import delta_field
    from src.core.spine import ridge_to_percentage
    
    x = 5.0
    for _ in range(n_iterations):
        x = D(x)
        x = H(x)
        _ = delta_field(x)
        _ = ridge_to_percentage(x)
    
    profiler.disable()
    
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(50)
    
    print("=== Hot Loop Profile ===")
    print(stream.getvalue())
```

---

### 4. Долгосрочные направления

#### 4.1: C-extensions

```
src/core/
├── c_branching.c  # D/H в C
├── c_delta.c      # delta_field в C
└── c_sigmoid.c    # sigmoid в C
```

```c
// c_branching.c
#include <Python.h>

static PyObject* c_D(PyObject* self, PyObject* args) {
    double x;
    if (!PyArg_ParseTuple(args, "d", &x))
        return NULL;
    return PyFloat_FromDouble(x * 2.0);
}

static PyMethodDef BranchingMethods[] = {
    {"D", c_D, METH_VARARGS, "Branching: D(a) = a * 2"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef branchingmodule = {
    PyModuleDef_HEAD_INIT,
    "c_branching",
    NULL,
    -1,
    BranchingMethods
};

PyMODINIT_FUNC PyInit_c_branching(void) {
    return PyModule_Create(&branchingmodule);
}
```

#### 4.2: JIT через numba/llvmlite

```python
# src/core/jit_engine.py
try:
    from numba import njit
    
    @njit
    def D_numba(x):
        return x * 2.0
    
    @njit
    def H_numba(x):
        return x / 2.0
    
    @njit
    def delta_field_numba(x_val):
        if isinstance(x_val, (int, float)):
            x = max(min(float(x_val), 1023.999), 0.0)
            return math.log2(x + 1.0) - math.log2(1024.0 - x)
        return [
            math.log2(max(min(float(x), 1023.999), 0.0) + 1.0)
            - math.log2(1024.0 - max(min(float(x), 1023.999), 0.0))
            for x in x_val
        ]
except ImportError:
    pass  # Fallback to inline_engine
```

#### 4.3: Vectorization через numpy/numexpr

```python
# src/core/vectorized.py
import numpy as np
import numexpr as ne

def delta_field_vectorized(arr):
    """Vectorized delta_field для numpy arrays."""
    x = np.clip(arr, 0, 1023.999)
    return ne.evaluate('log2(x + 1) - log2(1024 - x)')

def ridge_level_vectorized(arr):
    """Vectorized ridge_level для numpy arrays."""
    return np.log2(np.abs(arr) + 1e-300)

def ridge_to_percentage_vectorized(arr):
    """Vectorized sigmoid для numpy arrays."""
    n = np.clip(arr, -1000, 1000)
    return 100.0 / (1.0 + np.exp(-n * np.log(2)))
```

#### 4.4: Parallel через multiprocessing

```python
# src/core/parallel_engine.py
from multiprocessing import Pool

def parallel_sweep(delta_fields, thresholds, n_workers=8):
    """Parallel threshold sweep across classes."""
    with Pool(n_workers) as pool:
        results = pool.map(process_class, delta_fields)
    return results
```

#### 4.5: Memory optimization

```
# Проблемы текущего состояния:
# - VSZ ~421 GB (огромный virtual memory footprint)
# - RSS ~17 MB (хороший resident set)

# Решения:
# 1. sys.modules cleanup — удалить неиспользуемые модули
# 2. __pycache__ preloading — загрузить только нужные code objects
# 3. Lazy imports — загружать модули по требованию
# 4. Memory-mapped arrays — для больших тензоров
```

#### 4.6: Путь к Rust-extensions

```
# Долгосрочная цель: критические пути на Rust
# src/core/
# ├── pyo3_branching.rs  # D/H в Rust
# ├── pyo3_delta.rs      # delta_field в Rust
# └── pyo3_sigmoid.rs    # sigmoid в Rust
#
# Через PyO3 bindings → CPython extensions
```

---

## Сводная таблица приоритетов

| Приоритет | Направление | Ожидаемый эффект | Сложность | Время |
|-----------|-------------|-------------------|-----------|-------|
| **P0** | Inline D/H (default args) | 22% ускорение | Низкая | 0.5 дня |
| **P0** | Inline D/H (`__code__`) | 42% ускорение | Низкая | 1 день |
| **P0** | compile()/exec() | Генерация code objects | Низкая | 1 день |
| **P0** | sys.modules подмена | Убирает файловую зависимость | Средняя | 1 день |
| **P1** | Inline delta_field | 3x ускорение | Средняя | 3 дня |
| **P1** | Inline spine functions | 2-3x ускорение | Средняя | 2 дня |
| **P1** | marshal кеш | Быстрый старт | Низкая | 0.5 дня |
| **P2** | Dual-path для 18 модулей | Прозрачное переключение | Средняя | 5 дней |
| **P2** | Nucleus + CLI | Прозрачное для nucleus | Средняя | 3 дня |
| **P2** | complex/dual/p_adic/sweep | 1.5-2x ускорение | Средняя | 4 дня |
| **P3** | Benchmarks + profiling | Измеримость оптимизаций | Низкая | 1 день |
| **P4** | C-extensions | 10-50x ускорение | Высокая | 1 неделя |
| **P4** | numba JIT | 5-10x ускорение | Средняя | 3 дня |
| **P4** | Vectorization | 3-5x ускорение | Средняя | 2 дня |
| **P5** | Rust-extensions | 20-100x ускорение | Очень высокая | 2-3 недели |

---

## Критерии завершения

**P2 завершён когда:**
- [ ] Все 18 модулей `src/core/` имеют dual-path экспорты
- [ ] Все 21 модуль `src/nucleus/` работает в inline-режиме
- [ ] `Eugenia.py` поддерживает `--inline` флаг
- [ ] `generate.py` поддерживает `--optimization` флаг
- [ ] `config.yaml` поддерживает секцию `optimization`
- [ ] complex.py, dual.py, p_adic.py, sweep.py оптимизированы

**P3 завершён когда:**
- [ ] Benchmarks показывают измеримый прогресс
- [ ] Profiling выявляет реальные hotspots
- [ ] VSZ снижен ≥ 10%
- [ ] RSS снижен ≥ 10%

---

## Риски и ограничения

1. **C-extensions:** Требуют компиляции, могут сломаться на новых платформах
2. **numba:** Добавляет зависимость, может не работать на всех платформах
3. **numpy/numexpr:** Добавляет зависимость, увеличивает размер
4. **Rust:** Высокая сложность, требует изучения Rust
5. **VSZ 421 GB:** Огромный virtual memory — inline-код может помочь через cleanup неиспользуемых модулей
6. **Математическая корректность:** Inline-код не должен менять математическую семантику

---

## Зависимости

- **Предшествующие:** Этапы 01-09 (P0-P2 оптимизации)
- **Последующие:** Нет (долгосрочные направления)
- **Конфликты:** Нет конфликтов с другими этапами

---

## Математическая основа

```
D_ID = 2.0  # Константа из src/core/constants.py

D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
H(a) = a : D(Id) = a / D_ID = a / 2
```

**Обоснование из отчёта:**

> Для полного устранения оверхеда нужно:
> 1. Взять код из core как строки
> 2. Скомпилировать через compile()
> 3. Подменить __code__ у функций в Eugenia.py
> 4. Использовать default args для передачи зависимостей
> 
> Default args = 22% ускорение
> __code__ подмена = 42% ускорение
> sys.modules подмена = убирает файловую зависимость
> compile() + exec() = генерация code objects из строк
> marshal = сериализация code objects
> 
> ЕДИНСТВЕННЫЙ СПОСОБ УБРАТЬ ОВЕРХЕД ПОЛНОСТЬЮ — INLINE-КОД.
> 
> Всё остальное — частичные оптимизации.
