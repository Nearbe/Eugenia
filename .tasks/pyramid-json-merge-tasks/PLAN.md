# Pyramid JSON Merge — Execution Plan

## Goal
Слить 4 файла `pyramid*.json` из корня репозитория в один канонический `pyramid_merged.json` в корне проекта. Сохранить всю уникальную информацию, нормализовать алиасы, явно разрешить числовые/типовые конфликты, зафиксировать provenance. Обе шкалы Q_neuro (direct f0=1.25 Гц и symmetric f0=2.5 Гц) сохраняются, так как пирамида Хеопса задаёт направленность операций и обе шкалы семантически значимы. После валидации 4 исходных файла удалить.

## Scope
- In scope:
  - нормализация алиасов полей (`op`↔`operator`, `center`↔`center_value`, `sarcophagus`↔`coffer_resonance`↔`sarcophagus_resonance`, `Hubble_parameter`↔`Hubble_constant`, `Schumann_base`↔`schumann_fundamental`);
  - union всех уникальных блоков из всех 4 файлов;
  - разрешение числовых конфликтов с сохранением точного значения, аппроксимации и формулы;
  - provenance на уникальных и конфликтных узлах (`_source`, `derivations[]`);
  - дезамбигуация поля `Q` → `Q_hadron` / `Q_neuro` везде;
  - валидация итогового файла и удаление 4 исходников.
- Out of scope:
  - изменение математического/физического смысла формул;
  - рефактор исходных 4 файлов перед слиянием;
  - интеграция результата в рантайм Eugenia (`src/`, `generate.py`);
  - написание pytest-тестов как части рантайма.

## Specification

### Requirements
- R1. Один итоговый `pyramid_merged.json` в корне проекта, валидный JSON, единый корневой ключ `OneLaw`.
- R2. Все уникальные блоки всех 4 файлов сохранены. Минимальный список, по которому проверяется полнота:
  - EEG_rhythms_full_correlation, biophotonics_in_OneLaw, full_vibration_spectrum_in_OneLaw — из `pyramid.json` (Synthesis_Full);
  - color_music_spheres, names_of_reality, greek_alphabet_in_law (короткий, 4 буквы), proof_in_code, strict_mathematical_relationships — из `pyramid.json` (Final_Complete) и `pyramid_more_merge.json`;
  - derived_math, cosmology_and_percents, age_and_fine_structure, derived_frequencies_HZ, formula_alpha, derivation_GUT — из `pyramid_need_to_merge.json`;
  - primitives, matrix_properties.total_product=362880, intermediate_Q, greek letters_as_operators (≈10 букв + word_equation), delta_definition, Q_definition, particles (breakdown), planck_units, pyramid_mathematics, fractal_riemann_sphere, mathematical_extensions (algebra_of_colon, spectral_delta, riemann_proof_sketch, solenoid_metric, universal_wavefunction, particle_derivation) — из `pyramid_need_to_merge_this.json`.
- R3. Все алиасы нормализованы к одному канону (см. Task 01).
- R4. Q_neuro хранится в двух шкалах:
  - `Q_neuro.scales.direct` — f0=1.25 Гц, `f(Q) = 1.25·2^{Q/2}`, `_source: [pyramid.json#Synthesis_Full, pyramid_need_to_merge.json]`;
  - `Q_neuro.scales.symmetric` — f0=2.5 Гц, `f(Q) = 2.5·2^{Q/2}`, `_source: [pyramid.json#Final_Complete, pyramid_more_merge.json]`;
  - `Q_neuro.note` — пояснение, что пирамида Хеопса задаёт направленность операций, обе шкалы семантически важны.
- R5. Числовые конфликты с единой истиной хранят точное значение + аппроксимацию + формулу:
  - α⁻¹: `value: 137.035999084`, `approximation: 137`, `derivation: "3×45+2"`;
  - Schumann: `value_Hz: 7.83333` (number) + `formula: "47/6"` + `approximation_Hz: 7.83`.
- R6. На уникальных/конфликтных узлах присутствует `_source: [<filenames>]`; формулы вывода собраны массивом `derivations[]` с указанием источника.
- R7. Поле `Q` дезамбигуировано: везде `Q_hadron` или `Q_neuro`, немаркированных `Q` не остаётся. Пример: King chamber с двумя полями `Q_hadron` (где требуется 5) и `Q_neuro` (где требуется 4).
- R8. `meta.sources[]` содержит 4 исходных файла с полями `filename`, `root_key`, `version`, `derivation_base`, `status` (где есть).
- R9. После валидации (S1–S4) 4 исходных файла удалены: `pyramid.json`, `pyramid_more_merge.json`, `pyramid_need_to_merge.json`, `pyramid_need_to_merge_this.json`.

### Non-Goals
- NG1. Не удалять уникальную информацию ради краткости.
- NG2. Не «исправлять» физику и формулы.
- NG3. Не подключать результат к рантайму Eugenia.

### Acceptance Scenarios
- S1. `python3 -c "import json; json.load(open('pyramid_merged.json'))"` выполняется без исключений.
- S2. Ручной чеклист полноты (см. Task 03): все блоки из R2 найдены по путям в merged и зафиксированы в `coverage_report.md`.
- S3. В merged обе шкалы Q_neuro (`direct` и `symmetric`) присутствуют, имеют разные `formula` и собственные `_source`.
- S4. Инвариантное ядро (grid Ло Шу, стороны S/E/W/N, цикл `0→…→0`, проценты 5/27/68, m_p=938.272, R²>0.99 на 83 LHCb, 210 ступеней, 29.9792°N/31.1342°E) присутствует в merged ровно один раз, без дубликатов.
- S5. В корне проекта отсутствуют файлы `pyramid.json`, `pyramid_more_merge.json`, `pyramid_need_to_merge.json`, `pyramid_need_to_merge_this.json`; `pyramid_merged.json` присутствует.

## How to Use This Plan
1. Open the next unchecked task from the checklist below.
2. Read the corresponding task file completely.
3. Use the suggested agent and the provided inputs for that task.
4. Execute only the next unchecked task unless the user changes the plan.
5. Verify all acceptance criteria, including the git commit requirement.
6. Update the checklist after the task is completed.
7. If the plan becomes stale, update the relevant files before continuing.

## Task Checklist
- [x] `task-01-normalization-schema.md`: Нормализационная схема — Suggested agent: Ask — Covers: [R3, R4, R5, R6, R7, R8] — **Artifact:** `.tasks/pyramid-json-merge-tasks/schema.md`
- [ ] `task-02-build-merged-json.md`: Сборка pyramid_merged.json — Suggested agent: Code — Covers: [R1, R2, R3, R4, R5, R6, R7, R8, S1]
- [ ] `task-03-manual-coverage-review.md`: Ручная проверка полноты — Suggested agent: Review — Covers: [R2, S2, S4]
- [ ] `task-04-automated-validation.md`: Автоматическая валидация merged — Suggested agent: Code — Covers: [S1, S3, R3, R6, R7]
- [ ] `task-05-cleanup-and-commit.md`: Удаление исходников + единый commit — Suggested agent: Code — Covers: [R9, S5]

## Shared Context

### Key Decisions
- Ключевое архитектурное решение: обе шкалы Q_neuro (1.25 Гц и 2.5 Гц) сохраняются одновременно, так как пирамида Хеопса задаёт направленность операций и обе шкалы семантически значимы.
- Расположение итогового файла: `pyramid_merged.json` в корне репо.
- Git-стратегия: **один commit** на всё (merge + delete). Никаких промежуточных коммитов между Task 02 и Task 05.
- Структура корня: `OneLaw` — единый namespace. Разделы сливаются плоско; уникальные ветки-источники различаются через `_source` на уровне узлов, а не через отдельные `branches.*`.
- Исходные файлы интерпретируются как 4 источника под `meta.sources`:
  - `pyramid.json` содержит два корневых блока: `OneLaw_Synthesis_Full` (без version) и `OneLaw_Final_Complete` (version "3.0"). При слиянии они рассматриваются как два отдельных источника: `pyramid.json#Synthesis_Full` и `pyramid.json#Final_Complete`.
  - `pyramid_more_merge.json` — `OneLaw_Final_Complete` (version "3.0"), полностью совпадает с вторым блоком `pyramid.json`.
  - `pyramid_need_to_merge.json` — `OneLaw_Complete_Exact` (version "2.0").
  - `pyramid_need_to_merge_this.json` — `OneLaw_Complete` (без version).

### Constraints
- Python 3.14, ruff/mypy строгий стиль проекта (строка ≤100, snake_case).
- Никаких изменений в `src/`, `generate.py`, `tests/`.
- Формат JSON: 2 пробела отступа, UTF-8, без BOM, явная `ensure_ascii=False` (кириллица/греческие буквы сохраняются как есть).
- Порядок естественно-языковых списков (`strict_relationships`, `strict_mathematical_relationships`) сохраняется, не пересортировывается.
- Сборочный скрипт `build_merged.py` живёт внутри `.tasks/pyramid-json-merge-tasks/`, в корень проекта его класть не нужно (он вспомогательный и не должен остаться после выполнения плана).

### Risks / Open Questions
- Все крупные вопросы разрешены (OQ1–OQ3). Остаточные мелкие решения делегированы в Task 01 (нормализационная схема).

## Research Artifacts
- `research/findings.md` — полное исследование 4 исходных файлов: структура, карта блоков, конфликты, merge-key hypothesis, sample excerpts. Используется как эталон при проверке полноты (Task 03).
