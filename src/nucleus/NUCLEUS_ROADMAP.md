# Nucleus — Детальный План Развития

**Дата:** 2026-04-18
**Статус модулей:** 20/21 full implementation, 1 skeleton (`llm_crisis_analysis.py`)
**Всего строк кода:** ~5,400+

---

## 📋 Обзор

**Цель системы:** Извлечь "геометрическую структуру" весов существующей модели (Gemma GGUF) — паттерны, которые модель
выучила. Сжать 111GB → ~50MB через SVD. Построить граф корреляций между паттернами.

**Что НЕ делаем:**

- ❌ Не обучаем модель
- ❌ Не запускаем инференс (Gemma не используется как inference engine)
- ❌ Не создаём новую ML-архитектуру

**Что делаем:**

- ✅ Парсим GGUF файлы → извлекаем weight tensors как NumPy arrays
- ✅ Применяем SVD → извлекаем паттерны (собственные векторы)
- ✅ Сжимаем веса → компактная форма (~50MB)
- ✅ Строим граф корреляций между паттернами
- ✅ Сохраняем/загружаем граф (персистентная память)

---

## 🔴 P0: GGUF Weight Extraction (извлечение весов из моделей)

**Статус:** В процессе — `src/extractors/gguf_extractor.py` создан.

### 1.1. GGUF Weight Extractor ✅

**Файл:** `src/extractors/gguf_extractor.py` (420+ строк)

**Реализовано:**

- ✅ `GGUFExtractor` — парсер GGUF формата (ручной бинарный парсинг)
- ✅ `TensorInfo` — metadata для каждого тензора (name, shape, dtype, offset)
- ✅ `GGUFMetadata` — parsed header metadata (KV pairs, tensor count, offsets)
- ✅ `extract_tensor(name)` — извлечение одного тензора как np.ndarray
- ✅ `extract_all_tensors()` — извлечение всех тензоров (dict[str, np.ndarray])
- ✅ `get_tensor_info(name)` — metadata по имени
- ✅ `get_layer_tensors(layer_index)` — тензоры конкретного слоя
- ✅ `get_weight_keys(pattern)` — фильтрация по glob pattern (например "*.weight")
- ✅ `get_model_info()` — metadata модели из GGUF KV pairs (name, architecture, layers, etc.)
- ✅ `extract_gguf_weights(path, pattern)` — convenience function
- ✅ `get_gguf_model_info(path)` — quick model info helper

**Поддерживаемые dtypes:** int8, uint8, float16, float32, float64

**CLI entry point:** `src/extractors/cli_extract.py`

```bash
# Extract all weights matching "*.weight" pattern
python -m extractors.cli_extract --gguf model.gguf

# Extract single tensor by name
python -m extractors.cli_extract --gguf model.gguf --name "model.layers.0.self_attn.q_proj.weight"

# Extract with custom pattern
python -m extractors.cli_extract --gguf model.gguf --pattern "*.k_proj.weight"

# Save to NPZ archive
python -m extractors.cli_extract --gguf model.gguf --output weights.npz

# Save each tensor as separate .npy file
python -m extractors.cli_extract --gguf model.gguf --output-dir extracted_weights/

# Show model info only
python -m extractors.cli_extract --gguf model.gguf --info-only

# List all tensor names
python -m extractors.cli_extract --gguf model.gguf --list-tensors

# Extract specific layer range
python -m extractors.cli_extract --gguf model.gguf --layer-range 0-5
```

**Структура папки extractors:**

```
src/extractors/
├── __init__.py          # Export GGUFExtractor
├── __main__.py          # python -m extractors.cli_extract entry point
├── gguf_extractor.py    # GGUF parser + weight extraction (~420 lines)
└── cli_extract.py       # CLI tool for extraction (~180 lines)
```

### 1.2. Расширение для других форматов (future)

- [ ] `src/extractors/safetensors_extractor.py` — .safetensors формат
- [ ] `src/extractors/pytorch_extractor.py` — .pt/.pth torch.save формат
- [ ] `src/extractors/mlx_extractor.py` — .mlx MLX format

**Зависимости:** Только `numpy`, `struct`. Никаких внешних библиотек для GGUF — ручной бинарный парсинг.

---

## 🔴 P1: Solenoid Lossless Storage (HIGH PRIORITY)

**Цель:** Реализовать механизм хранения данных в соленоиде без потерь, основанный на `H(D(a)) = a` цикле
рекурсии-регрессии. Это фундаментальный слой — без него невозможен ни persistent storage, ни runtime optimization.

### 1.1. Solenoid Point Encoder/Decoder

- [ ] **1.1.1** — `src/nucleus/solenoid_encoder.py`:
    - Метод `encode_to_solenoid(data: np.ndarray) -> dict` — кодирование как solenoid point
        - Вычисляет binary prefix (ε₀...εₙ₋₁) — первые n выборов ветвления
        - Вычисляет D-level metadata (log₂ depth)
        - Вычисляет p-adic residue (a mod Dᵐ)
    - Метод `decode_from_solenoid(encoded: dict) -> np.ndarray` — декодирование обратно
        - Восстанавливает через `Dⁿ(residue) ⊕ prefix_correction`
        - Гарантирует `H(D(z₀)) = z₀` → lossless ✓
    - Метод `verify_lossless(original: np.ndarray, decoded: np.ndarray) -> bool`
        - Проверяет `||original - decoded|| < ε` (ε = 1e-6 для float16)

### 1.2. Solenoid Storage Engine (H∘D cycle engine)

- [ ] **1.2.1** — `src/nucleus/solenoid_engine.py`:
    - Метод `branch(data: np.ndarray) -> np.ndarray` — оператор D(a) = a : Ω
    - Метод `compress(data: np.ndarray) -> np.ndarray` — оператор H(a) = a : D(Id)
    - Метод `full_cycle(data: np.ndarray) -> np.ndarray` — D∘H = identity
        - Применяет H(D(a)) = a → lossless ✓
        - Применяет D(H(a)) = a → lossless ✓
    - Метод `store_solenoid(data: np.ndarray) -> bytes` — сериализация solenoid point
    - Метод `load_solenoid(serialized: bytes) -> np.ndarray` — десериализация

### 1.3. Solenoid-based Pattern Storage (for KnowledgeGraph)

- [ ] **1.3.1** — Расширить `KnowledgeGraph` (в `knowledge_graph.py`):
    - Метод `build_from_weights_solenoid(W, k) -> dict` — SVD + solenoid encoding
    - Метод `get_node_vector_solenoid(idx) -> np.ndarray` — solenoid-encoded vector
    - Метод `similarity_solenoid(i, j) -> float` — similarity via solenoid points

- [ ] **1.3.2** — Расширить `SemanticPatternExtractor` (в `semantic_knowledge_storage.py`):
    - Метод `extract_solenoid_patterns(W) -> List[EigenPattern]` — solenoid-encoded patterns
    - Метод `store_patterns_solenoid(patterns) -> bytes` — solenoid serialization

### 1.4. Solenoid Serialization Format

- [ ] **1.4.1** — Расширить `SemanticStorageFormat` (в `semantic_knowledge_storage.py`):
    - Метод `serialize_solenoid_point(point: dict) -> bytes`:
        - Header: magic number + version
        - Binary prefix (variable length)
        - D-level metadata (log₂ depth as uint32)
        - p-adic residue (variable length, float16 array)
    - Метод `deserialize_solenoid_point(data: bytes) -> dict`:
        - Parse header, validate magic number
        - Extract binary prefix, metadata, residue
        - Return structured solenoid point dict

---

## 🟡 P2: Персистентная память (Persistent Knowledge Storage)

**Цель:** Сохранять/загружать граф знаний из файла. Хитрости: индексы, checkpointing, incremental updates.

### 2.1. Graph Serialization

- [ ] **2.1.1** — Расширить `KnowledgeGraph` (в `knowledge_graph.py`)
    - Метод `save_to_file(path: str, format: str = "binary") -> None` — сериализация графа
    - Метод `load_from_file(path: str, format: str = "binary") -> KnowledgeGraph` — десериализация
    - Поддержка форматов: binary (struct), JSON, NPZ

### 2.2. Checkpointing для графа

- [ ] **2.2.1** — `src/nucleus/graph_checkpoint.py`: checkpointing
    - Метод `save_checkpoint(graph: KnowledgeGraph, path: str, metadata: dict = None) -> str`
    - Метод `load_checkpoint(path: str) -> KnowledgeGraph`
    - Метод `list_checkpoints(path: str) -> list[str]`
    - Метод `cleanup_old_checkpoints(path: str, keep_last: int = 5) -> None`

### 2.3. Persistent Storage (pattern ID store/retrieve)

- [ ] **2.3.1** — `src/nucleus/persistent_storage.py`
    - Метод `store_pattern(pattern: SemanticPattern) -> str` — сохранение, возврат ID
    - Метод `retrieve_pattern(pattern_id: str) -> SemanticPattern` — по ID
    - Метод `store_relationship(rel: PatternRelationship) -> None`
    - Метод `get_relationships_for(pattern_id: str) -> list[PatternRelationship]`
    - Метод `get_all_patterns() -> list[SemanticPattern]`
    - Метод `get_all_relationships() -> list[PatternRelationship]`

### 2.4. Graph Indexing (KNN for fast search)

- [ ] **2.4.1** — `src/nucleus/graph_index.py`
    - Метод `build_knn_index(patterns: np.ndarray) -> object` — KNN-индекс (FAISS или scipy)
    - Метод `query_index(query: np.ndarray, k: int = 10) -> tuple[np.ndarray, np.ndarray]`
    - Метод `save_index(path: str) -> None`
    - Метод `load_index(path: str) -> object`

---

## 🟢 P3: SVD Pattern Extraction Pipeline

**Цель:** Полный пайплайн — GGUF → weights → SVD patterns → KnowledgeGraph.

### 3.1. Gemma → Nucleus Pipeline

- [ ] **3.1.1** — `src/nucleus/gemma_nucleus_pipeline.py`
    - Метод `load_gemma_weights(path: str) -> dict` — загрузка всех весов через GGUFExtractor
    - Метод `extract_all_patterns(k: int = 32) -> dict` — SVD по всем слоям
    - Метод `compute_cross_layer_correlations() -> np.ndarray` — межслойные корреляции
    - Метод `build_nucleus_graph() -> KnowledgeGraph` — построение графа
    - Метод `save_nucleus_state(path: str) -> None` — сохранение состояния

- [ ] **3.1.2** — CLI: `src/nucleus/cli/extract_gemma.py`
    - Команда `python -m nucleus.cli.extract_gemma --gguf path/to/model.gguf --k 32 --output output/`

### 3.2. Unit Tests for Extractors

- [ ] **3.2.1** — `tests/test_extractors_gguf.py`
    - Тест GGUF header parsing (magic number, version)
    - Тест tensor extraction correctness (shape, dtype match)
    - Тест model info extraction

---

## 🟢 P4: Оптимизация для реального рантайма

### 4.1. GPU Acceleration (MPS/CUDA)

- [ ] **4.1.1** — `src/nucleus/gpu_accelerator.py`
    - Метод `to_device(tensor: np.ndarray, device: str = "auto") -> torch.Tensor`
    - Метод `svd_gpu(matrix: torch.Tensor, k: int) -> tuple[torch.Tensor, torch.Tensor]`
    - Метод `correlation_gpu(a: torch.Tensor, b: torch.Tensor) -> float`
    - Метод `to_numpy(tensor: torch.Tensor) -> np.ndarray`

### 4.2. Caching & Memory Management

- [ ] **4.2.1** — `src/nucleus/cache_manager.py`
    - Метод `cache_pattern_projection(input: np.ndarray, key: str = None) -> np.ndarray`
    - Метод `get_cached(key: str) -> np.ndarray | None`
    - Метод `clear_cache() -> None`
    - Метод `get_stats() -> dict`

### 4.3. Batch Processing & Vectorization

- [ ] **4.3.1** — `src/nucleus/batch_processor.py`
    - Метод `batch_forward(batch: np.ndarray, core: DeterministicKnowledgeCore) -> np.ndarray`
    - Метод `batch_similarity(matrix_a: np.ndarray, matrix_b: np.ndarray) -> np.ndarray`
    - Метод `batch_svd(weights: list[np.ndarray], k: int) -> list[tuple]`

---

## 🟢 P5: Мульти-модальные входы

### 5.1. Input Normalizer для разных типов данных

- [ ] **5.1.1** — `src/nucleus/multi_modal_input.py`
    - Метод `normalize_text(text: str) -> np.ndarray`
    - Метод `normalize_image(image: np.ndarray) -> np.ndarray` (delta field + topology)
    - Метод `normalize_audio(audio: np.ndarray) -> np.ndarray` (MFCC features)
    - Метод `normalize_numerical(data: np.ndarray) -> np.ndarray`

### 5.2. Cross-Modal Fusion

- [ ] **5.2.1** — `src/nucleus/modal_fusion.py`
    - Метод `fuse_text_image(text_vec: np.ndarray, image_vec: np.ndarray) -> np.ndarray`
    - Метод `fuse_all_modalities(vectors: dict[str, np.ndarray]) -> np.ndarray`
    - Метод `compute_modality_weights(vectors: dict[str, np.ndarray]) -> dict[str, float]`

---

## 📊 Сводная таблица задач

| Фаза                          | Задач                 | Строк кода  | Приоритет |
|-------------------------------|-----------------------|-------------|-----------|
| P0: GGUF Weight Extraction    | 1 (done) + 2 (future) | ~600 + ~800 | 🔴 High   |
| P1: Solenoid Lossless Storage | 4 задачи              | ~1,800      | 🔴 High   |
| P2: Persistent Memory         | 4 задачи              | ~1,500      | 🟡 Medium |
| P3: SVD Pipeline              | 3 задачи              | ~800        | 🟢 Low    |
| P4: Runtime Optimization      | 7 задач               | ~1,200      | 🟢 Low    |
| P5: Multi-modal               | 6 задач               | ~1,000      | 🟢 Low    |
| **Итого**                     | **27**                | **~7,300**  |           |

---

## 🔄 Зависимости между фазами

```
P0: GGUF extraction ──→ P1: Solenoid storage (lossless encoding)
P0: GGUF extraction ──→ P2: Persistent storage (save/load graph)
P1: Solenoid storage ──→ P2: Persistent storage (save/load solenoid points)
P1: Solenoid storage ──→ P3: SVD pipeline (lossless pattern storage)
P1: Solenoid storage ──→ P4: Runtime optimization (fast solenoid decode)
P2: Persistent storage ──→ P4: Runtime optimization (caching, indexing)
P3: SVD pipeline ────→ P5: Multi-modal (unified pattern space)
```

---

## 📅 Рекомендуемый порядок выполнения

1. **Фаза 0 (P0):** ✅ GGUF weight extraction — DONE
2. **Фаза 1 (P1):** 🔴 Solenoid storage — lossless encoding mechanism (HIGH PRIORITY)
3. **Фаза 2 (P2):** 🟡 Persistent memory (save/load graph, checkpointing)
4. **Фаза 3 (P3):** 🟢 SVD pipeline — GGUF → weights → patterns → graph
5. **Фаза 4 (P4):** 🟢 GPU acceleration + caching
6. **Фаза 5 (P5):** 🟢 Multi-modal inputs & fusion

---

## 🎯 Критерии готовности

- [x] GGUF weight extraction работает (ручной бинарный парсинг)
- [ ] 🔴 **P1: Solenoid storage — H(D(a)) = a cycle verified** — lossless encoding/decoding
- [ ] 🔴 **P1: Solenoid serialization — binary format with magic number + version**
- [ ] P2: Все 21 nucleus модуль полностью реализованы (не скелеты)
- [ ] Покрытие тестами ≥ 80% для nucleus модулей
- [ ] GGUF веса извлекаются и паттерны строятся автоматически (pipeline)
- [ ] Граф знаний сохраняется/загружается из файла (persistent storage)
- [ ] SVD выполняется на GPU (MPS/CUDA) с ускорением ≥ 3x
- [ ] Кэш проекций даёт ≥ 70% hit rate для повторяющихся запросов
- [ ] Поддержка text, image, audio, numerical inputs
