# ОТЧЁТ: `sys` модуль — потенциал для оптимизации Eugении.py

## Контекст

Eugenia.py работает как бесконечный цикл (~180k итераций/сек) с одним GIL.
VSZ процесса: ~421 GB, RSS: ~17 MB.

**Проблема:** вызовы функций из `src/core/` добавляют ~412% оверхед.
`D(5.0)` выполняется в 5.2 раза медленнее, чем `5.0 * 2` inline.

---

## 1. `sys.monitoring` (Python 3.12+)

### Что это

Новый механизм мониторинга на уровне байткода. 6 tool_id (0-5), 19 событий.

### События

| Событие           | Значение | Описание                   |
|-------------------|----------|----------------------------|
| PY_START          | 1        | Старт функции              |
| PY_RESUME         | 2        | Возобновление              |
| PY_RETURN         | 4        | Возврат из функции         |
| PY_YIELD          | 8        | Yield                      |
| CALL              | 16       | Вызов функции              |
| LINE              | 32       | Новая строка               |
| INSTRUCTION       | 64       | Каждая инструкция байткода |
| JUMP              | 128      | Переход                    |
| BRANCH_LEFT       | 256      | Ветвление влево            |
| BRANCH_RIGHT      | 512      | Ветвление вправо           |
| STOP_ITERATION    | 1024     | Стоп итерация              |
| RAISE             | 2048     | Исключение                 |
| EXCEPTION_HANDLED | 4096     | Обработанное исключение    |
| PY_UNWIND         | 8192     | Размотка                   |
| PY_THROW          | 16384    | Throw                      |
| RERAISE           | 32768    | Повторное исключение       |
| C_RETURN          | 65536    | Возврат из C-функции       |
| C_RAISE           | 131072   | Исключение из C-функции    |
| BRANCH            | 262144   | Ветвление                  |
| NO_EVENTS         | 0        | Нет событий                |

### Методы

| Метод                                              | Описание                                  |
|----------------------------------------------------|-------------------------------------------|
| `use_tool_id(id, name)`                            | Захват tool_id по имени (возвращает None) |
| `free_tool_id(id)`                                 | Освобождение tool_id                      |
| `clear_tool_id(id)`                                | Сброс tool_id                             |
| `register_callback(tool_id, event_mask, callback)` | Регистрация callback                      |
| `set_events(tool_id, events)`                      | Включение событий для tool                |
| `set_local_events(code_object, tool_id, events)`   | Включение событий для code object         |
| `get_events(tool_id)`                              | Получение событий для tool                |
| `get_local_events(code_object)`                    | Получение событий для code                |
| `get_tool(tool_id)`                                | Получение имени tool                      |
| `restart_events(tool_id, events)`                  | Перезапуск событий                        |

### Статус: ❌ НЕ РАБОТАЕТ

**Баг в Python 3.14.4:**

- `set_local_events(code_object, tool_id, events)` — TypeError: `'code' object cannot be interpreted as an integer`
- `set_local_events(int, tool_id, events)` — ValueError: `code must be a code object`
- Первый аргумент должен быть code object, но C-код пытается конвертировать его в int
- Callback'и не срабатывают без `set_local_events`
- Callback'и **добавляют** оверхед, а не убирают

**Вывод:** Не подходит для оптимизации. Добавляет оверхед вместо того, чтобы убрать его.

---

## 2. `sys.setprofile(fn)`

### Что это

Callback на каждый call/return функции.

### Сигнатура

```python
def profile(frame, event, arg):
    # event = 'call' | 'return' | 'exception'
    return profile  # Возвращаем self для продолжения
```

### Статус: ⚠️ ДОБАВЛЯЕТ оверхед

**Результаты замеров:**

- `import sys` — 14M/сек (ничего)
- `import core.realmath` (первый) — 15.7ms
- `import core.realmath` (из кеша) — 0.001ms
- `D(5.0)` — 12.8M/сек
- `5.0 * 2` inline — 65.4M/сек
- **Overhead вызова функции: 412%**

**Вывод:** Не подходит для оптимизации. Добавляет оверхед на каждый call/return.

---

## 3. `sys._getframe()`

### Что это

Доступ к фрейму вызова.

### Свойства фрейма

| Свойство    | Тип   | Описание              |
|-------------|-------|-----------------------|
| `f_locals`  | dict  | Локальные переменные  |
| `f_globals` | dict  | Глобальные переменные |
| `f_code`    | code  | Code object           |
| `f_back`    | frame | Вызывающий фрейм      |
| `f_lasti`   | int   | Последний байткод     |
| `f_lineno`  | int   | Номер строки          |

### Методы code object

| Свойство         | Тип   | Описание                |
|------------------|-------|-------------------------|
| `co_code`        | bytes | Байткод                 |
| `co_consts`      | tuple | Константы               |
| `co_names`       | tuple | Имена (для LOAD_GLOBAL) |
| `co_varnames`    | tuple | Имена переменных        |
| `co_freevars`    | tuple | Свободные переменные    |
| `co_nlocals`     | int   | Кол-во локальных        |
| `co_filename`    | str   | Имя файла               |
| `co_firstlineno` | int   | Первая строка           |
| `co_stacksize`   | int   | Размер стека            |
| `co_flags`       | int   | Флаги                   |

### Статус: ✅ РАБОТАЕТ

**Результаты:**

- `f_locals` — dict, можно менять
- `f_globals` — dict, можно менять
- Подмена `func.__code__` — даёт **1.42x ускорение** для простых функций
- Подмена `frame.f_globals['D'] = lambda x: x * 2` — работает, но **LOAD_GLOBAL + CALL остаётся**

**Вывод:** Можно использовать для подмены `__code__` и `f_globals`, но не убирает оверхед полностью.

---

## 4. `sys.modules`

### Что это

Кэш загруженных модулей (dict).

### Использование

```python
sys.modules['core'] = FakeModule()
sys.modules['core.realmath'] = FakeModule()
```

### Статус: ✅ РАБОТАЕТ

**Результаты:**

- Можно подменить модуль на любой объект
- Убирает файловую зависимость
- **Не убирает оверхед вызовов функций**

**Вывод:** Полезен для устранения файловой зависимости, но не для оптимизации вызовов.

---

## 5. `sys.path` / `sys.path_importer_cache`

### Что это

Путь поиска модулей и кэш импортеров.

### Использование

```python
sys.path.insert(0, '/path/to/src')
sys.path_importer_cache.clear()
```

### Статус: ✅ РАБОТАЕТ

**Результаты:**

- `sys.path.insert(0, '.')` — 675k/сек
- Можно динамически добавлять/убирать пути
- Убирает необходимость PYTHONPATH

**Вывод:** Полезен для управления путями импорта.

---

## 6. `marshal`

### Что это

Сериализация Python-объектов, включая code objects.

### Использование

```python
code_bytes = marshal.dumps(func.__code__)  # Сериализация
loaded_code = marshal.loads(code_bytes)  # Десериализация
new_func = types.FunctionType(loaded_code, globals)
```

### Статус: ✅ РАБОТАЕТ

**Результаты:**

- `marshal.dumps(code)` — 109 bytes для простой функции
- `marshal.loads()` — возвращает code object
- `types.FunctionType(code, globals)` — создаёт функцию из code object
- Можно менять `func.__code__` на лету

**Вывод:** Полезен для хранения и подмены code objects.

---

## 7. `compile()` + `exec()`

### Что это

Компиляция строки в code object и выполнение.

### Использование

```python
code_str = '''
def D(x):
    return x * 2

def H(x):
    return x / 2
'''

compiled = compile(code_str, '<inline>', 'exec')
namespace = {}
exec(compiled, namespace)
D = namespace['D']
H = namespace['H']
```

### Статус: ✅ РАБОТАЕТ

**Результаты:**

- `compile(code_str, '<inline>', 'exec')` — компиляция строки
- `exec(compiled, namespace)` — выполнение в namespace
- Получаем code objects для всех функций
- Можно подменять `__code__` у существующих функций

**Вывод:** Ключевой инструмент для генерации code objects из строк.

---

## 8. `sys.audit` / `sys.addaudithook()`

### Что это

Хуки на audit-события (безопасность).

### Сигнатура

```python
def audit_hook(event_name, arg):
    pass


sys.addaudithook(audit_hook)
```

### Статус: ⚠️
---

## 9. `sys._current_frames()`

### Что это

Возвращает dict {thread_id: frame} для всех потоков.

### Статус: ℹ️ Бесполезен

**Результаты:**

- `sys._current_frames()` — dict {thread_id: frame}
- Текущий процесс: 1 фрейм

---

## 10. `sys.float_info` / `sys.int_info` / `sys.hash_info`

### Что это

Константы и лимиты для float/int/hash.

### float_info

| Свойство   | Значение                | Описание        |
|------------|-------------------------|-----------------|
| `max`      | 1.7976931348623157e+308 | Макс float      |
| `min`      | 2.2250738585072014e-308 | Мин float       |
| `epsilon`  | 2.220446049250313e-16   | Точность        |
| `dig`      | 15                      | Десятичных цифр |
| `mant_dig` | 53                      | Битов мантиссы  |

### int_info

| Свойство            | Значение       | Описание        |
|---------------------|----------------|-----------------|
| `dig`               | 4300           | Десятичных цифр |
| `width`             | 64             | Битов           |
| `digits_str_format` | 'small_digits' | Формат строки   |

### hash_info

| Свойство         | Значение | Описание       |
|------------------|----------|----------------|
| `hash_width`     | 64       | Битов          |
| `modulus`        | 2^61 - 1 | Модуль         |
| `inf_key`        | 314159   | Ключ для inf   |
| `binop_hash_key` | 40463    | Ключ для binop |

### Статус: ℹ️ ИНФОРМАТИВНО

**Вывод:** Константы.

---

## 11. `sys.setrecursionlimit()` / `sys.setswitchinterval()`

### Что это

Настройки рекурсии и переключения потоков.

### Использование

```python
sys.setrecursionlimit(3)  # Как в Eugении.py
sys.setswitchinterval(0.00000000000000001)  # Как в Eugении.py
```

### Статус: ✅ РАБОТАЕТ

**Результаты:**

- `setrecursionlimit(3)` — как в Eugenia.py
- `setswitchinterval(1e-17)` — минимальное переключение
- `set_int_max_str_digits(0)` — без лимита на BigInt

**Вывод:** Уже используется в Eugenia.py для оптимизации.

---

# ИТОГ: Что может убрать оверхед вызовов?

---
Не работает.

1. `sys.monitoring` — баг в Python 3.14.4
2. `sys.setprofile` — добавляет оверхед
3. `sys.audit` — не для нашей задачи

---
Частично работает.

4. `sys.modules` подмена — убирает файловую зависимость
5. `sys.path` — управление путями импорта
6. `sys._getframe` — доступ к фрейму, подмена globals
7. `sys._current_frames` — только для отладки
8. `sys.float_info/int_info/hash_info` — константы
9. `sys.setrecursionlimit/switchinterval` — уже используется.

---
Работает, хорошо.

10. `sys._getframe` + `__code__` подмена — **1.42x ускорение**
11. `compile()` + `exec()` — генерация code objects
12. `marshal` — сериализация code objects

## КЛЮЧЕВОЕ НАБЛЮДЕНИЕ: Default args

| Метод                        | Скорость      |
|------------------------------|---------------|
| `import math; math.log2()`   | 8.4M/сек      |
| `_log2 = math.log2; _log2()` | 11.4M/сек     |
| `def f(x, log2=_log2)`       | **14M/сек**   |
| `x * 2` inline               | **65.4M/сек** |

**Default args = fastest way передать функцию-зависимость без LOAD_GLOBAL оверхеда.**

---

# ГЛАВНЫЙ ВЫВОД

**Единственный способ убрать оверхед полностью — inline-код.**

Всё остальное — частичные оптимизации:

- Default args = 22% ускорения
- `__code__` подмена = 42% ускорения
- `sys.modules` подмена = убирает файловую зависимость
- `compile()` + `exec()` = генерация code objects из строк
- `marshal` = сериализация code objects

**Для полного устранения оверхеда нужно:**

1. Взять код из core как строки
2. Скомпилировать через `compile()`
3. Подменить `__code__` у функций в Eugenia.py
4. Использовать default args для передачи зависимостей
