## Краткий вывод

Read-only разведка выполнена для `src/core`, `src/nucleus`, документации `Universe` и тестового покрытия. Основной вывод: математический код уже выделен в отдельный слой, но сейчас он больше похож на набор разрозненных операторов и прототипов, чем на строгую математическую библиотеку с единым контрактом.

Ключевые проблемы:

- `src/core` содержит много мелких файлов-операторов, но нет явной канонической спецификации доменов, типов, инвариантов и связей между операторами `D/H/L/Ω/Π/Δ/solenoid/p-adic`.
- Часть реализаций расходится с документацией: например, `delta_field.py` использует `log2`, а README и Universe описывают `ln|Re| - ln|Im|`/натуральный логарифм с диапазоном около `[-5.545, 5.545]`.
- В `src/core` есть явные математические дефекты или нестрогие заглушки: p-адическое расстояние для равных значений возвращает бесконечность, соленоидное кодирование часто даёт нули для дробных значений, `delta_distance` не согласован с векторным вводом, `sqrt` для отрицательных чисел молча возвращает `0.0`.
- `src/nucleus` активно зависит от `src/core`, но часть кода — демонстрации/прототипы; есть встроенные `test_*` функции внутри модулей, `if __name__ == "__main__"`, псевдо-SVD вместо настоящей SVD, неполная/ошибочная интеграция с solenoid lossless storage.
- Каталог `tests/` в текущей рабочей копии отсутствует, хотя `pyproject.toml`, `README.md` и `AGENTS.md` его документируют. Релевантных pytest-тестов для `src/core` и `src/nucleus` фактически не найдено.

Рекомендуемая форма рефакторинга: сначала зафиксировать строгую математическую спецификацию и тестовый oracle для `core`, затем привести `nucleus` к использованию только этих контрактов, отделив демонстрации от runtime-кода.

## Документация Universe

Изученные релевантные документы:

- `Universe/ReadMe.md` — вводит Δ как динамическую величину: линейное отклонение, евклидова дистанция, cosine similarity, RoPE/вращение, адаптивная метрика, фрактальная/бифуркационная интерпретация.
- `Universe/Math/_СИСТЕМА_U_СЖАТО.md` — сжатая спецификация U-системы: `Id : Ω`, `D(a)=a:Ω=a⊕a`, `H(a)=a:D(Id)`, `L(Dⁿ(Id))=n`, `Δ = ln|Re| − ln|Im|`, информация как глубина рекурсии.
- `Universe/Math/13_Деление_на_ноль_как_линейное_преобразование.md` — задаёт `D` как линейный оператор ветвления, `H` как обратный оператор сжатия, `H(D(a)) = a`, `D(H(a)) = a`, `Ker D = {Ω}`, `Im D = 𝕌`.
- `Universe/Math/14_Дуальные_числа.md` — релевантно для строгого оформления производной/потенциала через dual numbers.
- `Universe/Math/15_Пределы_и_непрерывность.md` — релевантно для `continuity_*`, `limit_*`.
- `Universe/Math/23_Соленоид.md` — ключевой документ для памяти: соленоид как обратный предел `𝒮 = lim← (𝕌:Ω)`, точка как согласованная история `z₀ = D(z₁) = D²(z₂) = ...`, двоичная история, метрика близости по общему префиксу, связь с p-адическими числами.
- `Universe/Math/24_p-адические_числа.md` — описывает D(Id)-адическую топологию: ветвление в вещественной топологии ведёт к Π, а в p-адической — к Ω; соленоид и D-адические целые представлены как две стороны одного объекта.
- `Universe/Formal_Proofs.md` — содержит формальные наброски аксиом U-системы, но в текущем виде это скорее философско-исследовательский документ, а не готовая строгая спецификация для кода.
- `src/nucleus/COMPRESSION_SUMMARY.md` — связывает Nucleus с solenoid storage: `H(D(a))=a`, SVD extraction, binary prefix, D-level metadata, p-adic residue, заявленная lossless-реконструкция.
- `src/nucleus/NUCLEUS_ROADMAP.md` — текущий план развития: GGUF extraction, solenoid encoder/engine/storage, persistent storage, SVD pipeline, тесты extractors и целевое покрытие nucleus ≥80%.

Наблюдение: документация богата идеями, но для кода нужна промежуточная спецификация меньшего масштаба: точные домены, типы, формулы, ожидаемые свойства, допустимые приближения и тестовые примеры.

## Текущая структура src/core

`src/core` содержит около 80 Python-файлов. Структура сейчас построена по принципу «один оператор/понятие — один файл».

Основные группы:

1. Базовые U-операторы и константы:
   - `D.py` — `D(x)=2x` для скаляра/list.
   - `H.py` — `H(x)=x/2` для скаляра/list.
   - `L.py` — `L(x)=log2(|x|)`.
   - `safe_divide.py` — `a:0 -> 2a`, `a:2 -> a/2`, иначе обычное деление.
   - `constants.py`, `__math_constants.py`, `__init__.py`, `Math.py`.

2. Delta-field и sweep pipeline:
   - `delta_field.py`, `complex_delta_field.py`, `inverse_delta_field.py`, `inverse_complex_delta_field.py`.
   - `compute_thresholds.py`, `compute_jump_events.py`, `compute_sweep.py`, `sweep.py`, `sweep_results.py`, `sweep_process_class.py`.
   - `count_components.py`, `label_2d.py`, `gradient_magnitude.py`.

3. Метрики и топологии:
   - `euclidean_distance.py`, `delta_distance.py`, `similarity.py`.
   - `p_adic_distance.py`, `v2_adic_valuation.py`, `d_adic_convergence.py`.
   - `solenoid_trajectory.py`, `encode_solenoid_trajectory.py`, `solenoid_distance.py`, `solenoid_similarity.py`, `solenoid_pattern_distance.py`, `solenoid_distance_from_masks.py`.

4. Паттерны/fractal/pyramid/spine:
   - `fractal_pattern_signature.py`, `fractal_pyramid_structure.py`, `fractal_pyramid.py`, `fractal_pyramid_level.py`, `fractal_pyramid_to_string.py`.
   - `pattern_bridge_identity.py`, `pattern_distance_from_delta.py`, `pattern_similarity_from_delta.py`, `pattern_similarity_from_complex.py`, `pattern_pyramid_depth.py`, `pattern_spine_chain.py`.
   - `spine_value.py`, `spine_value_array.py`.

5. Численные и алгебраические помощники:
   - `linear_algebra.py` — `CoreVector`, `CoreMatrix`, dot/norm/mean/std/matmul/quantize и т.д.
   - `svd.py`, `svd_reconstruct.py`, `svd_error.py`, `mat_*`, `vec_*`.
   - `ln.py`, `log2.py`, `sin.py`, `cos.py`, `exp.py`, `sqrt.py`, `gcd.py`, `lcm.py`, `binomial_probability.py`.

Ключевые замечания по структуре:

- `linear_algebra.py` — фактический центральный модуль для Nucleus; он list-backed, без NumPy, и содержит много функций разного уровня.
- `__init__.py` экспортирует часть операторов, но далеко не все; `Math.py` — legacy-compat слой с частичным набором экспортов.
- `SweepResults` в `src/core/sweep_results.py` — ручной класс со `__slots__`, без dataclass/typing; параллельно в проекте есть typed containers в `src/models/types.py`.
- Много файлов имеют декоративный copyright/banner, что затрудняет чтение математического ядра.

## Текущая структура src/nucleus

`src/nucleus` содержит 20 Python-модулей и несколько `.md` документов. Это слой deterministic knowledge / memory layout, завязанный на математические операторы из `core`.

Основные группы:

1. Публичный API:
   - `__init__.py` экспортирует `GeometricExtractor`, `GeometricFeatures`, `KnowledgeGraph`, `KnowledgeSystem`, `PatternNode`, `Seed`, `Explorer`, `CorrelationEngine`.

2. Deterministic knowledge core:
   - `deterministic_core.py` — `SemanticPattern`, `PatternRelationship`, `DeterministicKnowledgeCore`, serialize/deserialize.
   - `deterministic_knowledge.py` — другой `DeterministicKnowledgeCore`/`DeterministicFunction` на основе low-rank patterns.
   - `nucleus_knowledge_system.py` — `PatternNode`, `GeometricExtractor`, `KnowledgeSystem`; активно использует delta/complex/fractal/pyramid/solenoid/pattern operators.

3. Compression / SVD-like extraction:
   - `correlation_compressor.py` — `_core_decompose`, `_compose`, `CorrelationCompressor`; заявлено SVD-like, но фактически берутся нормализованные столбцы/строки, это не строгая SVD.
   - `cross_layer_compressor.py` — compress/decompress layer и cross-layer pattern.
   - `fractal_compressor.py` — многоуровневое low-rank residual compression.
   - `semantic_knowledge_storage.py` — semantic operators/pattern extraction/storage.
   - `nucleus_model_patterns.py` — `ModelLoader`, `PatternExtractor`, `ModelProfile`.

4. Graph/geometric systems:
   - `geometric_extractor.py` — graph features через `networkx`; зависит от `core.compute_thresholds`, `D`, `gradient_magnitude`, `safe_divide`.
   - `knowledge_graph.py` — graph over compressed layer embeddings, mixed similarity: cosine + delta + p-adic + solenoid.
   - `universal_geometric_classifier.py` — list-like geometric classifier по histogram/jumps/betti/capacity.

5. Maps/protocols/seeds:
   - `universal_knowledge_map.py` — deterministic projection map.
   - `universal_knowledge_protocol.py` — learn/encode/similarity/save/load для maps.
   - `nucleus_seed_system.py` — seed-based correlation explorer.

6. Прототипы/демонстрации:
   - `llm_crisis_analysis.py`, `nucleus_hybrid.py`, `nucleus_duality.py`, `nucleus_graphics.py`, `nucleus_unified.py`, `universal_knowledge_map.py` и др. имеют `if __name__ == "__main__"`.
   - В нескольких runtime-модулях есть функции вида `test_*`, но это не pytest-тесты, а демонстрационные функции.

Критичные интеграционные замечания:

- `src/nucleus/geometric_extractor.py` вызывает `compute_thresholds([curvature, density, delta_score, s_curve_score], prime=prime)`, но `src/core/compute_thresholds.py` имеет сигнатуру `(sweep_min, sweep_max, sweep_step)`. Это прямое несоответствие API.
- `geometric_extractor.py` импортирует `networkx`, но `networkx` отсутствует в `pyproject.toml` dependencies.
- `knowledge_graph.py` смешивает cosine similarity, delta distance, p-adic distance и solenoid distance без формальной нормализации и без доказанного диапазона результата.
- `nucleus_model_patterns.py` содержит `from nucleus_graphics import GeometricEngine`, что не соответствует правилу импорта `from nucleus import ...` / package-relative imports и может ломаться при package execution.
- В `src/nucleus` есть несколько похожих «ядр знаний» с пересекающимися именами и разными моделями данных.

## Найденные тесты и покрытие

Фактическое состояние:

- Каталог `tests/` в текущей рабочей копии отсутствует: `list_dir tests` вернул `Directory does not exist`.
- `pyproject.toml` настроен на `testpaths = ["tests"]` и `python_files = "test_*.py"`, но таких проектных тестов для Eugenia нет.
- `AGENTS.md` и `README.md` документируют `tests/test_math.py`, `tests/test_integration.py`, `tests/test_nucleus_*.py`, но файлы отсутствуют.
- `search_file_by_name("test_*.py", ".")` нашёл только тесты внутри vendored/external каталогов (`ggml`, `llama.cpp`) и не нашёл проектные тесты Eugenia.
- Поиск `def test_` нашёл демонстрационные функции внутри `src/nucleus`:
  - `src/nucleus/correlation_compressor.py::test_methods`
  - `src/nucleus/fractal_compressor.py::test_radical`
  - `src/nucleus/cross_layer_compressor.py::test_full_model`
  - `src/nucleus/semantic_knowledge_storage.py::test_semantic_system`
  - `src/nucleus/deterministic_knowledge.py::test_compression_ratio`
  - `src/nucleus/universal_geometric_classifier.py::test_mnist_classification`
- Эти функции находятся в runtime-коде и вызываются из `if __name__ == "__main__"`; они печатают результат, но не содержат assertions и не являются надёжным покрытием.

Покрытие по смысловым областям сейчас отсутствует или не зафиксировано:

- Нет тестов для базовых законов `D/H/L/safe_divide`.
- Нет тестов для `delta_field` и обратного преобразования против документации/README.
- Нет тестов для sweep shapes, jump detection, threshold generation.
- Нет тестов для p-adic axioms: `d(x,x)=0`, ultrametric inequality, valuation powers of 2.
- Нет тестов для solenoid encoding/distance: common prefix metric, prefix-length cases, deterministic reconstruction.
- Нет тестов для `linear_algebra` matrix/vector shape contracts.
- Нет тестов для Nucleus deterministic behavior, serialization roundtrip, compression/decompression error bounds, API compatibility.
- Нет тестов для заявленного solenoid lossless storage.

## Проблемы и направления рефакторинга

1. Зафиксировать каноническую математику `core`.

   Нужно выбрать и документировать один минимальный набор понятий:

   - `Ω`, `Id`, `D_ID`, `Π`, `EPS`.
   - `D`, `H`, `L`, `safe_divide`.
   - `DeltaField`/`Δ`.
   - `SolenoidPoint`/trajectory/history metric.
   - `DAdic`/`PAdic` valuation and distance.
   - `CoreVector`/`CoreMatrix` contracts.

   Сейчас это распределено по десяткам файлов и частично противоречит документации.

2. Привести `delta_field` к одному контракту.

   Текущее несоответствие:

   - README: `D = log(X + 1) - log(256 - X)` и диапазон около `[-5.545, 5.545]`.
   - `src/core/delta_field.py`: `log2(x+1)-log2(256-x)` и `PIXEL_MAX_EXCLUSIVE=254.999`, что даёт другой диапазон.
   - Universe: `Δ = ln|Re| − ln|Im|`.

   Нужно решить: `ln` или `log2`, пиксельный домен `[0,255]` или `[0,255)`, как обрабатывать границы, где хранить константы.

3. Исправить p-adic слой.

   Текущие дефекты:

   - `v2_adic_valuation(0)` возвращает `-inf`, тогда как для valuation обычно ожидается `+inf`; из-за этого `p_adic_distance(a,a)` становится `inf`, а должен быть `0`.
   - `v % 2.0 == 0` для float не является строгим p-adic критерием.
   - `p_adic_distance` возвращает либо scalar, либо list, без typed overload/документации.

4. Исправить solenoid слой.

   Текущие дефекты:

   - `encode_solenoid_trajectory(delta_value)` для дробных `x in [0,1)` делает `int(x)&1`, то есть первый и часто все биты равны `0`; это не извлекает binary expansion корректно.
   - `solenoid_distance` возвращает `0.0`, если один путь является префиксом другого, даже если длины различны.
   - Нет типа `SolenoidPoint`, нет encode/decode, нет p-adic residue, нет verification lossless, хотя это описано в `COMPRESSION_SUMMARY.md` и `NUCLEUS_ROADMAP.md`.

5. Развести математические типы и runtime-совместимость.

   - `CoreVector(list)` и `CoreMatrix(list)` удобны, но нестроги: нет явных размерностей, dtype, проверки прямоугольности матриц, поведения для ragged inputs.
   - `linear_algebra.py` слишком большой и объединяет типы, статистику, матричные операции, deterministic random, quantization.
   - Нужны dataclasses/protocols и отдельные модули для vector/matrix/stats/quantization.

6. Убрать демонстрации и псевдо-тесты из runtime-кода.

   - `test_*` функции внутри `src/nucleus` должны быть перенесены в `tests/` или переименованы в `demo_*`, если остаются демонстрациями.
   - `if __name__ == "__main__"` в библиотечных модулях лучше заменить CLI/examples/tests.

7. Привести Nucleus к core-контрактам.

   - Сейчас Nucleus сам придумывает capacity/phase/signature/compression в разных модулях.
   - Нужно сделать `core` источником строгих операторов, а `nucleus` — композиционным слоем: extraction → pattern → graph → storage.
   - Нужны общие dataclasses для `Pattern`, `Relationship`, `CompressedLayer`, `KnowledgeMap`, `SolenoidEncoding`.

8. Разобраться с SVD.

   - `correlation_compressor._core_decompose` называется SVD-like, но не реализует SVD.
   - Документация Nucleus говорит о SVD decomposition и eigenpatterns.
   - Нужно либо использовать настоящую SVD (`numpy`/`scipy`/`torch`) с тестами реконструкции, либо переименовать текущий алгоритм в deterministic rank projection и явно задать его свойства.

9. Исправить API mismatch.

   - `src/nucleus/geometric_extractor.py` несовместим с текущим `src/core/compute_thresholds.py`.
   - Возможны скрытые несовместимости вокруг `delta_distance`, `p_adic_distance`, `solenoid_distance`, потому что функции возвращают разные типы для scalar/vector.

10. Добавить тесты как первый обязательный этап рефакторинга.

   Минимальный набор:

   - `tests/test_core_operators.py`
   - `tests/test_delta_field.py`
   - `tests/test_sweep.py`
   - `tests/test_p_adic.py`
   - `tests/test_solenoid.py`
   - `tests/test_linear_algebra.py`
   - `tests/test_nucleus_compression.py`
   - `tests/test_nucleus_graph.py`
   - `tests/test_nucleus_storage.py`

## Файлы для изменения

Высокий приоритет — `src/core`:

- `src/core/constants.py`
- `src/core/__math_constants.py`
- `src/core/__init__.py`
- `src/core/Math.py`
- `src/core/D.py`
- `src/core/H.py`
- `src/core/L.py`
- `src/core/safe_divide.py`
- `src/core/delta_field.py`
- `src/core/inverse_delta_field.py`
- `src/core/complex_delta_field.py`
- `src/core/inverse_complex_delta_field.py`
- `src/core/delta_distance.py`
- `src/core/compute_thresholds.py`
- `src/core/compute_jump_events.py`
- `src/core/compute_sweep.py`
- `src/core/sweep.py`
- `src/core/sweep_results.py`
- `src/core/linear_algebra.py`
- `src/core/p_adic_distance.py`
- `src/core/v2_adic_valuation.py`
- `src/core/d_adic_convergence.py`
- `src/core/encode_solenoid_trajectory.py`
- `src/core/solenoid_trajectory.py`
- `src/core/solenoid_distance.py`
- `src/core/solenoid_similarity.py`
- `src/core/solenoid_pattern_distance.py`
- `src/core/solenoid_encode_pattern.py`
- `src/core/fractal_pattern_signature.py`
- `src/core/fractal_pyramid_structure.py`
- `src/core/pattern_bridge_identity.py`
- `src/core/pattern_distance_from_delta.py`
- `src/core/pattern_similarity_from_delta.py`
- `src/core/pattern_similarity_from_complex.py`
- `src/core/pattern_pyramid_depth.py`
- `src/core/pattern_spine_chain.py`
- `src/core/ln.py`
- `src/core/log2.py`
- `src/core/sqrt.py`
- `src/core/sin.py`
- `src/core/cos.py`
- `src/core/exp.py`
- `src/core/svd.py`
- `src/core/svd_reconstruct.py`
- `src/core/svd_error.py`

Высокий приоритет — `src/nucleus`:

- `src/nucleus/__init__.py`
- `src/nucleus/deterministic_core.py`
- `src/nucleus/deterministic_knowledge.py`
- `src/nucleus/geometric_extractor.py`
- `src/nucleus/knowledge_graph.py`
- `src/nucleus/nucleus_knowledge_system.py`
- `src/nucleus/correlation_compressor.py`
- `src/nucleus/cross_layer_compressor.py`
- `src/nucleus/fractal_compressor.py`
- `src/nucleus/semantic_knowledge_storage.py`
- `src/nucleus/nucleus_model_patterns.py`
- `src/nucleus/nucleus_seed_system.py`
- `src/nucleus/universal_knowledge_map.py`
- `src/nucleus/universal_knowledge_protocol.py`
- `src/nucleus/universal_geometric_classifier.py`
- `src/nucleus/nucleus_graphics.py`
- `src/nucleus/nucleus_hybrid.py`
- `src/nucleus/nucleus_duality.py`
- `src/nucleus/nucleus_unified.py`
- `src/nucleus/llm_crisis_analysis.py`

Новые/восстановленные тестовые файлы, которые нужно создать или вернуть:

- `tests/test_math.py` или заменить на более точные файлы ниже.
- `tests/test_integration.py`.
- `tests/test_core_operators.py`.
- `tests/test_delta_field.py`.
- `tests/test_sweep.py`.
- `tests/test_p_adic.py`.
- `tests/test_solenoid.py`.
- `tests/test_linear_algebra.py`.
- `tests/test_nucleus_compression.py`.
- `tests/test_nucleus_graph.py`.
- `tests/test_nucleus_storage.py`.
- `tests/test_nucleus_protocol.py`.

Конфигурация/зависимости:

- `pyproject.toml` — добавить недостающие зависимости, если `networkx` остаётся runtime dependency; уточнить testpaths после восстановления `tests/`.

## Файлы для учета без изменения

Документация, которую нужно использовать как источник смысла, но не обязательно менять на шаге рефакторинга кода:

- `Universe/ReadMe.md`
- `Universe/Formal_Proofs.md`
- `Universe/Math/_СИСТЕМА_U_СЖАТО.md`
- `Universe/Math/03_Деление.md`
- `Universe/Math/06_Степени_двойки.md`
- `Universe/Math/08_Логарифм.md`
- `Universe/Math/09_Комплексные.md`
- `Universe/Math/12_Алгебра_процентов.md`
- `Universe/Math/13_Деление_на_ноль_как_линейное_преобразование.md`
- `Universe/Math/14_Дуальные_числа.md`
- `Universe/Math/15_Пределы_и_непрерывность.md`
- `Universe/Math/22_Геометрия.md`
- `Universe/Math/23_Соленоид.md`
- `Universe/Math/24_p-адические_числа.md`
- `Universe/Math/28_Масштабная_инвариантность.md`
- `Universe/Math/29_Динамические_системы.md`
- `Universe/Math/30_Информация.md`

Проектная документация/контекст:

- `README.md`
- `AGENTS.md`
- `src/nucleus/COMPRESSION_SUMMARY.md`
- `src/nucleus/NUCLEUS_ROADMAP.md`
- `src/nucleus/EUGENIA_ARCHITECTURE.md`
- `src/nucleus/SOLENOID_ROADMAP.md`
- `src/nucleus/UNIVERSAL_KNOWLEDGE.md`

Связанные runtime-модули, которые нужно учитывать при изменении контрактов `core`, но не обязательно менять первыми:

- `generate.py`
- `src/renderers/*.py`
- `src/models/types.py`
- `src/models/config.py`
- `src/data/*.py`
- `src/extractors/*.py`
- `src/utils/*.py`

Внешние/нерелевантные тесты, не использовать как покрытие Eugenia:

- `ggml/examples/python/test_tensor.py`
- `llama.cpp/**/tests/**`
- `whisper.cpp/**/test/**`

## Риски

- Нет текущего pytest safety net: любой рефакторинг core/nucleus может изменить поведение незаметно.
- Документация и код расходятся по базовым формулам (`ln` vs `log2`, диапазоны Δ, p-adic valuation, solenoid encoding). Нужно сначала выбрать канон, иначе рефакторинг станет косметическим.
- Nucleus зависит от нестабильных/нестрогих core-функций; исправление core может сломать Nucleus, но это полезное выявление скрытых контрактов.
- Заявленная lossless solenoid storage пока не реализована в строгом виде; нельзя строить persistent memory на текущих заглушках без proof-by-test.
- Псевдо-SVD может давать неверные ожидания по compression ratio и reconstruction quality; замена на настоящую SVD изменит результаты и размеры.
- `networkx` не указан в зависимостях, но используется в `src/nucleus/geometric_extractor.py`; CI/новая среда может падать на import.
- В репозитории много вложенных внешних проектов (`ggml`, `llama.cpp`, `whisper.cpp`) и вложенный `.git` в `Universe`; поиск тестов/рефакторинг должны явно ограничиваться Eugenia runtime, иначе можно смешать внешние артефакты с проектным кодом.
- Большое количество мелких файлов в `src/core` повышает риск циклических импортов и inconsistent API exports при перестройке.
- Если сохранить обратную совместимость `core.Math` и текущих exports, понадобится переходный слой/deprecation-план.
