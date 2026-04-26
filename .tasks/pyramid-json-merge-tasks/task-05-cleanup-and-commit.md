# Task 05: Удаление исходников + единый commit

**Type:** Configuration
**Suggested agent:** Code

## Goal
После подтверждения S1–S4 удалить 4 исходных файла из корня проекта и сделать **один** коммит, который одновременно вносит `pyramid_merged.json` и удаляет исходники. Все промежуточные изменения по предыдущим задачам должны попасть в этот же commit (squash/amend — по ситуации, см. «What to Do»).

## Why This Task Exists
Пользователь явно попросил: оставить только merged и не засорять корень. Для чистоты истории он же попросил единый commit вместо раздельных.

## Spec Coverage
- Requirements: R9
- Scenarios: S5

## Required Inputs
- Подтверждённый зелёный результат Task 03 (`coverage_report.md` — «All unique blocks present…» или все Gaps закрыты).
- Подтверждённый зелёный результат Task 04 (все PASS от `validate_merged.py`).
- `pyramid_merged.json` в корне проекта.
- Исходные файлы для удаления:
  - `pyramid.json`
  - `pyramid_more_merge.json`
  - `pyramid_need_to_merge.json`
  - `pyramid_need_to_merge_this.json`

## Files/Areas
- Корень проекта: удалить 4 перечисленных файла.
- Корень проекта: оставить `pyramid_merged.json`.
- Вспомогательные скрипты/отчёты в `.tasks/pyramid-json-merge-tasks/` остаются как рабочий артефакт задачи и не удаляются.
- Никаких правок в `src/`, `generate.py`, `tests/`, `pyproject.toml`.

## Constraints / Non-Goals
- Не удалять `pyramid_merged.json`.
- Не удалять `.tasks/pyramid-json-merge-tasks/`.
- Не делать force-push, не трогать чужие ветки.
- Не объединять commit с несвязанными изменениями.
- **До Task 03 + Task 04 PASS удаление запрещено.**

## Output Artifacts
- 4 исходных файла физически удалены из рабочего дерева и из индекса git.
- Единый git commit с сообщением в стиле проекта, например:
  - `feat: merge pyramid JSON variants into pyramid_merged.json`
  - в теле коммита — краткая ссылка на план (`.tasks/pyramid-json-merge-tasks/PLAN.md`), перечисление 4 удалённых файлов и появление `pyramid_merged.json`.

## What to Do
1. Перепроверить статус: есть ли чистый результат Task 03 и Task 04 (открыть `coverage_report.md`, ещё раз прогнать `validate_merged.py`).
2. Убедиться, что `git status` показывает:
   - добавленный `pyramid_merged.json`;
   - (возможно) ранее закоммиченные/незакоммиченные артефакты в `.tasks/pyramid-json-merge-tasks/`;
   - 4 исходных файла ещё на месте.
3. Удалить 4 исходника через `git rm` (безопасно, отслеживается git’ом).
4. Если по предыдущим задачам были сделаны промежуточные commits, сделать один commit через `git commit --amend` **только локально на текущей ветке**, либо `git reset --soft <base>` + один commit — предварительно уточнить у пользователя, если ветка уже куда-то выложена.
5. Если промежуточных commit’ов не было (всё в рабочем дереве или в индексе), достаточно `git add -A && git commit -m "..."`.
6. Проверить `git log -1 --stat`: в одном commit — добавление `pyramid_merged.json` и добавление/удаление файлов в `.tasks/pyramid-json-merge-tasks/` и удаление 4 исходников.
7. Проверить `ls pyramid*.json` в корне: должен остаться **только** `pyramid_merged.json`.

## Expected Output
- `git status` чистый, нет неотслеживаемых pyramid-файлов в корне, кроме merged.
- `git log -1` показывает один commit с нужным scope.
- Цитата вывода `ls pyramid*.json` (должен быть ровно один файл) в отчёте.

## Acceptance Criteria
- [ ] Task 03 и Task 04 подтверждены зелёными перед удалением.
- [ ] В корне проекта отсутствуют `pyramid.json`, `pyramid_more_merge.json`, `pyramid_need_to_merge.json`, `pyramid_need_to_merge_this.json`.
- [ ] В корне проекта присутствует `pyramid_merged.json`.
- [ ] Все изменения пакета (merged + cleanup) попадают в один git commit.
- [ ] Commit message соответствует Conventional-Commit-стилю проекта.
- [ ] Реальные выводы `git log -1 --stat` и `ls pyramid*.json` процитированы в отчёте.
- [ ] Covered requirements and scenarios are satisfied (R9, S5).
- [ ] I've created a git commit for this task.
