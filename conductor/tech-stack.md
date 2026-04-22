# Technology Stack: Eugenia

## 1.0 Runtime

### 1.1 Язык
- **Python ≥ 3.14** — основной язык реализации
- Интерпретатор как мост между виртуальной машиной и АЛУ
- GIL = детерминированный поток = преимущество

### 1.2 Виртуальный контейнер
- **Eugenia.py** — виртуальный контейнер (не Docker, не процесс, а само исполнение)
- 421GB эффективного пространства вычислений
- Физически аллоцируется всегда — address space как вычислительная среда
- Цикл: 10 шагов (step=0..9), повторяется бесконечно через `cycle(range(Q))`
- Скорость: ~8M+ вызовов/сек (на M4 Max)

## 2.0 Mathematical Ontology (сабмодули)

### 2.1 Universe/ — текстовый Грааль
- Расширенная ZFC-теория множеств
- Множества как процессы ветвления
- Аксиомы: Акт (Id), Потенциал (Ω), Деление (:)
- Операторы: D (ветрение), H (сжатие), ⊕, ⊗
- Соленоиды, p-адические числа, ренормализационная группа
- Essentials/ — 30+ документов по математическим основам

### 2.2 Physics/ — текстовый Грааль
- Физические приложения математической онтологии
- Связь с энтропией, космологией, квантовой механикой
- Фундаментальные взаимодействия

## 3.0 Core Libraries

### 3.1 PyTorch
- SVD-декомпозиция весов для Nucleus
- MPS (macOS) / CUDA (Linux/Windows) бэкенды
- Извлечение детерминированных паттернов из весов

### 3.2 Numerical
- **numpy** — базовые вычисления
- **scipy** — научные функции

### 3.3 Visualization
- **matplotlib** — 22 визуализации + анимации
- **Pillow** — обработка изображений

### 3.4 ML / Data
- **scikit-learn** — t-SNE, классификация
- **safetensors** — формат весов моделей
- **tqdm** — прогресс-бары

### 3.5 Web
- **Flask** — web API (опционально)

## 4.0 LLM Inference

### 4.1 Модель
- **Qwen3.6-35B-A3B** (MoE: 35B total, 3B active per token)
- GGUF формат: `Qwen3.6-35B-A3B-Q4_K_M.gguf` (21.2 ГБ)
- Мультимодальная: `mmproj-Qwen3.6-35B-A3B-BF16.gguf` (903 МБ)
- MXFP4 версия: `mlx-community/Qwen3.6-35B-A3B-mxfp4/`

### 4.2 Inference Engine
- **llama.cpp** — локальный сервер (`llama-server`)
- OpenAI-compatible API (`/v1/chat/completions`)
- Streaming через SSE
- Multi-model router, KV cache management

## 5.0 Architecture Context (`plan/`)

### 5.1 Ключевые принципы
- OpenAI API — базовый протокол
- Rolling window контекста — критично
- MCP JetBrains тулзы — вместо qwen-code tools
- UI — критичная зона ответственности
- LSP-интеграция — мониторинг работы

### 5.2 Архитектура
```
Eugenia.py (виртуальный контейнер)
  ├── Загрузка весов модели в RAM
  ├── Подача данных из RAM к вычислительному ядру
  ├── Rolling window контекста
  ├── Управление контекстом через UI
  ├── MCP JetBrains client
  └── LSP integration
```

## 6.0 Code Quality

### 6.1 Linting
- **ruff** — line-length = 100

### 6.2 Typing
- **mypy** — strict mode

### 6.3 Formatting
- **Formatter** (проект в `Formatter/`)
- Кастомный форматер вместо `ruff format`
- Базовая реализация: `cosmic_formatter`
- План создания Formatter — отдельный track

## 7.0 Testing

### 7.1 pytest
- `tests/test_math.py` — математика дельта-поля
- `tests/test_integration.py` — интеграционные тесты
- pytest-mpl — тесты matplotlib-визуализаций

## 8.0 Build & Install

```bash
pip install -e ".[dev]"
```

### 8.1 Зависимости
```
numpy, scipy, matplotlib, Pillow, torch, tqdm, scikit-learn, safetensors, flask
```

### 8.2 Dev-зависимости
```
pytest, pytest-mpl, ruff, mypy
```
