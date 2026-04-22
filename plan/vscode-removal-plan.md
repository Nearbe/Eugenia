# План: выпиливание VS Code из всех репозиториев

## Контекст
Пользователь хочет удалить ВСЁ, что связано с VS Code из всех 4 репозиториев.
Вместо этого будет своя интеграция с JetBrains IDE через MCP.

## Что найдено

### 1. qwen-code/ — packages/vscode-ide-companion/
**Полный пакет VS Code extension.** Содержит:
- `package.json` — манифест VS Code расширения
- `src/` — исходный код расширения (TypeScript)
- `assets/` — иконки и ассеты
- `schemas/` — JSON-схемы настроек
- `dist/` — скомпилированная версия
- `esbuild.js` — билд-скрипт
- `tailwind.config.js` — стили
- `development.md` — документация по разработке
- `README.md` — описание фич:
  - Native IDE experience (Qwen Code Chat panel)
  - Native diffing (ревью/принятие изменений в diff-режиме)
  - Auto-accept edits mode
  - File management (@-mention files)
  - Conversation history & multiple sessions
  - Open file & selection context

**Зависимости от этого пакета:**
- `packages/webui/` — shared UI компоненты (использует vscode-ide-companion)
- `scripts/build.js` — step 8: build vscode-ide-companion (depends on webui)
- `scripts/build_vscode_companion.js` — отдельный скрипт билда
- `package.json` — npm workspace + скрипты `build:vscode` и `build:all`
- `eslint.config.js` — linting для vscode-ide-companion
- `vitest.config.ts` — тесты для vscode-ide-companion
- `.gitignore` — игнор *.vsix файлов
- `.prettierignore` — игнор schemas
- `CONTRIBUTING.md` — ссылки на VS Code launch config
- `README.md` — ссылка на marketplace
- `docs/users/ide-integration/ide-companion-spec.md` — спецификация для создания companion-плагинов для других IDE (JetBrains, Sublime)
- `docs/plans/` — планы разработки

### 2. qwen-code/ — упоминания VS Code в других файлах
- `.gitignore` — 1 упоминание (*.vsix)
- `.prettierignore` — 1 упоминание (schemas)
- `esbuild.config.js` — нет прямых упоминаний
- `eslint.config.js` — linting rules для vscode-ide-companion
- `package.json` — npm workspace, scripts
- `vitest.config.ts` — тесты
- `scripts/build.js` — build step
- `scripts/build_vscode_companion.js` — весь файл про VS Code
- `scripts/clean.js` — clean step
- `docs/users/overview.md` — ссылка на VS Code extension
- `docs/developers/contributing.md` — инструкции по отладке в VS Code
- `docs/developers/tools/shell.md` — ссылка на VS Code ConPTY
- `docs/plans/` — планы разработки

### 3. Qwen-Agent/ — упоминания VS Code
- `.gitignore` — `./.vscode/` (локальный конфиг разработчика)
- `qwen-agent-docs/website/.gitignore` — `./.vscode/`
- `qwen-agent-docs/website/package-lock.json` — зависимость `@shikijs/vscode-textmate` (подсветка синтаксиса для docs-site)

### 4. llama.cpp/ — упоминания VS Code
- `.gitignore` — `./.vscode/` (локальный конфиг)
- `.dockerignore` — `./.vscode/`
- `README.md` — ссылка на external VS Code extension: `https://github.com/ggml-org/llama.vscode`
- `examples/simple-cmake-pkg/.gitignore` — `./.vscode/`

### 5. whisper.cpp/ — упоминания VS Code
- `.gitignore` — `./.vscode/` (локальный конфиг)

---

## План выпиливания

### Этап 1: Удаление packages/vscode-ide-companion/ из qwen-code/

#### 1.1 Удалить пакет
- Удалить `packages/vscode-ide-companion/` целиком

#### 1.2 Обновить package.json
- Удалить из `workspaces`: `"packages/vscode-ide-companion"`
- Удалить скрипт `"build:vscode": "node scripts/build_vscode_companion.js"`
- Удалить из `build:all`: `&& npm run build:vscode`
- Удалить из `overrides` (если есть зависимости от vscode)

#### 1.3 Удалить скрипты
- Удалить `scripts/build_vscode_companion.js`

#### 1.4 Обновить eslint.config.js
- Удалить linting rules для vscode-ide-companion

#### 1.5 Обновить vitest.config.ts
- Удалить тесты для vscode-ide-companion

#### 1.6 Обновить .gitignore
- Удалить строки с *.vsix

#### 1.7 Обновить .prettierignore
- Удалить строку с schemas

#### 1.8 Обновить docs/
- Обновить `docs/users/overview.md` — убрать ссылку на VS Code
- Обновить `docs/developers/contributing.md` — убрать инструкции по VS Code
- Обновить `docs/users/ide-integration/ide-companion-spec.md` — переписать для JetBrains MCP
- Удалить или обновить `docs/plans/` с упоминаниями vscode

#### 1.9 Обновить CONTRIBUTING.md
- Убрать ссылки на VS Code launch config

#### 1.10 Обновить README.md
- Убрать ссылку на marketplace VS Code

#### 1.11 Проверить зависимости
- Проверить, что `packages/webui/` не зависит от vscode-ide-companion напрямую
- Проверить, что `packages/cli/` не зависит

### Этап 2: Очистка Qwen-Agent/

#### 2.1 Удалить упоминания VS Code
- `.gitignore` — убрать `./.vscode/` (это локальный конфиг, можно оставить)
- `qwen-agent-docs/website/package-lock.json` — убрать `@shikijs/vscode-textmate` (но это в docs-site, который тоже под удалением)

### Этап 3: Очистка llama.cpp/

#### 3.1 Удалить упоминания VS Code
- `.gitignore` — убрать `./.vscode/` (локальный конфиг, можно оставить)
- `.dockerignore` — убрать `./.vscode/`
- `README.md` — убрать ссылку на llama.vscode extension
- `examples/simple-cmake-pkg/.gitignore` — убрать `./.vscode/`

### Этап 4: Очистка whisper.cpp/

#### 4.1 Удалить упоминания VS Code
- `.gitignore` — убрать `./.vscode/` (локальный конфиг, можно оставить)

---

## Итого что удалить:
1. `qwen-code/packages/vscode-ide-companion/` — полный пакет (~весь размер)
2. `qwen-code/scripts/build_vscode_companion.js` — скрипт билда
3. Упоминания VS Code в: package.json, eslint, vitest, gitignore, prettierignore, docs, contributing, readme

## Итого что оставить:
- `.vscode/` в каждом репозитории — это локальный конфиг разработчика, не часть проекта. Можно оставить.

## Итого что переписать:
- `docs/users/ide-integration/ide-companion-spec.md` — переписать спецификацию для JetBrains MCP вместо VS Code
