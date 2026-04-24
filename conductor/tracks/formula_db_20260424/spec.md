# Specification: Formula Database (formula_db_20260424)

## 1. Overview

Создание системы хранения и тестирования всех формул проекта Eugenia. **Интерактивный процесс**: сначала заносим физические константы из `Universe/Физические_константы.md` (CODATA 2022, ~180 записей) — эти константы **нужно подтвердить или опровергнуть** через математику проекта. После занесения файл **удаляется**. Затем итеративно обрабатываем каждый файл из `Physics/` (104+ файлов в `Physics/Формулы/` и поддиректориях). Дедупликация каждые 2-3 файла. Тестирование: комбинация синтаксической и вычислительной проверки. **Только собственная математика проекта** (`src/core`) — никаких numpy/sympy/scipy.

## 2. Functional Requirements

### 2.1 Formula Registry (SQLite)
- **FR-1:** SQLite-база данных с таблицами: `formulas`, `formula_dependencies`, `test_cases`, `verification_results`
- **FR-2:** Каждая запись: `id`, `name`, `type` (math/physics/constant/arbitrary), `expression`, `inputs`, `params`, `expected_value`, `expected_tolerance`, `source_file`, `category`, `extracted_at`
- **FR-3:** Тип `constant` — физические константы CODATA. **Цель: подтвердить или опровергнуть** через вычисление собственной математикой проекта.
- **FR-4:** Уникальность по `(id, source_file)` — дедупликация на уровне БД
- **FR-5:** Автоматический резольвинг зависимостей через DAG (topological sort)

### 2.2 Interactive Workflow
- **FR-6:** **Шаг 1:** Занести `Universe/Физические_константы.md` — ~180 записей CODATA 2022. Каждая константа — гипотеза, которую нужно проверить математикой.
- **FR-7:** **После занесения: удалить `Universe/Физические_константы.md`** — данные уже в БД.
- **FR-8:** **Шаг 2:** Итеративная обработка файлов `Physics/` (104+ файлов)
- **FR-9:** Дедупликация каждые 2-3 файла: проверка на дубликаты, вывод отчёта
- **FR-10:** Каждый файл: открыть → показать формулы → разместить в БД → отчёт
- **FR-11:** Прогресс-бар: сколько файлов обработано, сколько формул извлечено

### 2.3 Formula Testing
- **FR-12:** Синтаксическая проверка: парсинг выражения, валидация структуры формулы
- **FR-13:** Вычислительная проверка: вычисление с тестовыми данными, сравнение с `expected_value` в пределах `expected_tolerance`
- **FR-14:** Для `type=constant`: вычисление собственной математикой → сравнение с CODATA → результат: **подтверждено / опровергнуто**
- **FR-15:** **Целевой порог:** все константы должны сходиться с точностью **лучше 13%**
- **FR-16:** Автоматическая обработка зависимостей (резольвинг через DAG)

### 2.4 Core Module
- **FR-17:** `Tester/formula_db/` — основной модуль
- **FR-18:** `registry.py` — SQLite registry
- **FR-19:** `calculator.py` — abstract calculator backend
- **FR-20:** `project_math.py` — integration with src/core (STRICT, no fallback)
- **FR-21:** `validator.py` — syntax + computation validation
- **FR-22:** `interactive.py` — интерактивный процесс обработки файлов

### 2.5 Integration with Project Math (STRICT)
- **FR-23:** Использовать **только** собственную математику проекта (`src/core`) как вычислительный бэкенд
- **FR-24:** **Никакого fallback** на numpy/sympy/scipy
- **FR-25:** Если выражение нельзя вычислить своей математикой — ошибка с указанием пробела

## 3. Non-Functional Requirements
- **NFR-1:** Все вычисления детерминированы (GIL = преимущество)
- **NFR-2:** Поддержка mypy strict mode
- **NFR-3:** Код проходит ruff linting
- **NFR-4:** Документирование всех публичных функций (docstrings)
- **NFR-5:** Старые файлы `Tester/formulas_registry.yaml` и `Tester/Tester.ipynb` удаляются
- **NFR-6:** После занесения `Universe/Физические_константы.md` — удалить

## 4. Acceptance Criteria
1. ✅ База данных формул создана
2. ✅ Физические константы из `Universe/Физические_константы.md` занесены (~180 записей) как гипотезы для проверки
3. ✅ `Universe/Физические_константы.md` удалён после занесения
4. ✅ Итеративная обработка `Physics/` работает
5. ✅ Дедупликация каждые 2-3 файла работает
6. ✅ Для констант: расхождение с CODATA ≤ 13% — подтверждена, > 13% — требует исправления
7. ✅ Зависимости между формулами автоматически резольвятся
8. ✅ Только собственная математика проекта используется
9. ✅ Код проходит Formatter, ruff, mypy
10. ✅ Старые файлы Tester/ удалены

## 5. Out of Scope
- CLI-интерфейс (только интерактивный процесс)
- Автоматический парсинг формул из Markdown
- Визуализация формул
- Веб-интерфейс
- Тесты на тесты (тесты на модули)

## 6. Project Structure
```
Tester/
├── formula_db/               # Основной модуль
│   ├── __init__.py
│   ├── registry.py           # SQLite registry
│   ├── calculator.py         # Abstract calculator backend
│   ├── project_math.py       # Integration with src/core (STRICT)
│   ├── validator.py          # Syntax + computation validation
│   └── interactive.py        # Interactive file processing workflow
├── formula_db.db             # SQLite database
└── formulas_registry.yaml    # УДАЛИТЬ
└── Tester.ipynb              # УДАЛИТЬ
```
