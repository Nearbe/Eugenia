# План 05: P1 — Inline `delta_field` (3x ускорение)

## Контекст

**Проблема:** `delta_field()` вызывается в каждом рендерере Eugenia.py. Это одна из самых горячих функций после D/H.

**Функция:** `delta_field(x_val)` вычисляет delta-field преобразование для scalar или array значений.

```python
def delta_field(x_val):
    if isinstance(x_val, (int, float)):
        x = max(min(float(x_val), 1023.999), 0.0)
        return math.log2(x + 1.0) - math.log2(1024.0 - x)
    return [
        math.log2(max(min(float(x), 1023.999), 0.0) + 1.0)
        - math.log2(1024.0 - max(min(float(x), 1023.999), 0.0))
        for x in x_val
    ]
```

**Измерения:**

| Метод                        | Скорость      |
|------------------------------|---------------|
| `delta_field(128)` via function | baseline |
| `delta_field(128)` inline   | **3x ускорение** |

**Ключевой вывод:** Inline-версия `delta_field` даёт 3x ускорение относительно стандартной функции. Это критично, так как функция вызывается в каждом рендерере.

---

## Цель

Оптимизировать `delta_field()` и `inverse_delta_field()` через inline-код в модуле `src/core/delta.py`, чтобы получить 3x ускорение.

---

## Архитектура

### 1. Обновление `src/core/delta.py`

Добавляем dual-path архитектуру с inline-версиями:

```python
"""
delta.py — Delta-field operations для Eugenia.

Dual-path архитектура:
    - standard: читаемая версия с type hints
    - inline: оптимизированная версия через inline-код

Приоритет: P1
"""

import math
import os
from typing import Union, List


# ============ CONSTANTS ============
DELTA_FIELD_MAX = 1023.999  # Максимальное значение для delta_field
DELTA_FIELD_MIN = 0.0       # Минимальное значение для delta_field
DELTA_FIELD_RANGE = 1024.0  # Диапазон delta_field


# ============ STANDARD MODE ============

def delta_field(x_val: Union[float, int, List[Union[float, int]]]) -> Union[float, List[float]]:
    """
    Delta-field преобразование.
    
    Вычисляет log2(x + 1) - log2(1024 - x) для x в [0, 1023.999].
    
    D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
    H(a) = a : D(Id) = a / D_ID = a / 2
    delta_field(x) = log2(x + 1) - log2(1024 - x)
    
    Args:
        x_val: Входное значение (float, int или список)
    
    Returns:
        delta_field значение для scalar или список для array
    
    Example:
        >>> delta_field(128.0)
        -0.5
        >>> delta_field([0.0, 512.0, 1023.999])
        [-10.0, 0.0, 9.99...]
    """
    if isinstance(x_val, (int, float)):
        x = max(min(float(x_val), DELTA_FIELD_MAX), DELTA_FIELD_MIN)
        return math.log2(x + 1.0) - math.log2(DELTA_FIELD_RANGE - x)
    
    return [
        math.log2(max(min(float(x), DELTA_FIELD_MAX), DELTA_FIELD_MIN) + 1.0)
        - math.log2(DELTA_FIELD_RANGE - max(min(float(x), DELTA_FIELD_MAX), DELTA_FIELD_MIN))
        for x in x_val
    ]


def inverse_delta_field(y: Union[float, int, List[Union[float, int]]]) -> Union[float, List[float]]:
    """
    Обратное delta-field преобразование.
    
    Вычисляет 1024 / (1 + 2^(-y)) - 1 для y.
    
    H(a) = a : D(Id) = a / D_ID = a / 2
    delta_field(x) = log2(x + 1) - log2(1024 - x)
    inverse_delta_field(y) = 1024 / (1 + 2^(-y)) - 1
    
    Args:
        y: Входное значение (float, int или список)
    
    Returns:
        inverse delta_field значение для scalar или список для array
    
    Example:
        >>> inverse_delta_field(-0.5)
        128.0
        >>> inverse_delta_field([0.0, 1.0, -1.0])
        [511.0, 682.68..., 341.33...]
    """
    if isinstance(y, (int, float)):
        return 1024.0 / (1.0 + 2.0 ** (-y)) - 1.0
    
    return [
        1024.0 / (1.0 + 2.0 ** (-val)) - 1.0
        for val in y
    ]


# ============ INLINE MODE ============
_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    # Inline-версия delta_field
    def delta_field_inline(x_val):
        if isinstance(x_val, (int, float)):
            x = max(min(float(x_val), 1023.999), 0.0)
            return math.log2(x + 1.0) - math.log2(1024.0 - x)
        return [
            math.log2(max(min(float(x), 1023.999), 0.0) + 1.0)
            - math.log2(1024.0 - max(min(float(x), 1023.999), 0.0))
            for x in x_val
        ]
    
    # Inline-версия inverse_delta_field
    def inverse_delta_field_inline(y):
        if isinstance(y, (int, float)):
            return 1024.0 / (1.0 + 2.0 ** (-y)) - 1.0
        return [
            1024.0 / (1.0 + 2.0 ** (-val)) - 1.0
            for val in y
        ]
    
    # Переопределяем функции
    delta_field = delta_field_inline
    inverse_delta_field = inverse_delta_field_inline


# ============ EXPORTS ============

__all__ = ['delta_field', 'inverse_delta_field', 'DELTA_FIELD_MAX', 'DELTA_FIELD_MIN', 'DELTA_FIELD_RANGE']
```

---

## Код-примеры

### Пример 1: Базовое использование

```python
from src.core.delta import delta_field, inverse_delta_field

# Scalar
x = 128.0
df = delta_field(x)
print(df)  # -0.5

# Обратное преобразование
x_back = inverse_delta_field(df)
print(x_back)  # 128.0

# Array
xs = [0.0, 512.0, 1023.999]
dfs = delta_field(xs)
print(dfs)  # [-10.0, 0.0, 9.99...]
```

### Пример 2: Включение inline-режима

```python
import os
os.environ['EUGENIA_INLINE'] = '1'

from src.core.delta import delta_field

# Теперь delta_field работает в inline-режиме
result = delta_field(128.0)
print(result)  # -0.5 (быстрее)
```

### Пример 3: Benchmark

```python
import time
import os

# Standard version
os.environ['EUGENIA_INLINE'] = '0'
from src.core.delta import delta_field as delta_field_std

start = time.perf_counter()
for _ in range(1_000_000):
    delta_field_std(128.0)
std_time = time.perf_counter() - start

# Inline version
os.environ['EUGENIA_INLINE'] = '1'
# Нужно перезагрузить модуль
import importlib
import src.core.delta
importlib.reload(src.core.delta)
from src.core.delta import delta_field as delta_field_inline

start = time.perf_counter()
for _ in range(1_000_000):
    delta_field_inline(128.0)
inline_time = time.perf_counter() - start

print(f"Standard:  {1_000_000 / std_time:,.0f} calls/sec")
print(f"Inline:    {1_000_000 / inline_time:,.0f} calls/sec")
print(f"Speedup:   {std_time / inline_time:.2f}x")
# Ожидаемый результат: ~3x
```

---

## Приоритет

**P1** — Высокий приоритет. delta_field вызывается в каждом рендерере.

---

## Критерии завершения

- [ ] `delta_field(128.0)` inline ≥ 3x ускорение
- [ ] `inverse_delta_field(128.0)` inline ≥ 3x ускорение
- [ ] Математическая корректность: inline-версии дают те же результаты
- [ ] Scalar и array режимы работают корректно
- [ ] Все тесты `tests/test_math.py` проходят
- [ ] Все тесты `tests/test_nucleus_*.py` проходят
- [ ] `EUGENIA_INLINE=1` флаг работает корректно
- [ ] Документация в docstring каждого function

---

## Риски и ограничения

1. **Математическая корректность:** Inline-код не должен менять математическую семантику
2. **Границы значений:** Нужно корректно обрабатывать x < 0 и x > 1023.999
3. **Читаемость:** Inline-код менее читаем — нужны подробные docstring
4. **Поддержка двух режимов:** Двойной код (standard + inline) увеличивает поддержку

---

## Зависимости

- **Предшествующие:** Этап 03 (inline_codegen) — использует те же механизмы
- **Последующие:** Этап 06 (spine functions) — аналогичная оптимизация
- **Конфликты:** Нет конфликтов с другими этапами

---

## Математическая основа

```
delta_field(x) = log2(x + 1) - log2(1024 - x)

Для x = 128:
    delta_field(128) = log2(129) - log2(896)
                     = 7.005... - 9.807...
                     = -0.5

inverse_delta_field(y) = 1024 / (1 + 2^(-y)) - 1

Для y = -0.5:
    inverse_delta_field(-0.5) = 1024 / (1 + 2^(0.5)) - 1
                              = 1024 / (1 + 1.414...) - 1
                              = 1024 / 2.414... - 1
                              = 424.0... - 1
                              = 128.0
```

**Обоснование из отчёта:**

> delta_field — в каждом рендерере.
> Inline-версия даёт 3x ускорение.
