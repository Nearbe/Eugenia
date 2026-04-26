# Task 04: Автоматическая валидация merged

**Type:** Verification
**Suggested agent:** Code

## Goal
Реализовать скрипт-валидатор `validate_merged.py` в `.tasks/pyramid-json-merge-tasks/`, который машинно проверяет: (а) JSON-валидность merged, (б) обе шкалы Q_neuro, (в) форму конфликтных узлов, (г) отсутствие старых алиасов, (д) дезамбигуацию поля `Q`. Цель — чтобы регрессии ловились автоматически без ручного чтения.

## Why This Task Exists
Task 03 проверяет семантическую полноту, но не форму. Нам нужна детерминированная гарантия, что схема из Task 01 действительно применена в Task 02.

## Spec Coverage
- Requirements: R3, R6, R7
- Scenarios: S1, S3

## Required Inputs
- `.tasks/pyramid-json-merge-tasks/schema.md` — canonical names, alias dictionary, conflict-node shapes, Q-disambiguation rules.
- `pyramid_merged.json` в корне проекта — read-only.
- Канонические пути для проверок (выдержка из schema.md):
  - `OneLaw.axioms_and_operators.Q_neuro.scales.direct` и `.symmetric`;
  - `OneLaw.physical_constants.alpha_inverse` (value, approximation, derivation, _source);
  - `OneLaw.resonances.schumann_fundamental` (value_Hz, approximation_Hz, formula, _source);
  - `OneLaw.meta.sources` (массив длиной 4 с filename, root_key, version, derivation_base, status).

## Files/Areas
- `.tasks/pyramid-json-merge-tasks/validate_merged.py` — **создать**.
- `pyramid_merged.json` — только читать.
- Никаких правок в `src/` и рантайме.

## Constraints / Non-Goals
- Python 3.14, stdlib only (`json`, `pathlib`, `sys`, `re`).
- Никаких сетевых вызовов.
- Скрипт должен иметь ненулевой exit code при провале хотя бы одной проверки; подробные сообщения — в stdout.
- Не дублирует семантический review Task 03.

## Output Artifacts
- `.tasks/pyramid-json-merge-tasks/validate_merged.py` со следующими проверками (каждая — отдельная функция):
  1. `check_json_valid(path)` — `json.load` без исключений (R1, S1).
  2. `check_root_key(data)` — есть единственный корневой ключ `OneLaw`.
  3. `check_meta_sources(data)` — `OneLaw.meta.sources` — массив из 4 объектов, у каждого присутствуют `filename`, `root_key`.
  4. `check_q_neuro_scales(data)` — `OneLaw.axioms_and_operators.Q_neuro.scales` содержит `direct` (base_frequency_Hz=1.25) и `symmetric` (base_frequency_Hz=2.5); у обоих есть `formula`, `mapping`, `_source` (S3, R4).
  5. `check_alpha_inverse(data)` — `value == 137.035999084`, `approximation == 137`, `derivation` задано, `_source` непустой (R5).
  6. `check_schumann(data)` — поле `schumann_fundamental` имеет `value_Hz` типа number, `formula` типа string, присутствует `_source` (R5).
  7. `check_no_legacy_aliases(data)` — рекурсивный обход дерева; ни в одном узле не встречаются ключи из чёрного списка:
     - `op`, `center_value`, `coffer_resonance`, `Schumann_base`, `matrix_3x3`, `Hubble_parameter` (или противоположное — фиксируется в schema.md и зеркалируется здесь).
  8. `check_q_disambiguation(data)` — обход дерева; в контекстах, где встречается голое поле `Q`, должна быть разметка `Q_hadron`/`Q_neuro`. Допустимые исключения (задокументировать в коде): mapping-ключи вида `Q0..Q10` — они остаются как есть.
  9. `check_source_field_on_conflicts(data)` — у `alpha_inverse`, `schumann_fundamental`, обеих шкал `Q_neuro`, у `particles`, `planck_units`, `EEG_rhythms`, `biophotonics`, `pyramid_mathematics` присутствует `_source`.
- `main()` запускает все проверки, собирает результаты, печатает `PASS/FAIL: <check_name>: <detail>`, возвращает exit code 0 при всех PASS, 1 иначе.

## What to Do
1. Реализовать скрипт с перечисленными функциями.
2. Запустить `python3 .tasks/pyramid-json-merge-tasks/validate_merged.py`.
3. Убедиться, что все проверки PASS. Если какая-то FAIL — это сигнал вернуться к Task 02 и починить форму.
4. Вывод валидатора (конкретные строки PASS/FAIL) зафиксировать либо в `validation_log.md` рядом с валидатором, либо процитировать в отчёте агента.

## Expected Output
- `validate_merged.py` создан.
- Все 9 проверок возвращают PASS.
- Цитата реального stdout валидатора в отчёте агента.

## Acceptance Criteria
- [ ] Скрипт `validate_merged.py` создан.
- [ ] Запуск `python3 .tasks/pyramid-json-merge-tasks/validate_merged.py` завершается с exit code 0.
- [ ] Все 9 перечисленных проверок выводят PASS.
- [ ] Реальный stdout (минимум первые строки PASS и финальное резюме) процитирован в отчёте.
- [ ] Covered requirements and scenarios are satisfied (R3, R6, R7, S1, S3).
- [ ] I've created a git commit for this task *(см. примечание о git-стратегии в конце PLAN.md)*.
