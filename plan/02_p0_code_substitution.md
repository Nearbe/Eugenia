# План 02: P0 — `__code__` подмена (42% ускорение)

## Контекст

**Проблема:** Вызовы функций из `src/core/` добавляют ~412% оверхед. `D(5.0)` выполняется в 5.2 раза медленнее, чем `5.0 * 2` inline.

**Измерения:**

| Метод                        | Скорость      |
|------------------------------|---------------|
| `import math; math.log2()`   | 8.4M/сек      |
| `_log2 = math.log2; _log2()` | 11.4M/сек     |
| `def f(x, log2=_log2)`       | 14M/сек       |
| `D(5.0)` via function        | **12.8M/сек** |
| `5.0 * 2` inline             | **65.4M/сек** |
| `__code__` подмена           | **~18.2M/сек** (1.42x ускорение) |

**Ключевой вывод:** Подмена `__code__` у существующих функций на inline-версию даёт **1.42x ускорение** — это лучший результат среди методов, которые не требуют полной inline-подстановки кода.

**Механизм:** Python позволяет менять `__code__` у функции на лету. Это означает, что мы можем взять готовую функцию, подменить её байткод на оптимизированный inline-код, и все вызовы этой функции автоматически начнут использовать оптимизированный путь.

---

## Цель

Внедрить механизм подмены `__code__` для критических функций `D()`, `H()`, `delta_field()` и `ridge_to_percentage()` в Eugenia.py, чтобы получить 42% ускорение без изменения математической семантики.

---

## Архитектура

### 1. Новый модуль: `src/core/code_substitution.py`

Создаём ядро для подмены `__code__`:

```python
"""
code_substitution.py — Подмена __code__ для inline-оптимизации.

Механизм подмены __code__ у существующих функций на inline-версию.
Даёт 1.42x ускорение относительно стандартных function calls.

Benchmark:
    D(5.0) via __code__ подмена: ~18.2M calls/sec
    D(5.0) via default args:     ~14.0M calls/sec
    D(5.0) inline:                ~65.4M calls/sec

Приоритет: P0
"""

import types
import sys
from typing import Callable, Dict, Optional, Tuple


# ============ INLINE CODE TEMPLATES ============
# Предварительно скомпилированные inline-версии функций.
# Каждая строка — это полный код функции, который компилируется
# и из которого извлекается code object.

INLINE_CODE_TEMPLATES: Dict[str, str] = {
    'D': """
def D_inline(x):
    return x * 2.0
""",
    'H': """
def H_inline(x):
    return x / 2.0
""",
    'delta_field': """
def delta_field_inline(x_val):
    import math
    if isinstance(x_val, (int, float)):
        x = max(min(float(x_val), 1023.999), 0.0)
        return math.log2(x + 1.0) - math.log2(1024.0 - x)
    return [
        math.log2(max(min(float(x), 1023.999), 0.0) + 1.0)
        - math.log2(1024.0 - max(min(float(x), 1023.999), 0.0))
        for x in x_val
    ]
""",
    'ridge_to_percentage': """
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
""",
}


# ============ CODE OBJECT CACHE ============
# Кэш для уже скомпилированных code objects.
# Позволяет избежать повторной компиляции при каждом вызове.

_code_cache: Dict[str, types.CodeType] = {}


def _compile_inline_code(name: str) -> types.CodeType:
    """
    Компилирует inline-шаблон в code object и кэширует его.
    
    Args:
        name: Имя функции из INLINE_CODE_TEMPLATES.
        
    Returns:
        types.CodeType — скомпилированный code object.
        
    Raises:
        KeyError: Если name не найден в INLINE_CODE_TEMPLATES.
        ValueError: Если code object не найден в константах.
    """
    if name in _code_cache:
        return _code_cache[name]
    
    if name not in INLINE_CODE_TEMPLATES:
        raise KeyError(f"Unknown inline code template: {name}")
    
    code_str = INLINE_CODE_TEMPLATES[name]
    compiled = compile(code_str, f'<inline_{name}>', 'exec')
    
    # Извлекаем code object из констант
    for const in compiled.co_consts:
        if isinstance(const, types.CodeType):
            _code_cache[name] = const
            return const
    
    raise ValueError(f"No code object found for template: {name}")


# ============ SUBSTITUTION FUNCTIONS ============

def substitute_code(func: Callable, code_obj: types.CodeType) -> bool:
    """
    Подменяет __code__ у функции на переданный code object.
    
    Это основная функция подмены. После вызова все вызовы func()
    будут использовать новый code object.
    
    Args:
        func: Функция, у которой нужно подменить __code__.
        code_obj: Новый code object для подмены.
        
    Returns:
        True если подмена успешна, False если возникла ошибка.
        
    Example:
        >>> from src.core.branching import D
        >>> new_code = _compile_inline_code('D')
        >>> substitute_code(D, new_code)
        True
        >>> D(5.0)  # теперь использует inline-версию
        10.0
    """
    try:
        # Сохраняем оригинальный __code__ для rollback
        if not hasattr(func, '_original_code'):
            func._original_code = func.__code__
        
        func.__code__ = code_obj
        return True
    except (AttributeError, TypeError) as e:
        print(f"Warning: Failed to substitute __code__ for {func.__name__}: {e}")
        return False


def restore_code(func: Callable) -> bool:
    """
    Восстанавливает оригинальный __code__ у функции.
    
    Args:
        func: Функция, у которой нужно восстановить __code__.
        
    Returns:
        True если восстановление успешно, False если ошибка.
    """
    try:
        if hasattr(func, '_original_code'):
            func.__code__ = func._original_code
            return True
        return False
    except (AttributeError, TypeError) as e:
        print(f"Warning: Failed to restore __code__ for {func.__name__}: {e}")
        return False


def apply_inline(name: str, target_func: Callable) -> bool:
    """
    Применяет inline-версию к функции.
    
    Args:
        name: Имя шаблона из INLINE_CODE_TEMPLATES.
        target_func: Функция для подмены.
        
    Returns:
        True если подмена успешна, False если ошибка.
    """
    code_obj = _compile_inline_code(name)
    return substitute_code(target_func, code_obj)


def restore_inline(target_func: Callable) -> bool:
    """
    Восстанавливает оригинальную версию функции.
    
    Args:
        target_func: Функция для восстановления.
        
    Returns:
        True если восстановление успешно, False если ошибка.
    """
    return restore_code(target_func)


# ============ BATCH OPERATIONS ============

def apply_all_inline(funcs: Dict[str, Callable]) -> Dict[str, bool]:
    """
    Применяет inline-версии ко всем переданным функциям.
    
    Args:
        funcs: Словарь {name: func} для подмены.
        
    Returns:
        Словарь {name: success} результатов подмены.
        
    Example:
        >>> from src.core.branching import D, H
        >>> results = apply_all_inline({'D': D, 'H': H})
        {'D': True, 'H': True}
    """
    results = {}
    for name, func in funcs.items():
        results[name] = apply_inline(name, func)
    return results


def restore_all_inline(funcs: Dict[str, Callable]) -> Dict[str, bool]:
    """
    Восстанавливает оригинальные версии всех переданных функций.
    
    Args:
        funcs: Словарь {name: func} для восстановления.
        
    Returns:
        Словарь {name: success} результатов восстановления.
    """
    results = {}
    for name, func in funcs.items():
        results[name] = restore_inline(func)
    return results


# ============ CONTEXT MANAGER ============

from contextlib import contextmanager

@contextmanager
def inline_mode(funcs: Dict[str, Callable]):
    """
    Context manager для временного включения inline-режима.
    
    Args:
        funcs: Словарь {name: func} для inline-подмены.
        
    Example:
        >>> from src.core.branching import D, H
        >>> with inline_mode({'D': D, 'H': H}):
        ...     # Здесь D и H работают в inline-режиме
        ...     result = D(5.0) + H(10.0)
        >>> # Здесь D и H восстановлены в оригинальные версии
    """
    originals = {}
    for name, func in funcs.items():
        originals[name] = func.__code__
        apply_inline(name, func)
    
    try:
        yield
    finally:
        for name, func in funcs.items():
            func.__code__ = originals[name]


# ============ EXPORTS ============

__all__ = [
    'INLINE_CODE_TEMPLATES',
    '_compile_inline_code',
    'substitute_code',
    'restore_code',
    'apply_inline',
    'restore_inline',
    'apply_all_inline',
    'restore_all_inline',
    'inline_mode',
]
```

---

### 2. Обновление `src/core/branching.py`

Добавляем поддержку `__code__` подмены:

```python
"""
branching.py — Branching operations для Eugenia.

Dual-path архитектура:
    - standard: читаемая версия с type hints
    - inline: оптимизированная версия через __code__ подмену

Приоритет: P0
"""

import os
from src.core.code_substitution import apply_inline, restore_inline

# ============ STANDARD MODE ============
D_ID = 2.0  # Branching constant

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


# ============ INLINE MODE ============
_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    # Применяем inline-версии
    apply_inline('D', D)
    apply_inline('H', H)


# ============ EXPORTS ============
__all__ = ['D', 'H', 'D_ID']
```

---

### 3. Обновление `Eugenia.py`

Включаем inline-режим при старте:

```python
# В начале Eugenia.py
import os

# Включаем inline-режим через окружение
# EUGENIA_INLINE=1 python Eugenia.py
_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    # Подменяем __code__ у всех критических функций
    from src.core.code_substitution import apply_all_inline
    from src.core.branching import D, H
    from src.core.delta import delta_field
    from src.core.spine import ridge_to_percentage
    
    apply_all_inline({
        'D': D,
        'H': H,
        'delta_field': delta_field,
        'ridge_to_percentage': ridge_to_percentage,
    })
    print("[Eugenia] Inline mode ENABLED (1.42x speedup)")
else:
    from src.core.branching import D, H
    from src.core.delta import delta_field
    from src.core.spine import ridge_to_percentage
    print("[Eugenia] Inline mode DISABLED (standard mode)")

# Горячий цикл
x = 5.0
for _ in range(1_000_000):
    x = D(x)  # ~18.2M calls/sec с __code__ подменой
    x = H(x)
```

---

## Код-примеры

### Пример 1: Базовая подмена

```python
from src.core.code_substitution import apply_inline, restore_inline
from src.core.branching import D

# Оригинальная версия
print(D(5.0))  # 10.0

# Подменяем на inline-версию
apply_inline('D', D)
print(D(5.0))  # 10.0 (тот же результат, но быстрее)

# Восстанавливаем
restore_inline(D)
```

### Пример 2: Batch подмена

```python
from src.core.code_substitution import apply_all_inline, restore_all_inline
from src.core.branching import D, H
from src.core.delta import delta_field

# Применяем ко всем функциям сразу
funcs = {
    'D': D,
    'H': H,
    'delta_field': delta_field,
}

results = apply_all_inline(funcs)
print(results)  # {'D': True, 'H': True, 'delta_field': True}
```

### Пример 3: Context manager

```python
from src.core.code_substitution import inline_mode
from src.core.branching import D, H

# Только в этом блоке D и H работают в inline-режиме
with inline_mode({'D': D, 'H': H}):
    # Здесь D и H работают в inline-режиме
    result = D(5.0) + H(10.0)

# Здесь D и H восстановлены в оригинальные версии
```

### Пример 4: Benchmark

```python
import time
from src.core.code_substitution import apply_inline, restore_inline
from src.core.branching import D

# Standard version
start = time.perf_counter()
x = 5.0
for _ in range(10_000_000):
    x = D(x)
std_time = time.perf_counter() - start

# Inline version
apply_inline('D', D)
start = time.perf_counter()
x = 5.0
for _ in range(10_000_000):
    x = D(x)
inline_time = time.perf_counter() - start

# Restore
restore_inline(D)

print(f"Standard:  {10_000_000 / std_time:,.0f} calls/sec")
print(f"Inline:    {10_000_000 / inline_time:,.0f} calls/sec")
print(f"Speedup:   {std_time / inline_time:.2f}x")
# Ожидаемый результат: ~1.42x
```

---

## Приоритет

**P0** — Критический путь. Даёт 42% ускорение относительно standard mode.

---

## Критерии завершения

- [ ] `D(5.0)` via `__code__` подмена ≥ 18M calls/sec
- [ ] `H(5.0)` via `__code__` подмена ≥ 18M calls/sec
- [ ] Hot loop ускорение ≥ 30% (измерено в секундах)
- [ ] Все тесты `tests/test_math.py` проходят
- [ ] Все тесты `tests/test_nucleus_*.py` проходят
- [ ] `EUGENIA_INLINE=1` флаг работает корректно
- [ ] Математическая корректность: inline-версии дают те же результаты
- [ ] Rollback работает: `restore_inline()` восстанавливает оригинальную функцию
- [ ] Context manager `inline_mode()` корректно восстанавливает состояние
- [ ] Документация в docstring каждого function

---

## Риски и ограничения

1. **Python 3.14 совместимость:** `__code__` подмена работает в Python 3.14, но нужно тестировать на всех версиях
2. **Математическая корректность:** Inline-код не должен менять математическую семантику
3. **Rollback:** Нужно гарантировать корректное восстановление оригинального `__code__`
4. **Читаемость:** Inline-код менее читаем — нужны подробные docstring
5. **Поддержка двух режимов:** Двойной код (standard + inline) увеличивает поддержку
6. **Потенциальные баги:** Подмена `__code__` может сломать некоторые introspection-инструменты (debugger, profiler)

---

## Зависимости

- **Предшествующие:** Этап 01 (default args) — можно применять параллельно
- **Последующие:** Этап 03 (compile()/exec()) — генерация inline-кода
- **Конфликты:** Нет конфликтов с другими этапами

---

## Математическая основа

```
D_ID = 2.0  # Константа из src/core/constants.py

D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
H(a) = a : D(Id) = a / D_ID = a / 2
```

**Обоснование из отчёта:**

> Подмена `func.__code__` — даёт 1.42x ускорение для простых функций.
> 
> Подмена `frame.f_globals['D'] = lambda x: x * 2` — работает, но LOAD_GLOBAL + CALL остаётся.
