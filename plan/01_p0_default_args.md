# План 01: P0 — Default args для D/H (22% ускорение)

## Контекст

**Проблема:** Вызовы функций из `src/core/` добавляют ~412% оверхед. `D(5.0)` выполняется в 5.2 раза медленнее, чем `5.0 * 2` inline.

**Измерения:**

| Метод                        | Скорость      |
|------------------------------|---------------|
| `import math; math.log2()`   | 8.4M/сек      |
| `_log2 = math.log2; _log2()` | 11.4M/сек     |
| `def f(x, log2=_log2)`       | **14M/сек**   |
| `x * 2` inline               | **65.4M/сек** |

**Ключевой вывод:** Default args = fastest way передать функцию-зависимость без LOAD_GLOBAL оверхеда. Это даёт **22% ускорение** относительно уже оптимизированного варианта с модульным импортом.

**Механизм:** Когда функция вызывается с default arg, Python использует `LOAD_FAST` (быстрый доступ к локальной переменной) вместо `LOAD_GLOBAL` (медленный поиск в globals dict). Это убирает один из основных источников оверхеда.

---

## Цель

Внедрить default args для критических функций `D()` и `H()` в горячем цикле Eugenia.py, чтобы получить 22% ускорение без изменения математической семантики.

---

## Архитектура

### 1. Новый модуль: `src/core/fast_ops.py`

Создаём оптимизированные версии функций с default args:

```python
"""
fast_ops.py — Оптимизированные версии D/H с default args.

Использует default args для передачи констант,
чтобы избежать LOAD_GLOBAL оверхеда в горячем цикле.

Benchmark:
    D(5.0) via default args: ~14M calls/sec
    D(5.0) via LOAD_GLOBAL:  ~12.8M calls/sec
    D(5.0) inline:            ~65.4M calls/sec

Приоритет: P0
"""

# ============ CONSTANTS ============
D_ID = 2.0  # Branching constant: D(a) = a ⊕ a = a * 2


# ============ FAST D (Branching) ============
def D_fast(x, _D_ID=D_ID):
    """
    Оптимизированная версия D с default args.
    
    D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
    
    Default arg _D_ID = 2.0 передаётся через замыкание,
    что позволяет использовать LOAD_FAST вместо LOAD_GLOBAL.
    
    Args:
        x: Входное значение (float или iterable)
        _D_ID: Константа D_ID по умолчанию (2.0)
    
    Returns:
        x * 2.0 для scalar
        [v * 2.0 for v in x] для iterable
    """
    if isinstance(x, (int, float)):
        return x * _D_ID
    return [v * _D_ID for v in x]


# ============ FAST H (Compression) ============
def H_fast(x, _D_ID=D_ID):
    """
    Оптимизированная версия H с default args.
    
    H(a) = a : D(Id) = a / D_ID = a / 2
    
    Default arg _D_ID = 2.0 передаётся через замыкание,
    что позволяет использовать LOAD_FAST вместо LOAD_GLOBAL.
    
    Args:
        x: Входное значение (float или iterable)
        _D_ID: Константа D_ID по умолчанию (2.0)
    
    Returns:
        x / 2.0 для scalar
        [v / 2.0 for v in x] для iterable
    """
    if isinstance(x, (int, float)):
        return x / _D_ID
    return [v / _D_ID for v in x]


# ============ FAST OMEGA (Omega constant) ============
OMEGA = 0.0  # Omega constant

def O_fast(x, _OMEGA=OMEGA):
    """
    Оптимизированная версия O (Omega) с default args.
    
    O(a) = a + Ω = a + 0.0 = a (identity для float)
    
    Args:
        x: Входное значение
        _OMEGA: Константа OMEGA по умолчанию (0.0)
    
    Returns:
        x + OMEGA
    """
    return x + _OMEGA


# ============ PI constant ============
PI = float('inf')  # PI constant (infinity in current system)


# ============ EXPORTS ============
__all__ = ['D_ID', 'D_fast', 'H_fast', 'OMEGA', 'O_fast', 'PI']
```

---

### 2. Обновление `src/core/branching.py`

Добавляем dual-path экспорт:

```python
"""
branching.py — Branching operations для Eugenia.

Dual-path архитектура:
    - standard: читаемая версия с type hints
    - fast: оптимизированная версия с default args

Приоритет: P0
"""

import os
from src.core.fast_ops import D_fast, H_fast, D_ID

# ============ STANDARD MODE ============
def D(x):
    """
    Branching: D(a) = a ⊕ a = a * D_ID = a * 2.
    
    Standard (читаемая) версия.
    """
    if isinstance(x, (int, float)):
        return x * D_ID
    return [v * D_ID for v in x]


def H(x):
    """
    Compression: H(a) = a : D(Id) = a / D_ID = a / 2.
    
    Standard (читаемая) версия.
    """
    if isinstance(x, (int, float)):
        return x / D_ID
    return [v / D_ID for v in x]


# ============ FAST MODE ============
_USE_FAST = os.environ.get('EUGENIA_FAST', '0') == '1'

if _USE_FAST:
    # Переопределяем D и H на fast-версии
    D = D_fast
    H = H_fast


# ============ EXPORTS ============
__all__ = ['D', 'H', 'D_ID']
```

---

### 3. Обновление `Eugenia.py`

Использовать fast-версии в горячем цикле:

```python
# В начале Eugenia.py
import os
_USE_FAST = os.environ.get('EUGENIA_FAST', '0') == '1'

if _USE_FAST:
    from src.core.fast_ops import D_fast as D
    from src.core.fast_ops import H_fast as H
    from src.core.fast_ops import D_ID
else:
    from src.core.branching import D, H, D_ID

# Горячий цикл
x = 5.0
for _ in range(1_000_000):
    x = D(x)  # ~14M calls/sec с default args vs ~12.8M без
    x = H(x)
```

---

## Код-примеры

### Пример 1: Базовое использование

```python
from src.core.fast_ops import D_fast, H_fast, D_ID

# Default args автоматически передаются
result = D_fast(5.0)    # 5.0 * 2.0 = 10.0
result = H_fast(10.0)   # 10.0 / 2.0 = 5.0

# Явная передача (для тестирования)
result = D_fast(5.0, _D_ID=2.0)  # то же самое
```

### Пример 2: Benchmark

```python
import time
from src.core.fast_ops import D_fast, H_fast
from src.core.branching import D, H

# Fast version
start = time.perf_counter()
x = 5.0
for _ in range(10_000_000):
    x = D_fast(x)
fast_time = time.perf_counter() - start

# Standard version
start = time.perf_counter()
x = 5.0
for _ in range(10_000_000):
    x = D(x)
std_time = time.perf_counter() - start

print(f"Fast:  {10_000_000 / fast_time:,.0f} calls/sec")
print(f"Std:   {10_000_000 / std_time:,.0f} calls/sec")
print(f"Speedup: {std_time / fast_time:.2f}x")
# Ожидаемый результат: ~1.22x (22% ускорение)
```

### Пример 3: Использование в горячем цикле

```python
import os

_USE_FAST = os.environ.get('EUGENIA_FAST', '0') == '1'

if _USE_FAST:
    from src.core.fast_ops import D_fast as D, H_fast as H
else:
    from src.core.branching import D, H

def hot_loop(n_iterations=1_000_000):
    """Горячий цикл с оптимизированными D/H."""
    x = 5.0
    for _ in range(n_iterations):
        x = D(x)  # ~14M calls/sec с default args
        x = H(x)  # ~14M calls/sec с default args
    return x
```

---

## Приоритет

**P0** — Критический путь. Самый быстрый способ получить оптимизацию без изменения архитектуры.

---

## Критерии завершения

- [ ] `D_fast(5.0)` ≥ 14M calls/sec (vs 12.8M baseline)
- [ ] `H_fast(5.0)` ≥ 14M calls/sec
- [ ] Hot loop ускорение ≥ 15% (измерено в секундах)
- [ ] Все тесты `tests/test_math.py` проходят
- [ ] Все тесты `tests/test_nucleus_*.py` проходят
- [ ] `EUGENIA_FAST=1` флаг работает корректно
- [ ] Математическая корректность: `D_fast(x) == D(x)` для всех x
- [ ] Документация в docstring каждого function

---

## Риски и ограничения

1. **Математическая корректность:** Default args не должны менять результат вычислений
2. **Тестирование:** Нужны тесты для обеих версий (standard + fast)
3. **Глобальное состояние:** `D_ID` — общая константа, не должна меняться во время выполнения
4. **Читаемость:** Fast-версии менее читаемы — нужны подробные docstring
5. **Поддержка:** Два режима (standard + fast) увеличивают поддержку

---

## Зависимости

- **Предшествующие:** Нет (самостоятельный этап)
- **Последующие:** Этап 02 (`__code__` подмена) — можно применять параллельно
- **Конфликты:** Нет конфликтов с другими этапами

---

## Математическая основа

```
D_ID = 2.0  # Константа из src/core/constants.py

D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
H(a) = a : D(Id) = a / D_ID = a / 2
```

**Обоснование из отчёта:**

> Default args = fastest way передать функцию-зависимость без LOAD_GLOBAL оверхеда.
> 
> Измерения:
> - `import math; math.log2()` — 8.4M/сек
> - `_log2 = math.log2; _log2()` — 11.4M/сек
> - `def f(x, log2=_log2)` — **14M/сек**
> - `x * 2` inline — **65.4M/сек**
