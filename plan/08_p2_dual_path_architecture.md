# План 08: P2 — Dual-path архитектура для всех 18 модулей src/core/

## Контекст

**Проблема:** После P0/P1 оптимизаций (D/H, delta_field, spine) остаются 14 модулей `src/core/`, которые не оптимизированы. Нужно внедрить dual-path архитектуру для всех модулей.

**Двухрежимная архитектура:** Каждый модуль `src/core/*.py` получает два пути экспорта:
- **standard** — читаемая версия с type hints и docstring
- **inline** — оптимизированная версия через inline-код

**Механизм переключения:** Через окружение `EUGENIA_INLINE=1` и конфигурацию `config.yaml`.

---

## Цель

Обновить все 18 модулей `src/core/` для поддержки dual-path экспортов (standard + inline режимы).

---

## Архитектура

### 1. Шаблон рефакторинга каждого модуля

```python
"""
module.py — Module operations для Eugenia.

Dual-path архитектура:
    - standard: читаемая версия с type hints
    - inline: оптимизированная версия через inline-код

Приоритет: P2
"""

import math
import os
from typing import Union, List, Optional


# ============ CONSTANTS ============
# Константы модуля


# ============ STANDARD MODE ============

def standard_func(x):
    """
    Standard (читаемая) версия функции.
    
    Args:
        x: Входное значение
    
    Returns:
        Результат вычисления
    """
    # Читаемая реализация
    pass


# ============ INLINE MODE ============
_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    # Inline-версия (оптимизированная)
    def inline_func(x):
        # Оптимизированная реализация
        pass
    
    # Переопределяем функции
    standard_func = inline_func


# ============ EXPORTS ============
__all__ = ['standard_func']
```

---

### 2. Приоритет рефакторинга модулей

| Приоритет | Модуль | Критичность | Причина |
|-----------|--------|-------------|---------|
| **P0** | `branching.py` | 🔴 Критичный | D/H — самые вызываемые функции |
| **P0** | `constants.py` | 🔴 Критичный | D_ID, OMEGA, PI — константы |
| **P1** | `delta.py` | 🟡 Высокий | delta_field — в каждом рендерере |
| **P1** | `spine.py` | 🟡 Высокий | ridge_level, ridge_to_percentage — sigmoid |
| **P1** | `percent.py` | 🟡 Высокий | to_percentage, from_percentage |
| **P2** | `complex.py` | 🟢 Средний | complex_rotate, complex_multiply |
| **P2** | `dual.py` | 🟢 Средний | dual_branch, dual_compress |
| **P2** | `complex_delta.py` | 🟢 Средний | complex_delta_field |
| **P2** | `p_adic.py` | 🟢 Средний | v2_adic_valuation, p_adic_distance |
| **P2** | `sweep.py` | 🟢 Средний | encode_solenoid_trajectory |
| **P2** | `fractal_dimension.py` | 🟢 Средний | fractal_dimension_from_betti |
| **P2** | `distance.py` | 🟢 Средний | delta_distance, euclidean_distance |
| **P2** | `similarity.py` | 🟢 Средний | similarity (cosine) |
| **P2** | `limits.py` | 🟢 Средний | continuity_D, continuity_H |
| **P2** | `division.py` | 🟢 Средний | safe_divide, div_safe |
| **P2** | `potential.py` | 🟢 Средний | has_potential, is_potential |
| **P2** | `vector.py` | 🟢 Средний | normalize_vector_safe |
| **P2** | `chain.py` | 🟢 Средний | omega_to_pi_chain |
| **P2** | `pyramid.py` | 🟢 Средний | fractal_pyramid_level |

---

### 3. Обновление `src/core/__init__.py`

Добавляем conditional imports:

```python
"""
__init__.py — Package init для core modules.

Dual-path архитектура:
    - standard: читаемые экспорты
    - inline: оптимизированные экспорты

Приоритет: P2
"""

import os

# Режим работы
_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

# ============ STANDARD EXPORTS ============
if not _USE_INLINE:
    from .branching import D, H, D_ID
    from .delta import delta_field, inverse_delta_field
    from .spine import ridge_level, ridge_to_percentage, percentage_to_ridge
    from .percent import to_percentage, from_percentage
    from .complex import complex_rotate, complex_multiply, complex_compress
    from .dual import dual_branch, dual_compress
    from .complex_delta import complex_delta_field
    from .p_adic import v2_adic_valuation, p_adic_distance
    from .sweep import encode_solenoid_trajectory
    from .fractal_dimension import fractal_dimension_from_betti
    from .distance import delta_distance, euclidean_distance
    from .similarity import similarity
    from .limits import continuity_D, continuity_H
    from .division import safe_divide, div_safe
    from .potential import has_potential, is_potential
    from .vector import normalize_vector_safe
    from .chain import omega_to_pi_chain
    from .pyramid import fractal_pyramid_level
    from .constants import D_ID, OMEGA, PI

# ============ INLINE EXPORTS ============
if _USE_INLINE:
    from .fast_ops import D_fast as D, H_fast as H
    from .delta import delta_field, inverse_delta_field
    from .spine import ridge_level, ridge_to_percentage, percentage_to_ridge
    from .percent import to_percentage, from_percentage
    from .complex import complex_rotate, complex_multiply, complex_compress
    from .dual import dual_branch, dual_compress
    from .complex_delta import complex_delta_field
    from .p_adic import v2_adic_valuation, p_adic_distance
    from .sweep import encode_solenoid_trajectory
    from .fractal_dimension import fractal_dimension_from_betti
    from .distance import delta_distance, euclidean_distance
    from .similarity import similarity
    from .limits import continuity_D, continuity_H
    from .division import safe_divide, div_safe
    from .potential import has_potential, is_potential
    from .vector import normalize_vector_safe
    from .chain import omega_to_pi_chain
    from .pyramid import fractal_pyramid_level
    from .constants import D_ID, OMEGA, PI

# ============ EXPORTS ============
__all__ = [
    # Branching
    'D', 'H', 'D_ID',
    # Delta
    'delta_field', 'inverse_delta_field',
    # Spine
    'ridge_level', 'ridge_to_percentage', 'percentage_to_ridge',
    # Percent
    'to_percentage', 'from_percentage',
    # Complex
    'complex_rotate', 'complex_multiply', 'complex_compress',
    # Dual
    'dual_branch', 'dual_compress',
    # Complex Delta
    'complex_delta_field',
    # P-adic
    'v2_adic_valuation', 'p_adic_distance',
    # Sweep
    'encode_solenoid_trajectory',
    # Fractal Dimension
    'fractal_dimension_from_betti',
    # Distance
    'delta_distance', 'euclidean_distance',
    # Similarity
    'similarity',
    # Limits
    'continuity_D', 'continuity_H',
    # Division
    'safe_divide', 'div_safe',
    # Potential
    'has_potential', 'is_potential',
    # Vector
    'normalize_vector_safe',
    # Chain
    'omega_to_pi_chain',
    # Pyramid
    'fractal_pyramid_level',
    # Constants
    'OMEGA', 'PI',
]
```

---

### 4. Обновление `src/core/realmath.py`

Добавляем dual-path экспорты:

```python
"""
realmath.py — Convenience functions для core modules.

Dual-path архитектура:
    - standard: стандартные экспорты
    - inline: оптимизированные экспорты

Приоритет: P2
"""

import os

_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    def inline_mode():
        """Включает inline-режим."""
        return True
    
    def standard_mode():
        """Включает standard-режим."""
        return False
else:
    def inline_mode():
        """Включает inline-режим."""
        return False
    
    def standard_mode():
        """Включает standard-режим."""
        return True


__all__ = ['inline_mode', 'standard_mode']
```

---

## Код-примеры

### Пример 1: Включение inline-режима

```python
import os
os.environ['EUGENIA_INLINE'] = '1'

from src.core import D, H, delta_field, ridge_to_percentage

# Все функции работают в inline-режиме
print(D(5.0))   # 10.0
print(delta_field(128.0))  # delta_field(128)
print(ridge_to_percentage(5.0))  # sigmoid(5.0)
```

### Пример 2: Проверка режима

```python
from src.core.realmath import inline_mode, standard_mode

print(inline_mode())    # True или False
print(standard_mode())  # True или False
```

### Пример 3: Конфигурация через config.yaml

```yaml
# config.yaml
optimization:
  mode: "inline"  # "standard" | "inline"
  inline_functions:
    - "D"
    - "H"
    - "delta_field"
    - "ridge_to_percentage"
  sys_modules_patch: false
  marshal_cache: true
```

---

## Приоритет

**P2** — Средний приоритет. Нужно обновить все 18 модулей.

---

## Критерии завершения

- [ ] Все 18 модулей `src/core/` имеют dual-path экспорты
- [ ] `EUGENIA_INLINE=1` переключает все модули в inline-режим
- [ ] `EUGENIA_INLINE=0` переключает все модули в standard-режим
- [ ] `src/core/__init__.py` корректно экспортирует все функции
- [ ] `src/core/realmath.py` корректно переключает режимы
- [ ] `config.yaml` поддерживает секцию `optimization`
- [ ] Все тесты `tests/test_math.py` проходят
- [ ] Все тесты `tests/test_nucleus_*.py` проходят
- [ ] Математическая корректность: inline-версии дают те же результаты
- [ ] Документация в docstring каждого function

---

## Риски и ограничения

1. **Объём работы:** Нужно обновить 18 модулей
2. **Тестирование:** Нужно тестировать оба режима для каждого модуля
3. **Математическая корректность:** Inline-код не должен менять математическую семантику
4. **Читаемость:** Inline-код менее читаем — нужны подробные docstring
5. **Поддержка двух режимов:** Двойной код увеличивает поддержку

---

## Зависимости

- **Предшествующие:** Этапы 01-07 (P0/P1 оптимизации)
- **Последующие:** Этап 09 (обновление nucleus модулей)
- **Конфликты:** Нет конфликтов с другими этапами

---

## Математическая основа

```
D_ID = 2.0  # Константа из src/core/constants.py

D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
H(a) = a : D(Id) = a / D_ID = a / 2
```

**Обоснование из отчёта:**

> Каждый модуль src/core/*.py получает два пути экспорта:
> - standard: читаемая версия с type hints
> - inline: оптимизированная версия через inline-код
