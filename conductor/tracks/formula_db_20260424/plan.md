# Implementation Plan: formula_db_20260424

## Phase 1: Foundation — SQLite Schema & Registry

- [ ] Task: Создать структуру SQLite-базы данных (formulas, formula_dependencies, test_cases, verification_results)
- [ ] Task: Реализовать registry.py — CRUD операции для формул и констант
- [ ] Task: Добавить миграцию начальных данных из formulas_registry.yaml в SQLite
    - [ ] Subtask: Прочитать существующий formulas_registry.yaml
    - [ ] Subtask: Создать migration-скрипт для переноса в SQLite
    - [ ] Subtask: Протестировать миграцию
- [ ] Task: Реализовать dedup.py — проверку дубликатов по (id, source_file)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Foundation' (Protocol in workflow.md)

## Phase 2: Calculator Backend (STRICT — Project Math Only)

- [ ] Task: Создать calculator.py — абстрактный вычислительный бэкенд
- [ ] Task: Реализовать project_math.py — интеграция с src/core
    - [ ] Subtask: Определить API для вызова математики проекта
    - [ ] Subtask: Реализовать базовые операции: +, -, *, /, ^, ln, exp, sqrt, sin, cos
    - [ ] Subtask: Реализовать константы проекта (π, e, c, h, и т.д.)
- [ ] Task: Реализовать строгий режим — ошибка при попытке использовать numpy/sympy/scipy
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Calculator Backend' (Protocol in workflow.md)

## Phase 3: Validator — Syntax + Computation

- [ ] Task: Создать validator.py — синтаксическая проверка формул
    - [ ] Subtask: Парсинг выражений (без sympy — собственный парсер)
    - [ ] Subtask: Валидация структуры формулы
- [ ] Task: Реализовать вычислительную проверку
    - [ ] Subtask: Вычисление через calculator backend
    - [ ] Subtask: Сравнение expected_value с computed_value
    - [ ] Subtask: Расчёт расхождения в процентах
- [ ] Task: Реализовать проверку констант (type=constant)
    - [ ] Subtask: Расхождение ≤ 13% → confirmed
    - [ ] Subtask: Расхождение > 13% → flagged (requires fix)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Validator' (Protocol in workflow.md)

## Phase 4: Interactive Workflow — Constants First

- [ ] Task: Создать interactive.py — интерактивный процесс обработки файлов
- [ ] Task: Реализовать загрузку `Universe/Физические_константы.md`
    - [ ] Subtask: Парсинг таблицы CODATA 2022 (Quantity, Value, Uncertainty, Unit)
    - [ ] Subtask: Создание ~180 записей типа `constant`
    - [ ] Subtask: Запись в SQLite
- [ ] Task: Удалить `Universe/Физические_константы.md` после занесения
- [ ] Task: Реализовать прогресс-бар для обработки файлов
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Interactive Workflow' (Protocol in workflow.md)

## Phase 5: Interactive Workflow — Physics Iteration

- [ ] Task: Реализовать итеративную обработку `Physics/`
    - [ ] Subtask: Обход всех файлов в `Physics/Формулы/` и поддиректориях
    - [ ] Subtask: Открытие файла → показ формул → размещение в БД → отчёт
- [ ] Task: Реализовать дедупликацию каждые 2-3 файла
    - [ ] Subtask: Проверка на дубликаты по (id, source_file)
    - [ ] Subtask: Вывод отчёта о найденных дубликатах
- [ ] Task: Обработка формул из `Physics/` поддиректорий (03_Параметр_Δ, 04_Синхронизация, и т.д.)
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Physics Iteration' (Protocol in workflow.md)

## Phase 6: DAG Dependencies & Results

- [ ] Task: Реализовать автоматический резольвинг зависимостей через DAG
    - [ ] Subtask: Топологическая сортировка формул
    - [ ] Subtask: Выполнение в правильном порядке
- [ ] Task: Реализовать хранение результатов проверки в verification_results
- [ ] Task: Вывод итоговой сводки: сколько подтверждено, сколько опровергнуто, среднее расхождение
- [ ] Task: Conductor - User Manual Verification 'Phase 6: DAG & Results' (Protocol in workflow.md)

## Phase 7: Cleanup & Commit

- [ ] Task: Удалить `Tester/formulas_registry.yaml`
- [ ] Task: Удалить `Tester/Tester.ipynb`
- [ ] Task: Финальная проверка: Formatter, ruff, mypy
- [ ] Task: Коммит всех изменений
- [ ] Task: Conductor - User Manual Verification 'Phase 7: Cleanup' (Protocol in workflow.md)
