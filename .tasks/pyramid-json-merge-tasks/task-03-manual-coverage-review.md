# Task 03: Ручная проверка полноты

**Type:** Verification
**Suggested agent:** Review

## Goal
Пройти по таблице уникальных блоков из `research/findings.md` и явно убедиться, что в `pyramid_merged.json` присутствует каждый из них. Зафиксировать результат в `coverage_report.md` с точным путём в merged для каждого блока.

## Why This Task Exists
Автоматический валидатор (Task 04) проверит форму и алиасы, но не сможет убедиться, что сохранена семантика каждого уникального раздела. Это делает человеко-читаемый ревью-проход по ключевым разделам.

## Spec Coverage
- Requirements: R2
- Scenarios: S2, S4

## Required Inputs
- `.tasks/pyramid-json-merge-tasks/research/findings.md` — эталонная карта уникальных блоков (раздел «Cross-file Comparison → Карта», раздел «Ключи/разделы, присутствующие только в части файлов», таблица инвариантного ядра).
- `.tasks/pyramid-json-merge-tasks/schema.md` — canonical layout, по которому искать пути в merged.
- `pyramid_merged.json` в к��рне проекта — итог Task 02, read-only.

## Files/Areas
- `.tasks/pyramid-json-merge-tasks/coverage_report.md` — **создать** отчёт.
- `pyramid_merged.json` — только читать.
- Исходные `pyramid*.json` — можно читать для сверки содержимого, если возникают сомнения.

## Constraints / Non-Goals
- Не модифицировать `pyramid_merged.json` и не менять скрипт сборки.
- Не дублировать проверки автоматического валидатора (Task 04).
- Не переписывать содержимое блоков, только фиксировать их наличие и путь.

## Output Artifacts
- `.tasks/pyramid-json-merge-tasks/coverage_report.md` с двумя обязательными таблицами:
  1. **Unique blocks coverage** — колонки: `source_file`, `original_path`, `merged_path`, `present (yes/no)`, `notes`. Минимум 20 строк по всем уникальным блокам из R2.
  2. **Invariant core check** — колонки: `item`, `merged_path`, `value_matches_core`, `notes`. Покрывает: grid Ло Шу, сумма/константа матрицы, стороны S/E/W/N (digits/sum/product/operator), цикл `0→…→0`, проценты 5/27/68, m_p=938.272, R²>0.99 на 83 LHCb, 210 ступеней, координаты 29.9792°N/31.1342°E.

## What to Do
- Прочитать `pyramid_merged.json` целиком.
- Для каждой строки из «Unique blocks coverage» найти блок в merged и указать его путь (например, `OneLaw.biophotonics`, `OneLaw.particles.groups.mesons_Q2`).
- Для каждой строки «Invariant core check» убедиться, что значение присутствует и совпадает с findings.md; занести путь и пометку о дубликатах, если нашлись.
- Если какой-то блок отсутствует или значение расходится — занести `present: no` + краткое описание расхождения, и в конце отчёта сделать раздел «Gaps to fix» со списком проблем.
- Если всё покрыто — в конце отчёта явно написать «All unique blocks present, invariant core is singular and consistent.»

## Expected Output
- Файл `coverage_report.md` с двумя таблицами и финальным вердиктом (OK / список Gaps).
- Короткий summary в отчёте агента: сколько блоков проверено, сколько пропусков найдено.

## Acceptance Criteria
- [ ] `coverage_report.md` содержит обе обязательные таблицы.
- [ ] Unique blocks coverage покрывает все блоки из R2 (минимум 20 строк).
- [ ] Invariant core check покрывает минимум 9 пунктов инвариантного ядра.
- [ ] Для каждого присутствующего блока указан конкретный путь в merged.
- [ ] Найденные пропуски/расхождения перечислены в «Gaps to fix» с ссылками на путь и на источник в findings.md.
- [ ] Covered requirements and scenarios are satisfied (R2, S2, S4).
- [ ] I've created a git commit for this task *(см. примечание о git-стратегии в конце PLAN.md)*.
