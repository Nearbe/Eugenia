# Implementation Plan: Formatter

## Phase 1: Анализ текущего Formatter

### Tasks
- [ ] Task: Прочитать DESIGN.md и pyproject.toml проекта Formatter
    - [ ] Изучить текущую архитектуру cosmic_formatter
    - [ ] Понять что уже реализовано
    - [ ] Определить gaps между текущим состоянием и spec
- [ ] Task: Проанализировать код `cosmic_formatter/core.py` и `sections.py`
    - [ ] Понять текущие трансформации
    - [ ] Определить какие правила уже есть
    - [ ] Определить какие правила отсутствуют
- [ ] Task: Проанализировать примеры кода из `src/` для определения паттернов inline-формата
    - [ ] Выделить типичные паттерны кода Eugenia
    - [ ] Определить какие трансформации нужны для inline-формата
    - [ ] Задокументировать паттерны

## Phase 2: Проектирование правил трансформации

### Tasks
- [ ] Task: Определить набор правил inline-формата
    - [ ] Правила для функций (inline vs extract)
    - [ ] Правила для классов
    - [ ] Правила для импортов
    - [ ] Правила для docstrings
- [ ] Task: Определить нейминг-конвенции для инструментов Formatter
    - [ ] Каталог инструментов с именами
    - [ ] Семантика каждого инструмента
    - [ ] Детерминированные правила выбора инструмента
- [ ] Task: Спроектировать API Formatter
    - [ ] CLI интерфейс
    - [ ] Programmatic API
    - [ ] Конфигурация

## Phase 3: Реализация ядра Formatter

### Tasks
- [ ] Task: Реализовать базовый парсер AST
    - [ ] Чтение Python-файлов
    - [ ] Построение AST
    - [ ] Обход AST
- [ ] Task: Реализовать правила трансформации (Phase 2 output)
    - [ ] Inline-функции
    - [ ] Inline-классы
    - [ ] Inline-импорты
    - [ ] Inline-docstrings
- [ ] Task: Реализовать генератор выходного кода
    - [ ] AST → source code
    - [ ] Сохранение семантики
    - [ ] Сохранение структуры

## Phase 4: Интеграция и тестирование

### Tasks
- [ ] Task: Протестировать на кодовой базе Eugenia
    - [ ] Запустить на `src/core/`
    - [ ] Запустить на `src/nucleus/`
    - [ ] Запустить на `src/renderers/`
- [ ] Task: Исправить обнаруженные проблемы
    - [ ] Анализ diff
    - [ ] Корректировка правил
    - [ ] Повторное тестирование
- [ ] Task: Добавить документацию
    - [ ] Обновить DESIGN.md
    - [ ] Добавить примеры использования
    - [ ] Добавить CLI help

## Phase Completion Verification and Checkpointing Protocol

**Trigger:** This protocol is executed immediately after a task is completed that also concludes a phase in `plan.md`.

1.  **Announce Protocol Start:** Inform the user that the phase is complete and the verification and checkpointing protocol has begun.

2.  **Verify Formatter Compliance:** Run the project's custom `Formatter` on all changed files.

3.  **Verify Linting & Typing:** Run `ruff check .` and `mypy src/` on changed files.

4.  **Propose a Detailed, Actionable Manual Verification Plan:**
    -   Analyze `product.md`, `product-guidelines.md`, and `plan.md` to determine the user-facing goals of the completed phase.
    -   Generate a step-by-step plan with expected outcomes.

5.  **Await Explicit User Feedback:**
    -   Ask: "**Does this meet your expectations? Please confirm with yes or provide feedback.**"
    -   **PAUSE** and await the user's response.

6.  **Create Checkpoint Commit:** Stage all changes and commit with message `conductor(checkpoint): Checkpoint end of Phase X`.

7.  **Attach Auditable Verification Report using Git Notes.**

8.  **Get and Record Phase Checkpoint SHA:** Append `[checkpoint: <sha>]` to the phase heading in `plan.md`.

9.  **Commit Plan Update** with message `conductor(plan): Mark phase '<PHASE NAME>' as complete`.

10.  **Announce Completion.**
