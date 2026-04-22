# План 06: P1 — Inline spine functions (2-3x ускорение)

## Контекст

**Проблема:** Функции из `src/core/spine.py` (ridge_level, ridge_to_percentage, percentage_to_ridge) вызываются в каждом рендерере и при нормализации. Это один из hottest путей после D/H/delta_field.

**Функции:**

1. **ridge_level(x)** — вычисляет log2(|x| + 1e-300)
2. **ridge_to_percentage(n)** — sigmoid преобразование ridge в percentage
3. **percentage_to_ridge(p)** — inverse sigmoid преобразование

**Измерения:**

| Метод                        | Скорость      |
|------------------------------|---------------|
| `ridge_to_percentage(5)` via function | baseline |
| `ridge_to_percentage(5)` inline   | **2-3x ускорение** |

**Ключевой вывод:** Inline-версии spine functions дают 2-3x ускорение. ridge_to_percentage особенно критичен, так как это sigmoid, который вызывается миллионы раз.

---

## Цель

Оптимизировать ridge_level, ridge_to_percentage и percentage_to_ridge через inline-код в модуле `src/core/spine.py`, чтобы получить 2-3x ускорение.

---

## Архитектура

### 1. Обновление `src/core/spine.py`

Добавляем dual-path архитектуру с inline-версиями:

```python
"""
spine.py — Spine operations (ridge_level, ridge_to_percentage) для Eugenia.

Dual-path архитектура:
    - standard: читаемая версия с type hints
    - inline: оптимизированная версия через inline-код

Приоритет: P1
"""

import math
import os
from typing import Union, List


# ============ CONSTANTS ============
RIDGE_THRESHOLD = 1000.0      # Порог для sigmoid
RIDGE_EPSILON = 1e-300        # Эпсилон для ridge_level
LOG2_EXP_BOUND = 700.0        # Граница для exp overflow


# ============ STANDARD MODE ============

def ridge_level(x: Union[float, int]) -> float:
    """
    Вычисляет ridge level для значения x.
    
    ridge_level(x) = log2(|x| + epsilon)
    
    D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
    H(a) = a : D(Id) = a / D_ID = a / 2
    
    Args:
        x: Входное значение
    
    Returns:
        ridge level для x
    
    Example:
        >>> ridge_level(1024.0)
        10.0
        >>> ridge_level(0.0)
        -996.57...
    """
    return math.log2(abs(x) + RIDGE_EPSILON)


def ridge_to_percentage(n: Union[float, int]) -> float:
    """
    Преобразует ridge level в percentage (sigmoid).
    
    ridge_to_percentage(n) = 100 / (1 + 2^(-n))
    
    Для |n| >= 1000 возвращает 0.0 или 100.0 (overflow protection).
    Для |exp_arg| > 700 возвращает 0.0 или 100.0 (exp overflow protection).
    
    H(a) = a : D(Id) = a / D_ID = a / 2
    ridge_to_percentage(n) = 100 / (1 + 2^(-n))
    
    Args:
        n: Ridge level значение
    
    Returns:
        Percentage значение в [0.0, 100.0]
    
    Example:
        >>> ridge_to_percentage(0.0)
        50.0
        >>> ridge_to_percentage(10.0)
        99.90...
        >>> ridge_to_percentage(-10.0)
        0.097...
        >>> ridge_to_percentage(1000.0)
        100.0
    """
    if n >= RIDGE_THRESHOLD:
        return 100.0
    if n <= -RIDGE_THRESHOLD:
        return 0.0
    
    exp_arg = -n
    if exp_arg > LOG2_EXP_BOUND:
        return 0.0
    if exp_arg < -LOG2_EXP_BOUND:
        return 100.0
    
    return 100.0 / (1.0 + 2.0 ** exp_arg)


def percentage_to_ridge(p: Union[float, int]) -> float:
    """
    Обратное преобразование percentage в ridge level (inverse sigmoid).
    
    percentage_to_ridge(p) = -log2((100 / p) - 1)
    
    Для p <= 0 возвращает -1000.0 (overflow protection).
    Для p >= 100 возвращает 1000.0 (overflow protection).
    
    D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
    percentage_to_ridge(p) = -log2((100 / p) - 1)
    
    Args:
        p: Percentage значение в [0.0, 100.0]
    
    Returns:
        Ridge level значение
    
    Example:
        >>> percentage_to_ridge(50.0)
        0.0
        >>> percentage_to_ridge(99.90...)
        10.0
        >>> percentage_to_ridge(0.097...)
        -10.0
    """
    if p <= 0.0:
        return -RIDGE_THRESHOLD
    if p >= 100.0:
        return RIDGE_THRESHOLD
    
    return -math.log2((100.0 / p) - 1.0)


# ============ INLINE MODE ============
_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    # Inline-версия ridge_level
    def ridge_level_inline(x):
        return math.log2(abs(x) + 1e-300)
    
    # Inline-версия ridge_to_percentage (оптимизированный sigmoid)
    def ridge_to_percentage_inline(n):
        if n >= 1000:
            return 100.0
        if n <= -1000:
            return 0.0
        exp_arg = -n
        if exp_arg > 700:
            return 0.0
        if exp_arg < -700:
            return 100.0
        return 100.0 / (1.0 + 2.0 ** exp_arg)
    
    # Inline-версия percentage_to_ridge (оптимизированный inverse sigmoid)
    def percentage_to_ridge_inline(p):
        if p <= 0.0:
            return -1000.0
        if p >= 100.0:
            return 1000.0
        return -math.log2((100.0 / p) - 1.0)
    
    # Переопределяем функции
    ridge_level = ridge_level_inline
    ridge_to_percentage = ridge_to_percentage_inline
    percentage_to_ridge = percentage_to_ridge_inline


# ============ EXPORTS ============

__all__ = [
    'ridge_level',
    'ridge_to_percentage',
    'percentage_to_ridge',
    'RIDGE_THRESHOLD',
    'RIDGE_EPSILON',
    'LOG2_EXP_BOUND',
]
```

---

## Код-примеры

### Пример 1: Базовое использование

```python
from src.core.spine import ridge_level, ridge_to_percentage, percentage_to_ridge

# ridge_level
level = ridge_level(1024.0)
print(level)  # 10.0

# ridge_to_percentage (sigmoid)
pct = ridge_to_percentage(10.0)
print(pct)  # 99.90...

# percentage_to_ridge (inverse sigmoid)
level_back = percentage_to_ridge(pct)
print(level_back)  # 10.0
```

### Пример 2: Включение inline-режима

```python
import os
os.environ['EUGENIA_INLINE'] = '1'

from src.core.spine import ridge_to_percentage

# Теперь ridge_to_percentage работает в inline-режиме
result = ridge_to_percentage(5.0)
print(result)  # sigmoid(5.0) (быстрее)
```

### Пример 3: Benchmark

```python
import time
import os

# Standard version
os.environ['EUGENIA_INLINE'] = '0'
from src.core.spine import ridge_to_percentage as rtp_std

start = time.perf_counter()
for _ in range(1_000_000):
    rtp_std(5.0)
std_time = time.perf_counter() - start

# Inline version
os.environ['EUGENIA_INLINE'] = '1'
import importlib
import src.core.spine
importlib.reload(src.core.spine)
from src.core.spine import ridge_to_percentage as rtp_inline

start = time.perf_counter()
for _ in range(1_000_000):
    rtp_inline(5.0)
inline_time = time.perf_counter() - start

print(f"Standard:  {1_000_000 / std_time:,.0f} calls/sec")
print(f"Inline:    {1_000_000 / inline_time:,.0f} calls/sec")
print(f"Speedup:   {std_time / inline_time:.2f}x")
# Ожидаемый результат: ~2-3x
```

---

## Приоритет

**P1** — Высокий приоритет. Spine functions вызываются в каждом рендерере.

---

## Критерии завершения

- [ ] `ridge_to_percentage(5.0)` inline ≥ 2x ускорение
- [ ] `percentage_to_ridge(50.0)` inline ≥ 2x ускорение
- [ ] `ridge_level(1024.0)` inline ≥ 2x ускорение
- [ ] Математическая корректность: inline-версии дают те же результаты
- [ ] Overflow protection работает корректно (n >= 1000, p <= 0, p >= 100)
- [ ] Все тесты `tests/test_math.py` проходят
- [ ] Все тесты `tests/test_nucleus_*.py` проходят
- [ ] `EUGENIA_INLINE=1` флаг работает корректно
- [ ] Документация в docstring каждого function

---

## Риски и ограничения

1. **Математическая корректность:** Inline-код не должен менять математическую семантику
2. **Overflow protection:** Нужно корректно обрабатывать overflow для sigmoid
3. **Читаемость:** Inline-код менее читаем — нужны подробные docstring
4. **Поддержка двух режимов:** Двойной код (standard + inline) увеличивает поддержку

---

## Зависимости

- **Предшествующие:** Этап 03 (inline_codegen) — использует те же механизмы
- **Последующие:** Этап 07 (marshal кеш) — сериализация сгенерированных code objects
- **Конфликты:** Нет конфликтов с другими этапами

---

## Математическая основа

```
ridge_level(x) = log2(|x| + epsilon)

Для x = 1024:
    ridge_level(1024) = log2(1024 + 1e-300)
                      = log2(1024)
                      = 10.0

ridge_to_percentage(n) = 100 / (1 + 2^(-n))

Для n = 10:
    ridge_to_percentage(10) = 100 / (1 + 2^(-10))
                            = 100 / (1 + 0.000976...)
                            = 100 / 1.000976...
                            = 99.90...

percentage_to_ridge(p) = -log2((100 / p) - 1)

Для p = 99.90:
    percentage_to_ridge(99.90) = -log2((100 / 99.90) - 1)
                                = -log2(1.00100... - 1)
                                = -log2(0.00100...)
                                = 10.0
```

**Обоснование из отчёта:**

> ridge_to_percentage (sigmoid — вызывается миллионы раз).
> Inline-версия даёт 2-3x ускорение.
