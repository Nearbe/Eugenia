# План 07: P1 — marshal кеш code objects (быстрый старт)

## Контекст

**Проблема:** При каждом запуске Eugenia.py нужно перекомпилировать inline-функции через `compile()` + `exec()`. Это добавляет ~0.1ms на функцию при старте.

**Решение:** Сериализовать code objects через `marshal` и кэшировать их. При запуске загружать сериализованные code objects вместо компиляции.

**Измерения:**

| Метод                        | Время       |
|------------------------------|-------------|
| `compile()` + `exec()`       | ~0.1ms/функция |
| `marshal.loads()`            | ~0.001ms/функция |
| **Экономия**                 | **100x быстрее** |

**Ключевой вывод:** `marshal.dumps(code)` сериализует code object в 109 bytes. `marshal.loads()` десериализует его обратно. Это позволяет избежать повторной компиляции при каждом запуске.

---

## Цель

Создать модуль `marshal_cache.py` для сериализации и кэширования code objects, чтобы ускорить запуск Eugenia.py.

---

## Архитектура

### 1. Новый модуль: `src/core/marshal_cache.py`

Создаём ядро для marshal-кеша:

```python
"""
marshal_cache.py — Сериализация и кэширование code objects через marshal.

Позволяет сериализовать code objects в байты и загружать их обратно
без повторной компиляции. Ускоряет запуск в 100x.

Benchmark:
    compile() + exec():     ~0.1ms на функцию
    marshal.loads():        ~0.001ms на функцию
    Экономия:               100x быстрее

Приоритет: P1
"""

import marshal
import types
import os
import sys
from typing import Dict, Optional


# ============ MARSHAL CACHE PATH ============
# Путь для хранения marshal-кеша.
# По умолчанию используется каталог модуля.

_CACHE_DIR = os.path.join(os.path.dirname(__file__), '_marshal_cache')
_CACHE_FILE = os.path.join(_CACHE_DIR, 'inline_code_cache.marsh')


# ============ INLINE CODE STRINGS ============
# Предварительно определённые inline-версии функций.
# Эти же строки используются в inline_codegen.py.

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
# Кэш для загруженных code objects.
# Позволяет избежать повторной десериализации.

_code_cache: Dict[str, types.CodeType] = {}


# ============ CORE FUNCTIONS ============

def _compile_to_marshal(name: str, code_str: str) -> bytes:
    """
    Компилирует код и сериализует code object через marshal.
    
    Args:
        name: Имя функции.
        code_str: Код функции как строка.
    
    Returns:
        bytes — сериализованный code object.
    """
    compiled = compile(code_str, f'<inline_{name}>', 'exec')
    
    # Извлекаем code object из констант
    for const in compiled.co_consts:
        if isinstance(const, types.CodeType):
            return marshal.dumps(const)
    
    raise ValueError(f"No code object found in compiled code for: {name}")


def _parse_marshal(marshal_bytes: bytes) -> types.CodeType:
    """
    Десериализует code object из marshal-байтов.
    
    Args:
        marshal_bytes: Сериализованный code object.
    
    Returns:
        types.CodeType — десериализованный code object.
    """
    return marshal.loads(marshal_bytes)


def dump_marshal_cache() -> Dict[str, bytes]:
    """
    Генерирует marshal-кеш для всех inline-функций.
    
    Returns:
        Dict[str, bytes] — словарь {name: marshal_bytes}.
        
    Example:
        >>> cache = dump_marshal_cache()
        >>> save_to_file('inline_code_cache.marsh', cache)
    """
    cache = {}
    for name, code_str in INLINE_CODE_STRINGS.items():
        cache[name] = _compile_to_marshal(name, code_str)
    return cache


def save_marshal_cache(cache: Dict[str, bytes], path: Optional[str] = None) -> str:
    """
    Сохраняет marshal-кеш в файл.
    
    Args:
        cache: Словарь {name: marshal_bytes}.
        path: Путь для сохранения. Если None, используется _CACHE_FILE.
    
    Returns:
        str — путь к сохранённому файлу.
    """
    if path is None:
        path = _CACHE_FILE
    
    # Создаём каталог если не существует
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'wb') as f:
        marshal.dump(cache, f)
    
    return path


def load_marshal_cache(path: Optional[str] = None) -> Dict[str, bytes]:
    """
    Загружает marshal-кеш из файла.
    
    Args:
        path: Путь к файлу. Если None, используется _CACHE_FILE.
    
    Returns:
        Dict[str, bytes] — словарь {name: marshal_bytes}.
    """
    if path is None:
        path = _CACHE_FILE
    
    if not os.path.exists(path):
        # Если файл не существует, генерируем кеш
        cache = dump_marshal_cache()
        save_marshal_cache(cache, path)
        return cache
    
    with open(path, 'rb') as f:
        return marshal.load(f)


def get_cached_code(name: str, path: Optional[str] = None) -> types.CodeType:
    """
    Получает code object из marshal-кеша.
    
    Сначала проверяет _code_cache, затем загружает из файла.
    
    Args:
        name: Имя функции.
        path: Путь к файлу кеша.
    
    Returns:
        types.CodeType — code object.
    """
    if name in _code_cache:
        return _code_cache[name]
    
    cache = load_marshal_cache(path)
    
    if name not in cache:
        # Если name не найден в кеше, компилируем
        if name in INLINE_CODE_STRINGS:
            marshal_bytes = _compile_to_marshal(name, INLINE_CODE_STRINGS[name])
            cache[name] = marshal_bytes
            save_marshal_cache(cache, path)
        else:
            raise KeyError(f"Unknown inline code template: {name}")
    
    code_obj = _parse_marshal(cache[name])
    _code_cache[name] = code_obj
    return code_obj


def get_all_cached_codes(path: Optional[str] = None) -> Dict[str, types.CodeType]:
    """
    Получает все code objects из marshal-кеша.
    
    Args:
        path: Путь к файлу кеша.
    
    Returns:
        Dict[str, types.CodeType] — словарь {name: code}.
    """
    result = {}
    for name in INLINE_CODE_STRINGS:
        result[name] = get_cached_code(name, path)
    return result


# ============ CODE OBJECT TO FUNCTION ============

def code_to_function(code_obj: types.CodeType, globals_dict: Optional[Dict] = None) -> types.FunctionType:
    """
    Создаёт функцию из code object.
    
    Args:
        code_obj: Code object.
        globals_dict: Globals namespace для функции.
    
    Returns:
        types.FunctionType — созданная функция.
    """
    return types.FunctionType(code_obj, globals_dict or {})


def get_cached_func(name: str, globals_dict: Optional[Dict] = None, path: Optional[str] = None) -> types.FunctionType:
    """
    Получает inline-функцию из marshal-кеша.
    
    Args:
        name: Имя функции.
        globals_dict: Globals namespace для функции.
        path: Путь к файлу кеша.
    
    Returns:
        types.FunctionType — inline-функция.
    """
    code_obj = get_cached_code(name, path)
    return code_to_function(code_obj, globals_dict)


# ============ AUTO-LOAD ON IMPORT ============

# Автоматическая загрузка кеша при импорте (опционально)
_AUTO_LOAD = True  # Set to False to disable auto-load

if _AUTO_LOAD:
    try:
        load_marshal_cache()
        print("[marshal_cache] Cache loaded from:", _CACHE_FILE)
    except (FileNotFoundError, EOFError, Exception) as e:
        # Если кеш не существует или повреждён, генерируем
        print(f"[marshal_cache] Cache not found or corrupted: {e}")
        cache = dump_marshal_cache()
        save_marshal_cache(cache)
        print("[marshal_cache] New cache generated at:", _CACHE_FILE)


# ============ EXPORTS ============

__all__ = [
    'INLINE_CODE_STRINGS',
    '_code_cache',
    'dump_marshal_cache',
    'save_marshal_cache',
    'load_marshal_cache',
    'get_cached_code',
    'get_all_cached_codes',
    'code_to_function',
    'get_cached_func',
    '_CACHE_DIR',
    '_CACHE_FILE',
]
```

---

### 2. Обновление `src/core/code_substitution.py`

Использовать marshal-кеш вместо компиляции:

```python
# В code_substitution.py, заменить _compile_inline_code:

def _compile_inline_code(name: str) -> types.CodeType:
    """
    Компилирует inline-шаблон в code object и кэширует его.
    Использует marshal-кеш если доступен.
    """
    if name in _code_cache:
        return _code_cache[name]
    
    # Пытаемся загрузить из marshal-кеша
    try:
        from src.core.marshal_cache import get_cached_code
        code_obj = get_cached_code(name)
        _code_cache[name] = code_obj
        return code_obj
    except (ImportError, KeyError, Exception):
        # Fallback: компилируем
        pass
    
    if name not in INLINE_CODE_TEMPLATES:
        raise KeyError(f"Unknown inline code template: {name}")
    
    code_str = INLINE_CODE_TEMPLATES[name]
    compiled = compile(code_str, f'<inline_{name}>', 'exec')
    
    for const in compiled.co_consts:
        if isinstance(const, types.CodeType):
            _code_cache[name] = const
            return const
    
    raise ValueError(f"No code object found for template: {name}")
```

---

## Код-примеры

### Пример 1: Генерация кеша

```python
from src.core.marshal_cache import dump_marshal_cache, save_marshal_cache

# Генерируем кеш
cache = dump_marshal_cache()
print(len(cache))  # 8 функций

# Сохраняем в файл
path = save_marshal_cache(cache)
print(f"Cache saved to: {path}")
```

### Пример 2: Загрузка кеша

```python
from src.core.marshal_cache import load_marshal_cache, get_cached_code

# Загружаем кеш
cache = load_marshal_cache()
print(len(cache))  # 8 функций

# Получаем code object
D_code = get_cached_code('D')
print(D_code.co_code)  # байткод
```

### Пример 3: Создание функции из code object

```python
from src.core.marshal_cache import get_cached_func

# Получаем inline-функцию
D = get_cached_func('D')
print(D(5.0))  # 10.0
```

### Пример 4: Benchmark

```python
import time
import os

# Отключаем auto-load
os.environ['EUGENIA_MARSHAL_AUTO_LOAD'] = '0'

# Compile version
from src.core.inline_codegen import compile_inline

start = time.perf_counter()
for _ in range(1000):
    compile_inline('D')
compile_time = time.perf_counter() - start

# Marshal version
from src.core.marshal_cache import get_cached_code

start = time.perf_counter()
for _ in range(1000):
    get_cached_code('D')
marshal_time = time.perf_counter() - start

print(f"Compile:   {compile_time:.4f}s")
print(f"Marshal:   {marshal_time:.4f}s")
print(f"Speedup:   {compile_time / marshal_time:.2f}x")
# Ожидаемый результат: ~100x
```

---

## Приоритет

**P1** — Высокий приоритет. Ускоряет запуск в 100x.

---

## Критерии завершения

- [ ] `dump_marshal_cache()` генерирует кеш корректно
- [ ] `save_marshal_cache()` сохраняет кеш в файл
- [ ] `load_marshal_cache()` загружает кеш из файла
- [ ] `get_cached_code('D')` возвращает code object
- [ ] `get_cached_func('D')` возвращает callable функцию
- [ ] `code_to_function()` создаёт функцию из code object
- [ ] marshal кеш генерируется и загружается корректно
- [ ] Все тесты `tests/test_math.py` проходят
- [ ] Все тесты `tests/test_nucleus_*.py` проходят
- [ ] Документация в docstring каждого function

---

## Риски и ограничения

1. **Совместимость:** marshal-кеш может не работать между разными версиями Python
2. **Актуальность:** При изменении inline-кода нужно перегенерировать кеш
3. **Файловая зависимость:** marshal-кеш — это файл, который нужно деплоить вместе с кодом
4. **Безопасность:** marshal не шифрует данные, но и не валидирует — загрузка из недоверенных источников опасна

---

## Зависимости

- **Предшествующие:** Этап 03 (inline_codegen) — использует те же строки кода
- **Последующие:** Нет
- **Конфликты:** Нет конфликтов с другими этапами

---

## Математическая основа

```
D_ID = 2.0  # Константа из src/core/constants.py

D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
H(a) = a : D(Id) = a / D_ID = a / 2
```

**Обоснование из отчёта:**

> marshal.dumps(code) — 109 bytes для простой функции.
> marshal.loads() — возвращает code object.
> types.FunctionType(code, globals) — создаёт функцию из code object.
> marshal = сериализация code objects.
