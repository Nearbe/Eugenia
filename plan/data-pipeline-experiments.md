# Эксперименты: схемотехника подачи данных для 100+ GB весов

## Контекст
- MacBook Pro M4 Max, 128GB RAM
- M4 Max: Apple Silicon с Metal GPU, Neural Engine
- Цель: уместить 100+ GB весов и подавать с максимальной скоростью
- Не Docker (не имеет прямого доступа к Apple Silicon)
- Свой контейнер = нативный процесс на macOS

## Ключевые вопросы

### 1. Сколько моделей одновременно?
- Qwen3.6-35B-A3B: 21GB (Q4_K_M)
- 100GB = ~5 моделей такого размера
- Или одна модель больше?
- Или модели разных размеров?

### 2. Как данные подаются к GPU/Neural Engine?
- Metal framework (MTLBuffer, MTLCommandBuffer)
- Neural Engine (Core ML)
- CPU (ARM NEON)
- Комбинация?

### 3. Какие операции?
- Инференс (генерация токенов)
- KV cache вычисления
- Attention механизмы
- Что ещё?

### 4. Что значит "схемотехника подачи данных"?
- Как веса загружаются из RAM в GPU?
- Как организована память?
- Как данные передаются между слоями?
- Как оптимизировать bandwidth?

## План экспериментов

### Фаза 1: Понимание архитектуры M4 Max
1. [ ] Изучить спецификацию M4 Max:
   - Размер L1/L2 кэша на ядро
   - Metal GPU architecture
   - Neural Engine specs
   - Memory bandwidth (сколько GB/sec)
   - Unified Memory architecture

2. [ ] Изучить как Metal работает с unified memory:
   - MTLBuffer из RAM
   - Zero-copy между CPU и GPU
   - Memory mapping

3. [ ] Изучить как Neural Engine работает с моделями:
   - Core ML format
   - Model optimization
   - Quantization support

### Фаза 2: Понимание llama.cpp оптимизаций
4. [ ] Изучить как llama.cpp использует Metal:
   - ggml-metal.m (Metal backend)
   - Как веса загружаются в GPU
   - Как KV cache хранится в GPU
   - Как происходит inference

5. [ ] Изучить quantization в llama.cpp:
   - Q4_K_M формат
   - Деquantization на лету
   - Как это влияет на скорость

6. [ ] Изучить MoE (Mixture of Experts) оптимизации:
   - Qwen3.6-35B-A3B — MoE модель
   - Как активировать только нужные experts
   - Как это оптимизировано в llama.cpp

### Фаза 3: Прототипирование подачи данных
7. [ ] Протестировать скорость чтения из RAM на M4 Max:
   - Sequential read bandwidth
   - Random read bandwidth
   - Как влияют page faults

8. [ ] Протестировать Metal bandwidth:
   - CPU → GPU transfer speed
   - GPU → CPU transfer speed
   - Zero-copy performance

9. [ ] Протестировать llama-server с разными параметрами:
   - `--n-gpu-layers` (сколько слоёв на GPU)
   - `--threads` (CPU threads)
   - `--ctx-size` (context size)
   - Измерить tokens/sec

10. [ ] Протестировать с разными quantization форматами:
    - Q4_K_M vs Q8_0 vs Q5_K_M
    - Сравнить скорость и качество

### Фаза 4: Проектирование контейнера
11. [ ] Определить минимальный набор оптимизаций:
    - Какие параметры критичны для скорости
    - Какие можно оптимизировать
    - Что даёт максимальный прирост

12. [ ] Спроектировать memory layout:
    - Где хранятся веса (RAM, GPU memory)
    - Как организyется KV cache
    - Как подаются данные между слоями

13. [ ] Спроектировать pipeline inference:
    - Загрузка модели
    - Подготовка контекста
    - Генерация токенов
    - Освобождение ресурсов

## Ожидаемые результаты
- Понимание limits M4 Max для LLM inference
- Понимание как максимизировать throughput
- Схема подачи данных для 100+ GB весов
- Конкретные параметры для llama-server
- Архитектура виртуального контейнера

## Критические метрики
- Memory bandwidth M4 Max: ~400-450 GB/s (unified memory)
- GPU compute: ~39.3 TFLOPS (40-core GPU)
- Neural Engine: ~35 TOPS
- L2 cache: ~72MB shared
- Тестировать реальные throughput на M4 Max

## Важные замечания
- Unified Memory: CPU и GPU делят одну память
- Zero-copy: нет копирования между CPU и GPU
- Quantization: Q4 = 4 бит на вес, в 4 раза меньше памяти
- MoE: только 3B активны на токен, остальные 32B спят
- KV cache: растёт с длиной контекста, потребляет память
