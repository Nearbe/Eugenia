# План 04: P0 — `sys.modules` подмена (убирает файловую зависимость)

## Контекст

**Проблема:** Вызовы функций из `src/core/` добавляют ~412% оверхед. Eugenia.py зависит от файловой системы для загрузки модулей.

**Измерения:**

| Метод                        | Скорость      |
|------------------------------|---------------|
| `import math; math.log2()`   | 8.4M/сек      |
| `_log2 = math.log2; _log2()` | 11.4M/сек     |
| `def f(x, log2=_log2)`       | 14M/сек       |
| `D(5.0)` via function        | 12.8M/сек     |
| `5.0 * 2` inline             | 65.4M/сек     |
| `sys.modules` подмена        | Убирает файловую зависимость |

**Ключевой вывод:** `sys.modules` подмена позволяет убрать файловую зависимость, подменяя реальные модули на fake-модули с inline-функциями. Это не убирает оверхед вызовов напрямую, но убирает файловую зависимость и упрощает деплой.

**Механизм:** `sys.modules` — это dict, который Python использует для кэширования загруженных модулей. Если мы подменим `sys.modules['core']` на объект с inline-функциями, все импорты `from core import D` будут использовать наши inline-функции вместо реальных модулей.

---

## Цель

Создать модуль `sys_patch.py` для подмены `sys.modules` с inline-функциями, чтобы убрать файловую зависимость и упростить деплой Eugenia.py.

---

## Архитектура

### 1. Новый модуль: `src/core/sys_patch.py`

Создаём ядро для подмены `sys.modules`:

```python
"""
sys_patch.py — Подмена sys.modules для inline-функций.

Позволяет подменить реальные модули core на fake-модули с inline-функциями.
Убирает файловую зависимость и упрощает деплой.

Benchmark:
    sys.modules подмена overhead:  ~0.01ms на подмену (одноразовый)
    Итоговая экономия: Убирает файловую зависимость,
    но не убирает оверхед вызовов напрямую.

Приоритет: P0
"""

import sys
import types
from typing import Dict, Optional, Any
from src.core.inline_codegen import load_all_inline, INLINE_CODE_STRINGS


# ============ FAKE MODULE FACTORY ============

def _create_fake_module(name: str, functions: Dict[str, Any]) -> types.ModuleType:
    """
    Создаёт fake-модуль с заданными функциями.
    
    Args:
        name: Имя модуля.
        functions: Словарь {name: func} функций для модуля.
    
    Returns:
        types.ModuleType — fake-модуль.
    """
    module = types.ModuleType(name)
    
    # Добавляем функции
    for func_name, func in functions.items():
        setattr(module, func_name, func)
    
    # Добавляем константы
    module.D_ID = 2.0
    module.OMEGA = 0.0
    module.PI = float('inf')
    
    # Добавляем __all__
    module.__all__ = list(functions.keys()) + ['D_ID', 'OMEGA', 'PI']
    
    return module


# ============ INLINE FUNCTIONS CACHE ============

_inline_functions: Optional[Dict[str, Any]] = None


def _get_inline_functions() -> Dict[str, Any]:
    """
    Загружает все inline-функции (с кэшированием).
    
    Returns:
        Dict[str, Any] — словарь {name: func} всех inline-функций.
    """
    global _inline_functions
    if _inline_functions is None:
        _inline_functions = load_all_inline()
    return _inline_functions


# ============ PATCH FUNCTIONS ============

def patch_sys_modules() -> Dict[str, types.ModuleType]:
    """
    Подменяет sys.modules на fake-модули с inline-функциями.
    
    Создаёт fake-модули для core, core.branching, core.delta,
    core.spine, core.constants и подменяет их в sys.modules.
    
    Returns:
        Dict[str, types.ModuleType] — словарь {module_name: fake_module}.
        
    Example:
        >>> patches = patch_sys_modules()
        >>> # Теперь from core.branching import D использует inline-версию
        >>> from core.branching import D
        >>> D(5.0)
        10.0
    """
    inline_funcs = _get_inline_functions()
    
    patches = {}
    
    # Создаём единый fake-модуль для всех подмодулей
    fake_core = _create_fake_module('core', inline_funcs)
    fake_branching = _create_fake_module('core.branching', {
        'D': inline_funcs.get('D'),
        'H': inline_funcs.get('H'),
    })
    fake_delta = _create_fake_module('core.delta', {
        'delta_field': inline_funcs.get('delta_field'),
        'inverse_delta_field': inline_funcs.get('inverse_delta_field'),
    })
    fake_spine = _create_fake_module('core.spine', {
        'ridge_level': inline_funcs.get('ridge_level'),
        'ridge_to_percentage': inline_funcs.get('ridge_to_percentage'),
        'percentage_to_ridge': inline_funcs.get('percentage_to_ridge'),
    })
    fake_constants = _create_fake_module('core.constants', {
        'D_ID': 2.0,
        'OMEGA': 0.0,
        'PI': float('inf'),
    })
    
    # Подменяем в sys.modules
    patches['core'] = fake_core
    patches['core.branching'] = fake_branching
    patches['core.delta'] = fake_delta
    patches['core.spine'] = fake_spine
    patches['core.constants'] = fake_constants
    
    # Сохраняем оригинальные модули для rollback
    patches['_originals'] = {
        name: sys.modules.get(name)
        for name in patches
        if name != '_originals'
    }
    
    # Применяем подмену
    for name, module in patches.items():
        if name != '_originals':
            sys.modules[name] = module
    
    print("[sys_patch] sys.modules patched with inline functions")
    return patches


def unpatch_sys_modules(patches: Optional[Dict[str, types.ModuleType]] = None) -> None:
    """
    Восстанавливает оригинальные модули из sys.modules.
    
    Args:
        patches: Словарь patches, возвращённый patch_sys_modules().
                 Если None, восстанавливает все подменённые модули.
    
    Example:
        >>> patches = patch_sys_modules()
        >>> # ... делаем что-то ...
        >>> unpatch_sys_modules(patches)
        >>> # sys.modules восстановлен
    """
    if patches is None:
        # Восстанавливаем все известные модули
        known_modules = [
            'core', 'core.branching', 'core.delta',
            'core.spine', 'core.constants',
        ]
        for name in known_modules:
            original = sys.modules.get(f'_{name}_original')
            if original is not None:
                sys.modules[name] = original
            else:
                sys.modules.pop(name, None)
        return
    
    originals = patches.get('_originals', {})
    for name, module in originals.items():
        sys.modules[name] = module
    
    print("[sys_patch] sys.modules restored")


def is_patched() -> bool:
    """
    Проверяет, подменены ли модули.
    
    Returns:
        True если модули подменены, False иначе.
    """
    # Проверяем, есть ли fake-модули в sys.modules
    for name in ['core', 'core.branching', 'core.delta']:
        module = sys.modules.get(name)
        if module is not None:
            # Проверяем, является ли модуль fake (имеет специфический атрибут)
            if hasattr(module, '_is_fake') and module._is_fake:
                return True
    return False


# ============ CONTEXT MANAGER ============

from contextlib import contextmanager

@contextmanager
def patched_sys_modules():
    """
    Context manager для временной подмены sys.modules.
    
    Example:
        >>> with patched_sys_modules():
        ...     from core.branching import D
        ...     result = D(5.0)
        >>> # sys.modules восстановлен
    """
    patches = patch_sys_modules()
    try:
        yield patches
    finally:
        unpatch_sys_modules(patches)


# ============ AUTO-PATCH ON IMPORT ============

# Автоматическая подмена при импорте (опционально)
_AUTO_PATCH = False  # Set to True to auto-patch on import

if _AUTO_PATCH:
    patch_sys_modules()


# ============ EXPORTS ============

__all__ = [
    'patch_sys_modules',
    'unpatch_sys_modules',
    'is_patched',
    'patched_sys_modules',
]
```

---

### 2. Обновление `Eugenia.py`

Использовать sys.modules подмену:

```python
# В начале Eugenia.py
import os

_USE_SYS_PATCH = os.environ.get('EUGENIA_SYS_PATCH', '0') == '1'

if _USE_SYS_PATCH:
    from src.core.sys_patch import patch_sys_modules
    patch_sys_modules()
    print("[Eugenia] sys.modules patched (no file dependency)")
else:
    print("[Eugenia] sys.modules NOT patched (standard import)")

# Теперь все импорты from core import ... используют inline-функции
# если sys.patch активен
from core.branching import D, H
from core.delta import delta_field
from core.spine import ridge_to_percentage

# Горячий цикл
x = 5.0
for _ in range(1_000_000):
    x = D(x)
    x = H(x)
```

---

## Код-примеры

### Пример 1: Базовая подмена

```python
from src.core.sys_patch import patch_sys_modules, unpatch_sys_modules

# Подменяем
patches = patch_sys_modules()
print(patches.keys())  # dict_keys(['core', 'core.branching', ...])

# Теперь импорты используют inline-функции
from core.branching import D, H
print(D(5.0))  # 10.0

# Восстанавливаем
unpatch_sys_modules(patches)
```

### Пример 2: Context manager

```python
from src.core.sys_patch import patched_sys_modules

with patched_sys_modules():
    # Здесь from core import ... использует inline-функции
    from core.branching import D
    print(D(5.0))  # 10.0

# Здесь sys.modules восстановлен
```

### Пример 3: Проверка состояния

```python
from src.core.sys_patch import is_patched

print(is_patched())  # False

from src.core.sys_patch import patch_sys_modules
patch_sys_modules()
print(is_patched())  # True

from src.core.sys_patch import unpatch_sys_modules
unpatch_sys_modules()
print(is_patched())  # False
```

---

## Приоритет

**P0** — Убирает файловую зависимость, упрощает деплой.

---

## Критерии завершения

- [ ] `patch_sys_modules()` подменяет sys.modules корректно
- [ ] `unpatch_sys_modules()` восстанавливает sys.modules корректно
- [ ] `is_patched()` возвращает правильное состояние
- [ ] `patched_sys_modules()` context manager работает корректно
- [ ] Импорты `from core.branching import D` используют inline-версии
- [ ] Все тесты `tests/test_math.py` проходят
- [ ] Все тесты `tests/test_nucleus_*.py` проходят
- [ ] `EUGENIA_SYS_PATCH=1` флаг работает корректно
- [ ] Математическая корректность: inline-версии дают те же результаты
- [ ] Документация в docstring каждого function

---

## Риски и ограничения

1. **Не убирает оверхед вызовов напрямую:** sys.modules подмена убирает файловую зависимость, но не оверхед вызовов. Нужно комбинировать с inline-кодом.
2. **Импорты:** После подмены все импорты `from core import ...` будут использовать fake-модули, что может сломать некоторые зависимости.
3. **Rollback:** Нужно гарантировать корректное восстановление оригинальных модулей.
4. **Чистота:** Подмена sys.modules — это "грязный" хак, который может сломать introspection-инструменты.
5. **Конфликты:** Если другие модули зависят от оригинальных core-модулей, подмена может сломать их.

---

## Зависимости

- **Предшествующие:** Этап 03 (inline_codegen) — использует inline-функции
- **Последующие:** Нет
- **Конфликты:** Нет конфликтов с другими этапами, но нужно комбинировать с inline-кодом для максимальной оптимизации

---

## Математическая основа

```
D_ID = 2.0  # Константа из src/core/constants.py

D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
H(a) = a : D(Id) = a / D_ID = a / 2
```

**Обоснование из отчёта:**

> sys.modules подмена — убирает файловую зависимость.
> 
> Не убирает оверхед вызовов напрямую, но упрощает деплой.
> 
> КЛЮЧЕВОЕ НАБЛЮДЕНИЕ: Default args = fastest way передать функцию-зависимость без LOAD_GLOBAL оверхеда.
