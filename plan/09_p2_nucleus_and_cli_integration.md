# План 09: P2 — Обновление nucleus модулей + CLI интеграция

## Контекст

**Проблема:** После обновления `src/core/` нужно обновить `src/nucleus/` модули для работы в inline-режиме, а также добавить CLI-флаги для переключения режимов.

**Модули `src/nucleus/`:** 21 модуль, которые зависят от `src/core/` и используют функции D, H, delta_field, ridge_to_percentage и другие.

**CLI-флаги:**
- `--inline` — включает inline-режим в Eugenia.py
- `--optimization` — включает оптимизацию в generate.py

---

## Цель

Обновить 21 модуль `src/nucleus/` для поддержки inline-режима и добавить CLI-флаги `--inline` и `--optimization`.

---

## Архитектура

### 1. Обновление `Eugenia.py`

Добавляем CLI-флаги:

```python
"""
Eugenia.py — Main entry point для Eugenia.

CLI-флаги:
    --inline: включает inline-режим
    --optimization: включает оптимизацию
    --mode: выбор режима (standard, fast, inline, marshal)

Приоритет: P2
"""

import os
import sys
import argparse


# ============ CLI PARSER ============

def parse_args():
    """Парсит CLI-аргументы."""
    parser = argparse.ArgumentParser(
        description='Eugenia — Infinite loop with core math operations'
    )
    parser.add_argument(
        '--inline',
        action='store_true',
        default=False,
        help='Enable inline mode for D/H/delta_field optimization'
    )
    parser.add_argument(
        '--optimization',
        choices=['standard', 'fast', 'inline', 'marshal'],
        default=None,
        help='Optimization mode'
    )
    parser.add_argument(
        '--sys-patch',
        action='store_true',
        default=False,
        help='Enable sys.modules patching'
    )
    parser.add_argument(
        '--marshal-cache',
        action='store_true',
        default=False,
        help='Enable marshal cache for code objects'
    )
    return parser.parse_args()


# ============ CONFIGURATION ============

args = parse_args()

# Определяем режим работы
if args.optimization:
    _MODE = args.optimization
elif args.inline:
    _MODE = 'inline'
else:
    _MODE = os.environ.get('EUGENIA_MODE', 'standard')

# Включаем inline-режим
if _MODE in ('fast', 'inline', 'marshal'):
    os.environ['EUGENIA_INLINE'] = '1'

# Включаем fast-режим
if _MODE == 'fast':
    os.environ['EUGENIA_FAST'] = '1'

# Включаем sys.modules patch
if _MODE == 'marshal' or args.sys_patch:
    os.environ['EUGENIA_SYS_PATCH'] = '1'

# Включаем marshal cache
if _MODE == 'marshal' or args.marshal_cache:
    os.environ['EUGENIA_MARSHAL_CACHE'] = '1'

print(f"[Eugenia] Mode: {_MODE}")
print(f"[Eugenia] Inline: {os.environ.get('EUGENIA_INLINE', '0')}")
print(f"[Eugenia] Fast: {os.environ.get('EUGENIA_FAST', '0')}")
print(f"[Eugenia] SysPatch: {os.environ.get('EUGENIA_SYS_PATCH', '0')}")
print(f"[Eugenia] Marshal: {os.environ.get('EUGENIA_MARSHAL_CACHE', '0')}")


# ============ IMPORTS ============

if _MODE in ('fast', 'inline', 'marshal'):
    # Используем оптимизированные версии
    if os.environ.get('EUGENIA_SYS_PATCH') == '1':
        from src.core.sys_patch import patch_sys_modules
        patch_sys_modules()
        print("[Eugenia] sys.modules patched")
    
    from src.core.fast_ops import D_fast as D, H_fast as H
    from src.core.delta import delta_field
    from src.core.spine import ridge_to_percentage
else:
    # Используем стандартные версии
    from src.core.branching import D, H
    from src.core.delta import delta_field
    from src.core.spine import ridge_to_percentage

print("[Eugenia] Imports complete")


# ============ HOT LOOP ============

def hot_loop(n_iterations=1_000_000):
    """
    Горячий цикл Eugenia.
    
    Args:
        n_iterations: Количество итераций
    """
    x = 5.0
    for i in range(n_iterations):
        x = D(x)  # ~14M calls/sec с default args, ~18.2M с __code__ подменой
        x = H(x)  # ~14M calls/sec с default args, ~18.2M с __code__ подменой
        _ = delta_field(x)  # ~3x ускорение с inline
        _ = ridge_to_percentage(x)  # ~2-3x ускорение с inline
    
    return x


# ============ MAIN ============

if __name__ == '__main__':
    print("[Eugenia] Starting hot loop...")
    
    import time
    start = time.perf_counter()
    result = hot_loop(1_000_000)
    elapsed = time.perf_counter() - start
    
    print(f"[Eugenia] Hot loop complete: {result}")
    print(f"[Eugenia] Time: {elapsed:.4f}s")
    print(f"[Eugenia] Iterations/sec: {1_000_000 / elapsed:,.0f}")
```

---

### 2. Обновление `generate.py`

Добавляем `--optimization` флаг:

```python
"""
generate.py — Generation script для Eugenia.

CLI-флаги:
    --optimization: выбор режима оптимизации (standard, fast, inline, marshal)
    --output: путь для вывода
    --iterations: количество итераций

Приоритет: P2
"""

import os
import sys
import argparse


# ============ CLI PARSER ============

def parse_args():
    """Парсит CLI-аргументы."""
    parser = argparse.ArgumentParser(
        description='Generate output from Eugenia'
    )
    parser.add_argument(
        '--optimization',
        choices=['standard', 'fast', 'inline', 'marshal'],
        default='standard',
        help='Optimization mode'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output path'
    )
    parser.add_argument(
        '--iterations',
        type=int,
        default=1_000_000,
        help='Number of iterations'
    )
    return parser.parse_args()


# ============ CONFIGURATION ============

args = parse_args()

if args.optimization in ('fast', 'inline', 'marshal'):
    os.environ['EUGENIA_INLINE'] = '1'
if args.optimization == 'fast':
    os.environ['EUGENIA_FAST'] = '1'
if args.optimization == 'marshal':
    os.environ['EUGENIA_SYS_PATCH'] = '1'
    os.environ['EUGENIA_MARSHAL_CACHE'] = '1'

print(f"[generate] Optimization: {args.optimization}")


# ============ IMPORTS ============

if args.optimization in ('fast', 'inline', 'marshal'):
    from src.core.fast_ops import D_fast as D, H_fast as H
else:
    from src.core.branching import D, H


# ============ GENERATION ============

def generate(n_iterations=1_000_000):
    """
    Генерация выходных данных.
    
    Args:
        n_iterations: Количество итераций
    """
    x = 5.0
    results = []
    
    for _ in range(n_iterations):
        x = D(x)
        x = H(x)
        results.append(x)
    
    return results


# ============ MAIN ============

if __name__ == '__main__':
    print(f"[generate] Generating {args.iterations} iterations...")
    
    import time
    start = time.perf_counter()
    results = generate(args.iterations)
    elapsed = time.perf_counter() - start
    
    print(f"[generate] Generated {len(results)} results")
    print(f"[generate] Time: {elapsed:.4f}s")
    print(f"[generate] Iterations/sec: {args.iterations / elapsed:,.0f}")
    
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(results, f)
        print(f"[generate] Saved to {args.output}")
```

---

### 3. Обновление `config.yaml`

Добавляем секцию `optimization`:

```yaml
# config.yaml — Конфигурация Eugenia

# Оптимизация
optimization:
  mode: "standard"  # "standard" | "fast" | "inline" | "marshal"
  inline_functions:
    - "D"
    - "H"
    - "delta_field"
    - "ridge_to_percentage"
  sys_modules_patch: false
  marshal_cache: true

# Запуск
run:
  iterations: 1000000
  output: null

# Логирование
logging:
  level: "INFO"
  file: null
```

---

### 4. Обновление `src/nucleus/` модулей

Каждый из 21 модуля `src/nucleus/` получает поддержку inline-режима:

```python
"""
nucleus_module.py — Nucleus module для Eugenia.

Поддержка inline-режима через env var EUGENIA_INLINE.

Приоритет: P2
"""

import os

_USE_INLINE = os.environ.get('EUGENIA_INLINE', '0') == '1'

if _USE_INLINE:
    # Используем inline-версии из core
    from src.core.fast_ops import D_fast as D, H_fast as H
    from src.core.delta import delta_field
    from src.core.spine import ridge_to_percentage
else:
    # Используем стандартные версии
    from src.core.branching import D, H
    from src.core.delta import delta_field
    from src.core.spine import ridge_to_percentage


__all__ = ['some_function']
```

---

## Код-примеры

### Пример 1: Запуск с inline-режимом

```bash
# Стандартный режим
python Eugenia.py

# Inline-режим
python Eugenia.py --inline

# Fast-режим
python Eugenia.py --optimization fast

# Marshal-режим
python Eugenia.py --optimization marshal
```

### Пример 2: Генерация с оптимизацией

```bash
# Стандартная генерация
python generate.py

# С inline-оптимизацией
python generate.py --optimization inline

# С marshal-кешем
python generate.py --optimization marshal --output results.json
```

### Пример 3: Конфигурация через config.yaml

```python
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

mode = config['optimization']['mode']
print(f"Mode: {mode}")
```

---

## Приоритет

**P2** — Средний приоритет. Обновление 21 модуля nucleus + CLI.

---

## Критерии завершения

- [ ] `Eugenia.py --inline` включает inline-режим
- [ ] `Eugenia.py --optimization fast/inline/marshal` работает корректно
- [ ] `generate.py --optimization` работает корректно
- [ ] `config.yaml` поддерживает секцию `optimization`
- [ ] Все 21 модуль `src/nucleus/` работает в inline-режиме
- [ ] Все тесты `tests/test_math.py` проходят
- [ ] Все тесты `tests/test_nucleus_*.py` проходят
- [ ] Документация в docstring каждого function

---

## Риски и ограничения

1. **CLI-совместимость:** Новые флаги могут сломать существующие скрипты
2. **Конфигурация:** config.yaml может содержать устаревшие параметры
3. **21 модуль nucleus:** Нужно обновить каждый модуль
4. **Тестирование:** Нужно тестировать оба режима для каждого модуля

---

## Зависимости

- **Предшествующие:** Этап 08 (dual-path архитектура)
- **Последующие:** Этап 10 (benchmarks, profiling, долгосрочные направления)
- **Конфликты:** Нет конфликтов с другими этапами

---

## Математическая основа

```
D_ID = 2.0  # Константа из src/core/constants.py

D(a) = a : Ω = a ⊕ a = a * D_ID = a * 2
H(a) = a : D(Id) = a / D_ID = a / 2
```

**Обоснование из отчёта:**

> Обновление Eugenia.py — --inline флаг CLI.
> Обновление generate.py — --optimization флаг.
> Обновление config.yaml — секция optimization.
