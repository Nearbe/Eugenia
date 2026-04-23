# Solenoid Roadmap — Карта решений на основе анализа whisper.cpp и llama.cpp

> **Дата:** 2026-04-23
> **Статус:** Draft
> **Цель:** Синтез идей из GGML (whisper.cpp) и K-quant (llama.cpp) в контексте Solenoid storage layer

---

## A. Математический синтез

### GGML (whisper.cpp) — одноуровневое квантование

Формула квантования GGML:

```
x̂ = ⌊x / scale⌋ × scale + bias
```

- **Один уровень масштаба** на блок (обычно 256 элементов)
- **Статическая числовая иерархия** — scale/bias вычисляются один раз per-block
- **Linear по природе** — floor + multiply — нет нелинейных операций
- **Без рекурренции** — `n = 0`, нет итеративного применения
- Без awareness к importance (кроме per-channel в некоторых форматах)

### K-quant (llama.cpp) — двухуровневая иерархия

```
x̂ = d_super × s[j] × Q(x)
```

Где:
- `d_super` — super-block scale (на 16 sub-block'ов)
- `s[j]` — sub-block scale (на 32 элемента)
- `Q(x)` — квантованные индексы (int2/int4/int8)
- **Два уровня рекурренции** — `n = 2` (super → sub)
- **Adaptive scale** на sub-block уровне
- **Importance-aware** в IQ (Implicit Quantization) форматах
- **Non-linear**: ❌ (всё ещё floor/multiply)

### Solenoid — итеративный branching-compression

```
x̂ = Dⁿ(Hⁿ(x))
```

Где:
- `H: ℝᵈ → ℝᵏ` — hashing/reduction (d → k)
- `D: ℝᵏ → ℝᵈ` — branching/expansion (k → d)
- `n` — глубина итераций (адаптивная per-element)
- **∞ уровней рекурренции** — `n` адаптивен per-tensor per-element
- **Lossless cycle**: `H(D(a)) = a` — теоретически точное восстановление
- **Dynamic иерархия** — не фиксированная, а формируется из данных
- **Process ontology** — хранит генератор, не данные
- **Non-linear по природе** — `Dⁿ` нелинеен

### Сравнительный анализ

| Аспект | GGML (whisper) | K-quant (llama) | Solenoid |
|--------|---------------|-----------------|----------|
| Рекурренция | 0 | 2 | ∞ |
| Обратимость | ❌ | ❌ | ✅ `H(D(a)) = a` |
| Adaptive scale | ❌ | ✅ sub-block | ✅ element-level |
| Importance-aware | ❌ | ✅ IQ | ✅ SVD-based |
| Non-linear | ❌ | ❌ | ✅ `Dⁿ` |
| bpw | 2.5–8.0 | 0.89–6.56 | <0.1 |
| Онтология | Static | Static | Dynamic |
| Формула | `⌊x/s⌋×s+b` | `d_super × s[j] × Q` | `Dⁿ(Hⁿ(x))` |

### Ключевые выводы

1. **Общее с GGML/K-quant:** все используют фиксированную числовую иерархию масштабов
2. **Уникальное Solenoid:**
   - Lossless cycle `H(D(a)) = a` — теоретически точное восстановление
   - Динамическая иерархия — `n` адаптивен per-tensor per-element
   - Process ontology — хранит генератор, не данные
   - Non-linear по природе (`Dⁿ` нелинеен)
3. **Gap:** текущие форматы ограничены 2 уровнями; Solenoid открывает ∞ уровней

---

## B. Сводная таблица решений

### P0: Multi-scale Solenoid (из llama.cpp Q4_K)

**Источник:** llama.cpp Q4_K / Q6_K — super-block + sub-block scales

**Идея:** Интегрировать двухуровневую иерархию масштабов в Solenoid как первый шаг к ∞-уровневой модели.

**Формула:**
```
W_recon = D²(Id) × [D(Id)]^8 × Q
```

Где:
- `D²(Id)` — super-block branching (16 sub-block'ов)
- `[D(Id)]^8` — sub-block branching (8 элементов на sub-block)
- `Q` — квантованные индексы (входные данные для branching)

**Потенциал:**
- whisper large-v3-turbo: 547MB → ~350MB (4.3×)
- Низкий риск — прямая интеграция с существующим GGML block structure

**Зависимости:** нет

**Реализация:**
1. Заменить статический scale на `D`-branching в solenoid_engine
2. Поддержать super/sub-block metadata
3. `H` = reduced mean per sub-block, `D` = expand + multiply

---

### P1: Importance-weighted Solenoid (из llama.cpp AWQ)

**Источник:** llama.cpp AWQ (Activation-aware Weight Quantization) + IQ formats

**Идея:** Использовать SVD singular values для определения importance и адаптивной глубины Solenoid.

**Формула:**
```
n_i = clip(importance_i × n_max / max(importance), n_min, n_max)
```

Где:
- `importance_i = σ_i / Σσ_j` — нормализованный singular value
- `n_min = 1`, `n_max = 8` (configurable)
- `Hⁿⁱ(x)` — hashing `n_i` раз для элемента `i`
- `Dⁿⁱ(a)` — branching `n_i` раз

**Потенциал:**
- 350MB → ~250MB (6× от оригинала)
- Высокий приоритет — direct надстройка над P0

**Зависимости:** P0 (multi-scale)

**Реализация:**
1. Вычислить SVD per-layer: `W = UΣVᵀ`
2. `importance = |Σ|` → нормализация
3. Mapping `importance → n_i` (clip + scale)
4. Adaptive `Hⁿⁱ` и `Dⁿⁱ` в solenoid_engine
5. Store `n_matrix` как metadata (~d×1 bytes)

---

### P2: Hybrid SVD + Solenoid (самый большой потенциал)

**Источник:** SVD compression (из COMPRESSION_SUMMARY.md) + Universal Knowledge Protocol

**Идея:** Разложить веса через SVD, применить Solenoid только к residual. Core-часть хранится в low-rank формате.

**Pipeline:**
```
W ≈ UₖΣₖVₖᵀ + R
Solenoid(R) → compressed_residual
```

Где:
- `k = 32` (configurable)
- `UₖΣₖVₖᵀ` — core (low-rank), ~1.05MB для 111GB tensor
- `R = W - UₖΣₖVₖᵀ` — residual (~6MB после Solenoid)

**Формула:**
```
W_recon = UₖΣₖVₖᵀ + Dⁿ(Hⁿ(R))
```

**Потенциал:**
- 111GB → ~50-70MB (20×)
- **Переработка всего pipeline** — максимальный риск и потенциал

**Зависимости:** P0, P1

**Реализация:**
1. SVD decomposition per-layer (batched, GPU)
2. Выбрать `k` по budget per-layer
3. Store `Uₖ, Σₖ, Vₖ` в low-rank format
4. Вычислить `R = W - UₖΣₖVₖᵀ`
5. Apply Solenoid to `R`
6. Metadata: `k` per-layer + Solenoid params

**Бюджет (пример для 111GB):**
```
k=32:
  UₖΣₖVₖᵀ = 111GB × (2×32 / 4096) ≈ 1.74GB
  R = 111GB - 1.74GB ≈ 109.3GB
  Solenoid(R) @ <0.1bpw ≈ ~10MB
  Total ≈ 1.75GB (63×)

k=128:
  UₖΣₖVₖᵀ = 111GB × (2×128 / 4096) ≈ 6.94GB
  R ≈ 104GB
  Solenoid(R) ≈ ~10MB
  Total ≈ 7GB (16×)
```

---

### P3: Adaptive block size + non-linear (оптимизация)

**Источник:** llama.cpp block-size variants + non-linear quantization research

**Идея 1 — Adaptive block size:**
```
block_size = f(variance, budget)
n_iter = g(block_size, importance)
```

Где:
- `variance` per sub-region → определяет granularity
- `budget` → global bpw constraint
- Small blocks для high-variance regions
- Large blocks для smooth regions

**Идея 2 — Non-linear activation:**
```
x_recon = base + α·tanh(β·(residual - μ)) + γ·(residual - μ)²
```

Где:
- `base` = mean per block
- `residual = x - base`
- `tanh` — мягкая нелинейность (стабильные градиенты)
- `quadratic` — хвосты распределения
- `α, β, γ` — learnable per-block

**Потенциал:**
- +10-20% к P2 (fine-grained optimization)
- Не критичен для базового функционала

**Зависимости:** P0, P1, P2

**Реализация:**
1. Adaptive block size: variance analysis per-layer
2. Non-linear: tanh + quadratic terms in Dⁿ
3. Learn `α, β, γ` per-block via MSE minimization
4. Integrate into solenoid_engine

---

## C. Карта решений P0–P5

```
P0 ──────────────────────────────────────────────────────────┐
  Multi-scale Solenoid                                       │
  (super/sub-block branching)                               │
  ↓ Нет зависимостей                                          │
                                                             │
P1 ──────────────────────────────────────────────────────────┼───┐
  Importance-weighted Solenoid                              │   │
  (SVD → adaptive n_i)                                      │   │
  ↓ Зависит от: P0                                          │   │
                                                             │   │
P2 ──────────────────────────────────────────────────────────┼───┼───┐
  Hybrid SVD + Solenoid                                     │   │   │
  (low-rank core + Solenoid(R))                             │   │   │
  ↓ Зависит от: P0, P1                                      │   │   │
                                                             │   │   │
P3 ──────────────────────────────────────────────────────────┼───┼───┐
  Adaptive block + non-linear                               │   │   │
  (variance → block_size; tanh activation)                  │   │   │
  ↓ Зависит от: P0, P1, P2                                  │   │   │
                                                             │   │   │
P4 ──────────────────────────────────────────────────────────┼───┼───┼───┐
  GPU acceleration + batch processing                       │   │   │   │
  (并行化 SVD + Solenoid)                                    │   │   │   │
  ↓ Зависит от: P0-P3                                       │   │   │   │
                                                             │   │   │   │
P5 ──────────────────────────────────────────────────────────┼───┼───┼───┐
  Universal Knowledge Protocol integration                  │   │   │   │
  (P(d×k) + S(k) + Solenoid storage)                       │   │   │   │
  ↓ Зависит от: P0-P4                                       │   │   │   │
                                                             │   │   │   │
```

### Сводка по фазам

| Фаза | Название | Потенциал | Риск | Зависимости |
|------|----------|-----------|------|-------------|
| **P0** | Multi-scale | 4.3× | Низкий | Нет |
| **P1** | Importance-weighted | 6× | Средний | P0 |
| **P2** | Hybrid SVD+Sol | 20× | Высокий | P0, P1 |
| **P3** | Adaptive + non-linear | +10-20% к P2 | Средний | P0, P1, P2 |
| **P4** | GPU acceleration | infra | Средний | P0-P3 |
| **P5** | Universal Knowledge | architecture | Высокий | P0-P4 |

---

## D. Рекомендации по приоритизации

### 1. Начать с P0 — Multi-scale Solenoid

**Почему:**
- Низкий риск — прямая интеграция с существующим GGML block structure
- Быстрая интеграция — не требует переработки pipeline
- Валидирует branching-compression концепцию на знакомой структуре
- Даёт первый практический результат (4.3× compression)

**Action items:**
- [ ] Интегрировать super-block + sub-block в solenoid_engine.py
- [ ] Реализовать `D²` и `D⁸` branching
- [ ] Добавить metadata format для super/sub scales
- [ ] Тест на whisper large-v3-turbo

### 2. P1 — Importance-weighted Solenoid

**Почему:**
- Надстройка над P0 —复用 multi-scale infrastructure
- Direct применение SVD insights из COMPRESSION_SUMMARY.md
- Значительный буст к compression (6×)
- Валидирует adaptive depth концепцию

**Action items:**
- [ ] SVD per-layer → importance matrix
- [ ] Mapping `importance → n_i`
- [ ] Adaptive `Hⁿⁱ` и `Dⁿⁱ` в solenoid_engine
- [ ] Store `n_matrix` как metadata

### 3. P2 — Hybrid SVD + Solenoid

**Почему:**
- **Переработка всего pipeline** — максимальный потенциал (20×)
- Core-residual split — наиболее эффективная стратегия
- Low-rank core = lossless, Solenoid(R) = lossy → оптимальный tradeoff
- Ключевой инсайт: SVD k=32 → core 1.05MB + residual Solenoid ~6MB

**Action items:**
- [ ] Batched SVD per-layer (GPU)
- [ ] Dynamic `k` selection per-layer по budget
- [ ] Low-rank storage для `UₖΣₖVₖᵀ`
- [ ] Solenoid encoding residual
- [ ] Реверсивный pipeline: `W_recon = UₖΣₖVₖᵀ + Dⁿ(Hⁿ(R))`

### 4. P3 — Adaptive + non-linear

**Почему:**
- Fine-grained optimization — +10-20% к P2
- Adaptive block size — variance-driven granularity
- Non-linear activation — tanh + quadratic для хвостов
- Не критичен для базового функционала

**Action items:**
- [ ] Variance analysis per-layer
- [ ] Mapping `variance → block_size`
- [ ] Tanh + quadratic terms in Dⁿ
- [ ] Learn `α, β, γ` per-block

### 5. P4 — GPU acceleration

**Почему:**
- SVD и Solenoid encoding — compute-intensive
- Batch processing — critical для large models
- Infra-оптимизация, не compression

### 6. P5 — Universal Knowledge Protocol

**Почему:**
- Architecture-level change
- `P(d×k) + S(k)` — фундаментальное расширение
- Long-term vision

---

## E. Интеграция с существующим Nucleus

### P0 → `solenoid_engine.py`

**Текущее состояние:** Solenoid engine с базовым `H`/`D`
**Изменение:** Добавить super/sub-block metadata и multi-scale branching
**Файлы:**
- `src/nucleus/solenoid_engine.py` — добавить `MultiScaleSolenoid` class
- `src/nucleus/solenoid_storage.py` — обновить format spec

### P1 → `knowledge_graph.py` + `semantic_knowledge_storage.py`

**Текущее состояние:** Knowledge graph и semantic storage
**Изменение:** Add importance-aware metadata to knowledge entries
**Файлы:**
- `src/nucleus/knowledge_graph.py` — add `importance_matrix` field
- `src/nucleus/semantic_knowledge_storage.py` — adaptive depth per entry

### P2 → `gemma_nucleus_pipeline.py`

**Текущее состояние:** Gemma-based nucleus pipeline
**Изменение:** Переопределить weight loading — SVD decompose + Solenoid encode
**Файлы:**
- `src/nucleus/gemma_nucleus_pipeline.py` — hybrid SVD+Solenoid loader
- `src/nucleus/solenoid_engine.py` — `HybridSolenoid` class

### P3 → `gpu_accelerator.py` + `batch_processor.py`

**Текущее состояние:** GPU acceleration and batch processing
**Изменение:** Adaptive block size + non-linear in GPU kernels
**Файлы:**
- `src/nucleus/gpu_accelerator.py` — adaptive kernel selection
- `src/nucleus/batch_processor.py` — variance-driven batching

---

## F. Ключевые метрики и цели

### Текущее состояние (Solenoid storage)

| Метрика | Значение |
|---------|----------|
| bpw | <0.1 |
| Lossless cycle | ✅ `H(D(a)) = a` |
| Adaptive scale | ❌ (базовый) |
| Importance-aware | ❌ |
| Non-linear | ❌ (базовый) |
| Рекурренция | 1 (базовый) |

### Цели по фазам

| Фаза | bpw | Compression | Adaptive | Importance | Non-linear | Рекурренция |
|------|-----|-------------|----------|------------|------------|-------------|
| **P0** | ~0.5 | 4.3× | ✅ sub-block | ❌ | ❌ | 2 |
| **P1** | ~0.3 | 6× | ✅ element | ✅ SVD | ❌ | adaptive |
| **P2** | ~0.05 | 20× | ✅ element | ✅ SVD | ❌ | adaptive |
| **P3** | ~0.04 | 22× | ✅ variance | ✅ SVD | ✅ tanh | adaptive |

---

## G. Риски и митигация

### P0 — Multi-scale

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| Metadata overhead | Низкий | Super/sub-block — фиксированный overhead |
| Encoding complexity | Низкий | Прямая интеграция с GGML structure |
| Decoding latency | Средний | Cache super-block scales |

### P1 — Importance-weighted

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| SVD compute cost | Высокий | Batched SVD на GPU (P4) |
| Metadata size (n_matrix) | Средний | ~d bytes per layer — приемлемо |
| Quality degradation | Средний | Adaptive n_min = 1 — fallback |

### P2 — Hybrid SVD + Solenoid

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| SVD numerical stability | Средний | Regularization, thresholding |
| Low-rank approximation error | Высокий | Dynamic k per-layer по budget |
| Pipeline complexity | Высокий | Modular design: SVD layer → Solenoid layer |
| Training compatibility | Средний | Hybrid loader — transparent to model |

### P3 — Adaptive + non-linear

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| Learnable params overhead | Средний | Per-block params — ~64 bytes/block |
| Training instability | Низкий | tanh — stable gradients |
| Diminishing returns | Высокий | A/B testing vs P2 baseline |

---

## H. Формат хранения (предложение)

### Solenoid Multi-scale Format (SMF) v0.1

```
Header:
  magic: 0x534F4C4E  ("SOLE")
  version: 0x0001
  format: MULTI_SCALE (0) | HYBRID_SVD (1)
  layers: N

Layer (i):
  name: string
  shape: [d_in, d_out]
  
  Multi-scale mode:
    super_block_size: int (default 16)
    sub_block_size: int (default 32)
    super_scale: float[ceil(d / super_block_size)]
    sub_scale: float[ceil(d / sub_block_size)]
    n_matrix: int8[shape]         (depth per element)
    quantized_data: bytes          (Q indices)
    
  Hybrid SVD mode:
    k: int (rank)
    U_k: float[d_in × k]
    Sigma_k: float[k]
    V_k: float[k × d_out]
    residual_solenoid: bytes       (Dⁿ(Hⁿ(R)))
```

---

## I. Ссылки на источники

1. **WHISPER_CPP_COMPARISON.md** — GGML квантование, lossless cycle, multi-scale
2. **LLAMA_CPP_SOLENOID_IDEAS.md** — 5 идей: multi-scale, importance-weighted, hybrid SVD+K-quant, adaptive block size, non-linear
3. **COMPRESSION_SUMMARY.md** — SVD k=4 (125x, 99% ошибка), k=8 (62x, 98% ошибка)
4. **UNIVERSAL_KNOWLEDGE.md** — Universal Knowledge Protocol, P(d×k) + S(k)
5. **EUGENIA_ARCHITECTURE.md** — архитектура, geometric extractor, Solenoid storage layer
6. **NUCLEUS_ROADMAP.md** — текущий план, P0-P5 фазы

---

## J. Next Steps

1. **Немедленно:** P0 — Multi-scale Solenoid (1-2 дня)
2. **Следующая спринт:** P1 — Importance-weighted (3-5 дней)
3. **После валидации P0+P1:** P2 — Hybrid SVD (1-2 недели)
4. **По мере стабильности:** P3-P5 — оптимизация и масштабирование
