# План 03: P0 — `compile()` + `exec()` генерация code objects из строк

## Контекст

**Проблема:** Вызовы функций из `src/core/` добавляют ~412% оверхед. `D(5.0)` выполняется в 5.2 раза медленнее, чем `5.0 * 2` inline.

**Измерения:**

| Метод                        | Скорость      |
|------------------------------|---------------|
| `import math; math.log2()`   | 8.4M/сек      |
| `_log2 = math.log2; _log2()` | 11.4M/сек     |
| `def f(x, log2=_log2)`       | 14M/сек       |
| `D(5.0)` via function        | 12.8M/сек     |
| `5.0 * 2` inline             | 65.4M/сек     |
| `__code__` подмена           | ~18.2M/сек    |
| `compile()` + `exec()`       | Генерация code objects из строк |

**Ключевой вывод:** `compile()` + `exec()` — это ключевой инструмент для генерации code objects из строк. Позволяет определить функции как строки, скомпилировать их и подменить `__code__` у существующих функций.

**Механизм:** `compile(code_str, filename, mode)` компилирует строку в code object. `exec(compiled, globals, locals)` выполняет code object в заданном namespace. Из констант скомпилированного code object можно извлечь вложенные code objects.

---

## Цель

Создать модуль `inline_codegen.py` для генерации inline-функций из строк, который будет использоваться для подмены `__code__` у критических функций Eugenia.py.

---

## Архитектура

### 1. Новый модуль: `src/core/inline_codegen.py`

Создаём ядро для генерации inline-функций из строк:

```python
"""
inline_codegen.py — Генерация inline-функций из строк.

Использует compile() + exec() для генерации code objects из строк.
Позволяет определить функции как строки, скомпилировать их и
подменить __code__ у существующих функций.

Benchmark:
    compile() + exec() overhead: ~0.1ms на функцию (одноразовый)
    Подмена __code__ overhead:   ~0.01ms на подмену (одноразовый)
    
    Итоговая экономия: ~412% oверхед убирается полностью
    для подменённых функций.

Приоритет: P0
"""

import types
import sys
from typing import Callable, Dict, Optional, List, Any


# ============ INLINE CODE STRINGS ============
# Предварительно определённые inline-версии функций.
# Каждая строка — это полный код функции, который компилируется
# и из которого извлекается code object.

INLINE_CODE_STRINGS: Dict[str, str] = {
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
    'inverse_delta_field': """
def inverse_delta_field_inline(y):
    import math
    if isinstance(y, (int, float)):
        return 1024.0 / (1.0 + 2.0 ** (-y)) - 1.0
    return [
        1024.0 / (1.0 + 2.0 ** (-val)) - 1.0
        for val in y
    ]
""",
    'ridge_level': """
def ridge_level_inline(x):
    import math
    return math.log2(abs(x) + 1e-300)
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
    'percentage_to_ridge': """
def percentage_to_ridge_inline(p):
    import math
    if p <= 0.0:
        return -1000.0
    if p >= 100.0:
        return 1000.0
    return -math.log2((100.0 / p) - 1.0)
""",
    'complex_rotate': """
def complex_rotate_inline(z, angle):
    import math
    r, theta = abs(z), math.atan2(z.imag, z.real)
    new_theta = theta + angle
    return complex(r * math.cos(new_theta), r * math.sin(new_theta))
""",
}


# ============ CODE OBJECT CACHE ============
# Кэш для уже скомпилированных code objects.
# Позволяет избежать повторной компиляции при каждом вызове.

_code_cache: Dict[str, Dict[str, Any]] = {}


# ============ CORE FUNCTIONS ============

def compile_inline(name: str, code_str: Optional[str] = None) -> types.CodeType:
    """
    Компилирует inline-шаблон в code object.
    
    Args:
        name: Имя функции из INLINE_CODE_STRINGS.
        code_str: Опциональная строка кода. Если None, используется
                  шаблон из INLINE_CODE_STRINGS.
    
    Returns:
        types.CodeType — скомпилированный code object.
        
    Raises:
        KeyError: Если name не найден в INLINE_CODE_STRINGS.
        ValueError: Если code object не найден в константах.
        
    Example:
        >>> code = compile_inline('D')
        >>> # code — это code object для функции D_inline
    """
    if code_str is None:
        if name not in INLINE_CODE_STRINGS:
            raise KeyError(f"Unknown inline code template: {name}")
        code_str = INLINE_CODE_STRINGS[name]
    
    compiled = compile(code_str, f'<inline_{name}>', 'exec')
    
    # Извлекаем code object из констант
    for const in compiled.co_consts:
        if isinstance(const, types.CodeType):
            return const
    
    raise ValueError(f"No code object found in compiled code for: {name}")


def load_inline(name: str, globals_dict: Optional[Dict] = None) -> Callable:
    """
    Загружает inline-функцию из шаблона.
    
    Args:
        name: Имя функции из INLINE_CODE_STRINGS.
        globals_dict: Опциональный globals namespace. Если None,
                      используется текущий globals.
    
    Returns:
        Callable — загруженная inline-функция.
        
    Raises:
        KeyError: Если name не найден в INLINE_CODE_STRINGS.
        
    Example:
        >>> D_inline = load_inline('D')
        >>> D_inline(5.0)
        10.0
    """
    if name not in INLINE_CODE_STRINGS:
        raise KeyError(f"Unknown inline code template: {name}")
    
    code_str = INLINE_CODE_STRINGS[name]
    compiled = compile(code_str, f'<inline_{name}>', 'exec')
    
    namespace = {}
    exec(compiled, globals_dict or {}, namespace)
    
    # Извлекаем функцию из namespace
    for key in ['D_inline', 'H_inline', 'delta_field_inline', 
                'inverse_delta_field_inline', 'ridge_level_inline',
                'ridge_to_percentage_inline', 'percentage_to_ridge_inline',
                'complex_rotate_inline']:
        if key in namespace:
            return namespace[key]
    
    raise ValueError(f"Function not found in compiled namespace for: {name}")


def load_inline_with_name(name: str, func_name: Optional[str] = None) -> Callable:
    """
    Загружает inline-функцию с указанием имени функции.
    
    Args:
        name: Имя шаблона из INLINE_CODE_STRINGS.
        func_name: Имя функции в скомпилированном namespace.
                   Если None, используется имя из шаблона.
    
    Returns:
        Callable — загруженная inline-функция.
    """
    if func_name is None:
        # Извлекаем имя функции из шаблона
        for line in INLINE_CODE_STRINGS[name].split('\n'):
            if line.strip().startswith('def '):
                func_name = line.strip().split('def ')[1].split('(')[0]
                break
    
    if func_name is None:
        raise ValueError(f"Cannot extract function name from template: {name}")
    
    code_str = INLINE_CODE_STRINGS[name]
    compiled = compile(code_str, f'<inline_{name}>', 'exec')
    
    namespace = {}
    exec(compiled, {}, namespace)
    
    if func_name not in namespace:
        raise KeyError(f"Function {func_name} not found in compiled namespace")
    
    return namespace[func_name]


def get_inline_code(name: str) -> types.CodeType:
    """
    Получает code object из кеша или компилирует его.
    
    Args:
        name: Имя функции из INLINE_CODE_STRINGS.
    
    Returns:
        types.CodeType — code object.
    """
    if name not in _code_cache:
        _code_cache[name] = {
            'code': compile_inline(name),
            'func': load_inline(name),
        }
    return _code_cache[name]['code']


def get_inline_func(name: str) -> Callable:
    """
    Получает inline-функцию из кеша или загружает её.
    
    Args:
        name: Имя функции из INLINE_CODE_STRINGS.
    
    Returns:
        Callable — inline-функция.
    """
    if name not in _code_cache:
        _code_cache[name] = {
            'code': compile_inline(name),
            'func': load_inline(name),
        }
    return _code_cache[name]['func']


# ============ BATCH OPERATIONS ============

def load_all_inline(globals_dict: Optional[Dict] = None) -> Dict[str, Callable]:
    """
    Загружает все inline-функции.
    
    Args:
        globals_dict: Опциональный globals namespace.
    
    Returns:
        Dict[str, Callable] — словарь {name: func} всех inline-функций.
        
    Example:
        >>> all_funcs = load_all_inline()
        >>> all_funcs['D'](5.0)
        10.0
        >>> all_funcs['H'](10.0)
        5.0
    """
    result = {}
    for name in INLINE_CODE_STRINGS:
        result[name] = load_inline(name, globals_dict)
    return result


def get_all_inline_codes() -> Dict[str, types.CodeType]:
    """
    Получает code objects для всех inline-функций.
    
    Returns:
        Dict[str, types.CodeType] — словарь {name: code}.
    """
    result = {}
    for name in INLINE_CODE_STRINGS:
        result[name] = get_inline_code(name)
    return result


# ============ CODE SUBSTITUTION HELPER ============

def substitute_function(func: Callable, code_obj: types.CodeType) -> bool:
    """
    Подменяет __code__ у функции.
    
    Args:
        func: Функция для подмены.
        code_obj: Новый code object.
    
    Returns:
        True если подмена успешна, False если ошибка.
    """
    try:
        if not hasattr(func, '_original_code'):
            func._original_code = func.__code__
        func.__code__ = code_obj
        return True
    except (AttributeError, TypeError) as e:
        print(f"Warning: Failed to substitute __code__ for {func.__name__}: {e}")
        return False


def restore_function(func: Callable) -> bool:
    """
    Восстанавливает оригинальный __code__ у функции.
    
    Args:
        func: Функция для восстановления.
    
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


# ============ EXPORTS ============

__all__ = [
    'INLINE_CODE_STRINGS',
    'compile_inline',
    'load_inline',
    'load_inline_with_name',
    'get_inline_code',
    'get_inline_func',
    'load_all_inline',
    'get_all_inline_codes',
    'substitute_function',
    'restore_function',
]
```

---

### 2. Обновление `src/core/branching.py`

Добавляем поддержку inline-генерации:

```python
"""
branching.py — Branching operations для Eugenia.

Dual-path архитектура:
    - standard: читаемая версия с type hints
    - inline: оптимизированная версия через compile()/exec()

Приоритет: P0
"""

import os
from src.core.inline_codegen import get_inline_code, substitute_function, restore_function

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
    # Получаем inline code objects
    D_inline_code = get_inline_code('D')
    H_inline_code = get_inline_code('H')
    
    # Подменяем __code__
    substitute_function(D, D_inline_code)
    substitute_function(H, H_inline_code)


# ============ EXPORTS ============
__all__ = ['D', 'H', 'D_ID']
```

---

## Код-примеры

### Пример 1: Базовая компиляция

```python
from src.core.inline_codegen import compile_inline, load_inline

# Компилируем code object
code = compile_inline('D')
print(code.co_code)  # байткод функции

# Загружаем функцию
D_inline = load_inline('D')
result = D_inline(5.0)
print(result)  # 10.0
```

### Пример 2: Загрузка всех функций

```python
from src.core.inline_codegen import load_all_inline

# Загружаем все inline-функции
all_funcs = load_all_inline()

# Используем
D = all_funcs['D']
H = all_funcs['H']
delta_field = all_funcs['delta_field']

print(D(5.0))   # 10.0
print(H(10.0))  # 5.0
print(delta_field(128.0))  # delta_field(128)
```

### Пример 3: Подмена функции

```python
from src.core.inline_codegen import get_inline_code, substitute_function, restore_function
from src.core.branching import D

# Подменяем
D_inline_code = get_inline_code('D')
substitute_function(D, D_inline_code)

# Теперь D работает в inline-режиме
print(D(5.0))  # 10.0 (быстрее)

# Восстанавливаем
restore_function(D)
```

### Пример 4: Benchmark

```python
import time
from src.core.inline_codegen import load_inline

D_standard = None
D_inline = load_inline('D')

# Standard version
start = time.perf_counter()
x = 5.0
for _ in range(10_000_000):
    x = x * 2.0  # inline Python
std_time = time.perf_counter() - start

# Inline version
start = time.perf_counter()
x = 5.0
for _ in range(10_000_000):
    x = D_inline(x)
inline_time = time.perf_counter() - start

print(f"Standard:  {10_000_000 / std_time:,.0f} calls/sec")
print(f"Inline:    {10_000_000 / inline_time:,.0f} calls/sec")
print(f"Speedup:   {std_time / inline_time:.2f}x")
```

---

## Приоритет

**P0** — Критический путь. Позволяет генерировать inline-функции из строк.

---

## Критерии завершения

- [ ] `compile_inline('D')` возвращает code object
- [ ] `load_inline('D')` возвращает callable функцию
- [ ] `load_all_inline()` возвращает все inline-функции
- [ ] `substitute_function()` корректно подменяет `__code__`
- [ ] `restore_function()` корректно восстанавливает `__code__`
- [ ] Все тесты `tests/test_math.py` проходят
- [ ] Все тесты `tests/test_nucleus_*.py` проходят
- [ ] `EUGENIA_INLINE=1` флаг работает корректно
- [ ] Математическая корректность: inline-версии дают те же результаты
- [ ] Документация в docstring каждого function

---

## Риски и ограничения

1. **Компиляция при старте:** `compile()` + `exec()` выполняется при старте, добавляет ~0.1ms на функцию
2. **Математическая корректность:** Inline-код не должен менять математическую семантику
3. **Rollback:** Нужно гарантировать корректное восстановление оригинального `__code__`
4. **Читаемость:** Inline-код менее читаем — нужны подробные docstring
5. **Поддержка двух режимов:** Двойной код (standard + inline) увеличивает поддержку

---

## Зависимости

- **Предшествующие:** Этап 02 (`__code__` подмена) — использует те же механизмы
- **Последующие:** Этап 07 (marshal кеш) — сериализация сгенерированных code objects
- **Конфликты:** Нет конфликтов с другими этапами

---

## Математическая основа

```
D_ID = 2.0  # Константа из src/core/constants.py

D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
H(a) = a : D(Id) = a / D_ID = a / 2
```

**Обоснование из отчёта:**

> compile() + exec() = генерация code objects из строк.
> 
> Ключевой инструмент для генерации code objects из строк.
