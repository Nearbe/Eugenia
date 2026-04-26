# Task 01: Нормализационная схема

**Type:** Exploration
**Suggested agent:** Ask

## Goal
Зафиксировать словарь алиасов, политику provenance и формальную JSON-схему `OneLaw` (верхнеуровневый контур + правила для конфликтных узлов). Результат — документ `schema.md`, на который опираются Task 02 и Task 04.

## Why This Task Exists
Чтобы Task 02 строил merged детерминированно, а Task 04 мог автоматически валидировать результат, нужен явный, письменный контракт: какие имена канонические, какие — алиасы, как выглядит узел с конфликтом, где и как писать `_source` и `derivations`. Без этого слияние превратится в гадание.

## Spec Coverage
- Requirements: R3, R4, R5, R6, R7, R8

## Required Inputs
- `.tasks/pyramid-json-merge-tasks/research/findings.md` — полное исследование всех 4 файлов, включая:
  - карту блоков (раздел «Cross-file Comparison → Карта»);
  - инвариантное ядро;
  - список уникальных разделов по файлам;
  - перечисление 11 конфликтных точек в «Risks & Open Questions»;
  - sample excerpts.
- Исходные файлы в корне проекта (read-only):
  - `pyramid.json` (OneLaw_Synthesis_Full + OneLaw_Final_Complete v3.0)
  - `pyramid_more_merge.json` (OneLaw_Final_Complete v3.0)
  - `pyramid_need_to_merge.json` (OneLaw_Complete_Exact v2.0)
  - `pyramid_need_to_merge_this.json` (OneLaw_Complete, без version)

## Files/Areas
- `.tasks/pyramid-json-merge-tasks/schema.md` — **создать** документ схемы.
- `.tasks/pyramid-json-merge-tasks/research/findings.md` — только читать.
- `pyramid*.json` в корне — только читать для финальной проверки имён полей.

## Constraints / Non-Goals
- Не писать код и не собирать merged JSON на этой стадии.
- Не менять физику/формулы, не переписывать содержимое.
- Не пересортировывать natural-language списки (`strict_relationships` и т.п.).
- Держать документ кратким и практичным: это инструкция для Task 02, а не научная статья.

## Output Artifacts
- `.tasks/pyramid-json-merge-tasks/schema.md` со следующими обязательными разделами:
  1. **Canonical root layout** — верхнеуровневый контур `OneLaw`: `meta`, `primitives`, `matrix_lo_shu` (с `sides`, `cycle`), `axioms_and_operators` (division_by_zero, delta, Q_hadron, Q_neuro), `resonances`, `frequencies`, `derived_math`, `physical_constants`, `cosmology`, `mass_law` (+ `particles`, `examples`), `pyramid` (+ `pyramid_mathematics`, `chambers`, `acoustic_model`), `greek_alphabet`, `names_of_reality`, `color_music_spheres`, `proof_in_code`, `mathematical_extensions`, `EEG_rhythms`, `biophotonics`, `full_vibration_spectrum`, `fractal_riemann_sphere`, `planck_units`, `strict_relationships`.
  2. **Alias dictionary** — полная таблица `original → canonical`. Обязательно включить:
     - `op → operator`
     - `center_value → center`
     - `sarcophagus → sarcophagus_resonance`
     - `coffer_resonance → sarcophagus_resonance`
     - `Schumann_base → schumann_fundamental`
     - `Hubble_parameter → Hubble_constant` (или наоборот — зафиксировать выбор)
     - `matrix_3x3 → matrix_lo_shu.grid`
     - `cycle.trajectory → matrix_lo_shu.cycle.sequence`
     - `full_cycle → matrix_lo_shu.cycle`
     - `frequencies.pyramid_center → resonances.pyramid_center_Hz`
     - прочие имена, обнаруженные при финальном просмотре файлов.
  3. **Q disambiguation rules** — как разносить голое `Q` на `Q_hadron`/`Q_neuro` в каждом контексте, где оно встречается (Q_definition, King chamber, examples, intermediate_Q, mapping-таблицы).
  4. **Conflict-node shapes** — JSON-шаблоны для:
     - α⁻¹ узла: `{"value": 137.035999084, "approximation": 137, "derivation": "3×45+2", "_source": [...]}`.
     - Schumann узла: `{"value_Hz": 7.83333, "approximation_Hz": 7.83, "formula": "47/6", "derivation": "(TotalSum + 2) / West_digit_6 = 47/6", "_source": [...]}`.
     - Q_neuro: объект `scales: {direct: {...}, symmetric: {...}}`, каждая шкала с `base_frequency_Hz`, `formula`, `mapping`, `_source`; плюс `Q_neuro.note` о Хеопсовой направленности.
     - mapping-блоков, где в исходниках встречается и массив объектов, и объект с ключами-строками (нормализовать в массив `[{key, ...}]`).
  5. **Provenance rules** — где обязателен `_source`, где допустимо его не писать (инвариантное ядро), как именно выглядит идентификатор источника (`pyramid.json#Synthesis_Full`, `pyramid.json#Final_Complete`, `pyramid_more_merge.json`, `pyramid_need_to_merge.json`, `pyramid_need_to_merge_this.json`). Правило для `derivations[]`: массив объектов `{formula, source}`.
  6. **meta.sources[] layout** — структура элемента: `{filename, root_key, version, derivation_base, status}`.
  7. **Ordering rules** — какие массивы сохраняют порядок (strict_relationships*, sequence, trajectory), какие можно сортировать (mappings по `digit`/`Q`).
  8. **JSON formatting rules** — UTF-8, `ensure_ascii=False`, indent=2, кириллица/греческие как есть, числа хранятся как числа, где возможно; строковые формулы — как строки.

## What to Do
- Перечитать `research/findings.md`, особенно разделы «Per-file Structure», «Cross-file Comparison», «Risks & Open Questions», «Sample Excerpts».
- При необходимости выборочно заглянуть в исходные `pyramid*.json` в корне, чтобы удостовериться в точных именах полей, которые попадают в alias dictionary.
- Составить schema.md по структуре выше, максимально конкретно, с короткими JSON-шаблонами для каждого типа узла.
- В каждом разделе явно указать источник (ссылка на раздел findings.md или конкретный файл и путь).

## Expected Output
- Файл `.tasks/pyramid-json-merge-tasks/schema.md`, пригодный как готовая инструкция для реализации Task 02 и для автоматического валидатора Task 04.
- Краткое summary в отчёте агента: какие разделы созданы и какие конфликты явно покрыты.

## Acceptance Criteria
- [ ] `schema.md` содержит все 8 обязательных разделов.
- [ ] В alias dictionary перечислены все алиасы из findings.md §Risks п.4, п.5 и п.10 (минимум 10 записей).
- [ ] В conflict-node shapes явно показаны JSON-шаблоны для α⁻¹, Schumann, Q_neuro.scales.
- [ ] Правила provenance однозначны: понятно, на каких узлах писать `_source` и `derivations`, на каких — нет.
- [ ] В `meta.sources[]` показан точный layout элемента.
- [ ] Правила Q-дезамбигуации явно перечисляют все места появления голого `Q` и канонический перенос.
- [ ] Covered requirements and scenarios are satisfied (R3, R4, R5, R6, R7, R8).
- [ ] I've created a git commit for this task.

> **Примечание по git-стратегии этого плана:** итоговый commit делается один раз в Task 05 (merge + delete). Для Task 01 допускается промежуточный commit с добавлением schema.md, если он удобен исполнителю, но он не обязателен — главное, чтобы финальный commit Task 05 захватил все изменения пакета. Критерий «I've created a git commit for this task» считается выполненным, если изменения этой задачи попали в финальный commit Task 05.
