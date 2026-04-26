# Task 02: Сборка pyramid_merged.json

**Type:** Code Modification
**Suggested agent:** Code

## Goal
Реализовать вспомогательный скрипт `build_merged.py` в `.tasks/pyramid-json-merge-tasks/`, который читает 4 исходных `pyramid*.json` из корня проекта, применяет нормализационную схему из `schema.md` и записывает единый `pyramid_merged.json` в корень проекта. В самом файле Eugenia-рантайма не меняется ничего.

## Why This Task Exists
Это ядро плана: именно здесь 4 источника сливаются в один канонический файл. Без корректного детерминированного скрипта невозможно выполнить валидацию (Task 04) и cleanup (Task 05).

## Spec Coverage
- Requirements: R1, R2, R3, R4, R5, R6, R7, R8
- Scenarios: S1

## Required Inputs
- `.tasks/pyramid-json-merge-tasks/schema.md` — нормализационная схема из Task 01 (canonical layout, alias dictionary, conflict-node shapes, provenance rules, meta.sources layout, ordering/formatting rules).
- `.tasks/pyramid-json-merge-tasks/research/findings.md` — подробная карта блоков, конфликтов, sample excerpts.
- Исходные файлы в корне проекта:
  - `pyramid.json` (два корневых блока: `OneLaw_Synthesis_Full` + `OneLaw_Final_Complete` v3.0; обрабатывать как два источника `pyramid.json#Synthesis_Full` и `pyramid.json#Final_Complete`);
  - `pyramid_more_merge.json` (`OneLaw_Final_Complete` v3.0);
  - `pyramid_need_to_merge.json` (`OneLaw_Complete_Exact` v2.0);
  - `pyramid_need_to_merge_this.json` (`OneLaw_Complete`, без version).

## Files/Areas
- `.tasks/pyramid-json-merge-tasks/build_merged.py` — **создать**; инкапсулирует всю логику слияния.
- `pyramid_merged.json` — **создать в корне проекта** как результат выполнения скрипта.
- `pyramid*.json` в корне — **только читать**, не модифицировать.
- Никаких правок в `src/`, `generate.py`, `tests/`, `pyproject.toml`.

## Constraints / Non-Goals
- Python 3.14, стиль проекта (ruff, line-length=100, snake_case).
- Не удалять исходные файлы (это делает Task 05).
- Не подключать скрипт к Eugenia CLI, не регистрировать как renderer.
- Не использовать внешних зависимостей сверх stdlib (`json`, `pathlib`, `collections`, `dataclasses` — достаточно).
- Сохранить порядок `strict_*` списков и повествовательных последовательностей.
- Не пересортировывать greek letters / names_of_reality / side digits.
- `json.dump(..., ensure_ascii=False, indent=2)`.

## Output Artifacts
- `.tasks/pyramid-json-merge-tasks/build_merged.py` — сборочный скрипт.
- `pyramid_merged.json` в корне проекта — итоговый слитый JSON.
- Короткий лог сборки (stdout скрипта) с перечислением: прочитанных источников, числа применённых алиасов, числа конфликтных узлов с политикой разрешения.

## What to Do
1. Создать `build_merged.py` с CLI без аргументов: запуск из корня проекта (пути к исходникам жёстко `Path(__file__).resolve().parents[2] / "pyramid*.json"` или эквивалент — корень репо).
2. Реализовать шаги:
   - Загрузить 4 исходника, распаковать `pyramid.json` на два логических источника `#Synthesis_Full` и `#Final_Complete`.
   - Построить `meta.sources[]` по layout из schema.md.
   - Применить alias dictionary из schema.md: пройти по каждому источнику и переименовать ключи к каноническим именам.
   - Дезамбигуировать голое `Q` в `Q_hadron`/`Q_neuro` по правилам schema.md.
   - Нормализовать mapping-блоки (объект ↔ массив) к единому виду (массив объектов).
   - Слить инвариантное ядро (grid Ло Шу, стороны, цикл, проценты, константы, m_p, 210 ступеней, координаты Гизы) ровно один раз — без `_source` на самих числах, но с возможностью указать источники через `derivations[]`, если формулы вывода различаются.
   - Для конфликтных узлов применить JSON-шаблоны из schema.md:
     - α⁻¹: `{value: 137.035999084, approximation: 137, derivation: "3×45+2", _source: [...]}`;
     - Schumann: `{value_Hz: 7.83333, approximation_Hz: 7.83, formula: "47/6", derivation: "...", _source: [...]}`;
     - Q_neuro: `scales.direct` (f0=1.25, источники: `pyramid.json#Synthesis_Full`, `pyramid_need_to_merge.json`), `scales.symmetric` (f0=2.5, источники: `pyramid.json#Final_Complete`, `pyramid_more_merge.json`), плюс `Q_neuro.note` про Хеопсову направленность.
   - Собрать union уникальных блоков: EEG_rhythms, biophotonics, full_vibration_spectrum, particles (+groups +examples), planck_units, pyramid_mathematics, fractal_riemann_sphere, mathematical_extensions (algebra_of_colon, spectral_delta, riemann_proof_sketch, solenoid_metric, universal_wavefunction, particle_derivation), derived_frequencies_HZ, formula_alpha, derivation_GUT, matrix_properties.total_product=362880, primitives, intermediate_Q, greek letters_as_operators (расширенный список букв + word_equation), delta_definition, Q_definition, color_music_spheres, names_of_reality, proof_in_code, strict_mathematical_relationships, strict_relationships.
   - Прописать `_source: [<filenames>]` на всех уникальных и конфликтных узлах; где формул несколько — собрать `derivations: [{formula, source}, ...]`.
3. Запустить скрипт, проверить, что `pyramid_merged.json` создаётся и валиден (`json.load`).
4. Вывести в stdout короткий отчёт со статистикой.

## Expected Output
- Файл `pyramid_merged.json` создан в корне репо и валиден (S1 проходит).
- Файл `.tasks/pyramid-json-merge-tasks/build_merged.py` создан и содержит всю логику.
- Stdout сборки перечисляет источники и суммарные счётчики.

## Acceptance Criteria
- [ ] `python3 .tasks/pyramid-json-merge-tasks/build_merged.py` выполняется без ошибок.
- [ ] `pyramid_merged.json` создан в корне проекта и валиден для `json.load`.
- [ ] Итоговый JSON имеет единый корневой ключ `OneLaw`.
- [ ] `OneLaw.meta.sources` содержит 4 записи (Synthesis_Full, Final_Complete, Complete_Exact, Complete) с корректными `filename`, `root_key`, `version`, `derivation_base`, `status`.
- [ ] `OneLaw.axioms_and_operators.Q_neuro.scales.direct` и `.symmetric` оба присутствуют с корректными `base_frequency_Hz`, `formula`, `mapping`, `_source`.
- [ ] `OneLaw.physical_constants.alpha_inverse` имеет поля `value`, `approximation`, `derivation`, `_source`.
- [ ] `OneLaw.resonances.schumann_fundamental` имеет `value_Hz`, `approximation_Hz`, `formula`, `_source`.
- [ ] Ни в одном узле merged не встречаются старые алиасы (`op`, `center_value`, `coffer_resonance`, `sarcophagus` как корневое имя резонанса, `Schumann_base`, `matrix_3x3`).
- [ ] Все уникальные разделы из R2 присутствуют по известным путям (сверить с findings.md).
- [ ] Covered requirements and scenarios are satisfied (R1–R8, S1).
- [ ] I've created a git commit for this task *(см. примечание о git-стратегии в конце PLAN.md)*.
