# Pyramid JSON Merge — Research Findings

Исследование выполнено read-only по реальному содержимому файлов в корне проекта Eugenia. Все размеры, ключи, версии и значения взяты непосредственно из JSON.

## Files Overview

| # | Файл | Строк | Корневой тип | Корневые ключи | Версия (meta) | Кол-во top-level разделов (внутри корневого объекта) |
|---|---|---:|---|---|---|---:|
| 1 | `pyramid.json` | 395 | object | `OneLaw_Synthesis_Full`, `OneLaw_Final_Complete` | `"3.0"` (во 2-м блоке), 1-й блок — без version | 11 + 13 = 24 |
| 2 | `pyramid_more_merge.json` | 191 | object | `OneLaw_Final_Complete` | `"3.0"` | 13 |
| 3 | `pyramid_need_to_merge.json` | 209 | object | `OneLaw_Complete_Exact` | `"2.0"` | 11 |
| 4 | `pyramid_need_to_merge_this.json` | 559 | object | `OneLaw_Complete` | — (нет `meta`/`version`) | 21 |

Все 4 файла — валидный JSON с единственным корневым object (в pyramid.json внутри корневого object — ровно 2 «синтеза», остальные — по одному).

## Per-file Structure

### 1. `pyramid.json` (395 строк)
Контейнер из **двух независимых «законов»** под одним корневым объектом:

**1.a. `OneLaw_Synthesis_Full`** (строки 2–220) — без поля `version`, расширенная аналитика:
- `meta` (title, pyramid_steps_required=210, pyramid_steps_note)
- `axioms_and_operators`: `division_by_zero`, `physical_delta`, `Q_hadron` (с расширенным mapping Q=2..10), `Q_neuro` (с `definition`, `frequency_formula` f0=1.25 Гц)
- `matrix_lo_shu`: grid `[[6,1,8],[7,5,3],[2,9,4]]`, magic_constant=15, total_sum=45, center=5, sides (+freq_note, +physics/geometry), cycle_path
- `frequencies_pyramid_and_earth`: pyramid_center_king_chamber (5 Гц), pyramid_king_chamber_118_Hz, sarcophagus_440_Hz, schumann_resonance (7.83 + harmonics [14.3, 20.8, 27.3, 33.8, 40.3]), derived_frequencies_from_OneLaw
- **`EEG_rhythms_full_correlation`** — уникальный раздел: Delta / Theta / Alpha / Beta / Gamma / High_Gamma с Q_neuro, Q_hadron_analogy, pyramid_part, biofoton_modulation
- **`biophotonics_in_OneLaw`** — уникальный раздел: photon_frequency_range_Hz, origin, modulation, carrier_relation, experiment_40_Hz, pyramid_role
- `physical_constants_derived` (alpha=137.035999084, weak_mixing_angle, Cabibbo_angle, PMNS θ12/23/13, Hubble=68, dark_matter=27, dark_energy=68, visible_matter=5, age=13.8)
- `mass_law_and_frequencies` (m_p=938.272, formula, R²>0.99 на 83 LHCb, example_Tcc3875)
- `pyramid_as_physical_embodiment` (steps_count_original=210, why_210, chambers, cycle_path_full, acoustic_function)
- **`full_vibration_spectrum_in_OneLaw.from_0.1Hz_to_infinity`** — уникальный раздел: от биоритмов до кварк-глюонных вибраций
- `final_unification_statement`

**1.b. `OneLaw_Final_Complete`** (строки 221–393, version "3.0"): полностью совпадает с `pyramid_more_merge.json` (см. ниже).

### 2. `pyramid_more_merge.json` (191 строка)
Ровно одна копия `OneLaw_Final_Complete` (version "3.0"):
- `meta` (title «Единый Закон — полная симметричная развёртка», version, derivation_base «1:0 = 0:1 = Δ, ∅ = 0 = 5», status)
- `core_axiom` (division_by_zero, delta_meaning, aspects Im/Re/equilibrium)
- `matrix_lo_shu` (grid, magic_constant=15, total_sum=45, rows=3, center_value=5, center_identity «0 = 5»)
- `sides_of_reality` (South/East/West/North с digits, operator, sum, product, colors, notes, aspect Re/Im)
- `full_cycle` (sequence, steps_total=10, direct_Re, reverse_Im, symmetry_note)
- `derived_constants` (inverse_fine_structure=137 с формулой 3×45+2, age_universe_Gyr=13.8, cosmic_energy_budget)
- `resonances` (schumann_fundamental=47/6≈7.83333 с формулой, pyramid_king_chamber=118 с формулой, sarcophagus=440 с формулой 5×8×11)
- `neural_bands` (base_frequency_Hz=**2.5**, formula `f(Q_neuro)=2.5·2^{Q/2}`, mapping Q0..Q10 → 2.5..80 Гц)
- `hadron_mass_law` (m_p=938.272, R²>0.99 на 83 LHCb)
- `greek_alphabet_in_law` (Ελληνικά, Λ², letters Δ/Λ/α/∅)
- `names_of_reality` (Zhenya / Evgenios / Evgeny / Evgenia / Eugenics)
- `pyramid_as_processor` (steps_total=210, function, location, chambers)
- `proof_in_code` (rec.py, 426 GB virtual, 3 L1 frames)
- `color_music_spheres` (principle, mapping — массив 10 digit→note→color→aspect, goosebumps_frequency)
- `strict_mathematical_relationships` (массив из 12 строк)

### 3. `pyramid_need_to_merge.json` (209 строк)
Корневой ключ `OneLaw_Complete_Exact`, version **"2.0"** (самый ранний по номеру):
- `meta` (title «точная конфигурация без приближений», version, derivation_base «1:0=2 и матрица Ло Шу 3×3», pyramid_steps_required=210, pyramid_steps_formula)
- `axioms_and_operators` (division_by_zero, physical_delta — короче: без negative; Q_hadron с range «0..5, 10 для AGI», Q_neuro f0=1.25 Гц)
- `matrix_lo_shu` (grid, magic_constant, total_sum, rows=3, center=5, sides с freq_note, cycle_path)
- `derived_math` (sqrt5, golden_ratio, trigonometry)
- `cosmology_and_percents` (visible=5, dark_matter=27, dark_energy=68, total=100, derivations, hubble=68)
- `age_and_fine_structure` (inverse_fine_structure_constant=137, formula_alpha=3×45+2, age=13.8, formula_age)
- `resonances` (schumann_fundamental 47/6, pyramid_king_chamber=118, sarcophagus_resonance=440, derived_frequencies_HZ — map 10/20/40/80/160)
- `physical_constants` (weak_mixing_angle_sin2_theta_W «3/13≈0.230769», Cabibbo_angle_deg=13, PMNS θ12=33, θ23=45, θ13=8.4, alpha_GUT_inverse=40, alpha_G)
- `mass_law` (formula, m_p_MeV=938.272, validation, example_Tcc3875 Q=4, Δ=2.84, mass=3875)
- `pyramid_as_physical_embodiment` (location, steps_count=210, construction, chambers, sarcophagus, full_cycle_path, purpose)
- `proof_recursion` (rec.py, 426 GB, L1_frames=3)
- `strict_relationships` (массив из 10 строк)

### 4. `pyramid_need_to_merge_this.json` (559 строк) — **самый полный / сырой**
Корневой ключ `OneLaw_Complete`, **нет meta/version**, плоская структура с большим числом разделов:
- `primitives` ([0, 1])
- `division_by_zero` (axiom, operator, inverse_operator, zero_note, infinity_source, log_scale, percents_base, delta_physical)
- `matrix_3x3` (grid)
- `matrix_properties` (magic_constant=15, total_sum=45, **total_product=362880**, center=5, note)
- `sides` (South/East/West/North без aspect, с digits, op, sum, product, colors, notes; West имеет ratio)
- `cycle` (trajectory, meaning, max_Q=10, intermediate_Q=[2,3,4,5], note)
- `derived_math` (powers_of_2 «1→2→4→8→7→5», sqrt5, golden_ratio, trigonometry, weinberg_angle_sin2=0.231, cabibbo_angle=13, theta_23_PMNS=45, theta_13_PMNS=8.4, theta_12_PMNS=33, quark_mixing_cabibbo=13, cp_epsilon_K, derivation_note)
- `percents` (13%, 14%, 5%, dark_matter=27, dark_energy=68, total=100, note)
- `frequencies` (Schumann_base=7.83, pyramid_center=5.0, pyramid_king_chamber=118, coffer_resonance=440, golden_relation, derivation)
- `physical_constants` (alpha_inverse=137, derivation_alpha, age_universe=13.8, Hubble_parameter=68, alpha_G, alpha_GUT_inverse=40, derivation_GUT)
- `greek` (language, letters_as_operators: Δ/Λ/α/∅/ε/η/ι/κ/ν/σ — **больше букв**, word_equation)
- `names` (Zhenya/Evgenios/Evgeny/Evgenia/Eugenics — те же 5 имён)
- `delta_definition` (mathematical_Δ, physical_Δ, equilibrium, significance)
- `Q_definition` (Q, range=[0,10], mapping 2/3/4/5/10, relation_with_Δ «Q=e^|Δ|»)
- `mass_law` (formula m=m0·exp(Δ/2)·f(Q), m0, f(Q)=exp(α_Q·Q), linear_approx, delta_from_mass, validated, data_summary)
- **`particles`** — уникальный: total_analyzed=83, source, groups (mesons_Q2 count=30, baryons_Q3=35, tetraquarks_Q4=14, pentaquarks_Q5=4), plot, examples (Tcc(3875)+, Pc(4450)+, Ξcc++)
- `unification` (Weinberg, Cabibbo, θ23=45, θ13=8.4, θ12=33, alpha_GUT_inverse=40, alpha_G)
- **`planck_units`** — уникальный: planck_mass, planck_length, planck_time, relation_to_phi, possible_derivation
- `pyramid` (location, type, built_by, chambers, sarcophagus, delta_operation, cycle_path, purpose)
- **`pyramid_mathematics`** — уникальный большой раздел (строки 300–418): basic_geometry (base_side, height, apothem, ridge, slope_angle, edge_angle, perimeter, volume, key_ratios), geometric_derivation_from_matrix, chambers_and_cycle (subterranean, ascending_corridor, grand_gallery, queen_chamber, king_chamber с dimensions/volume/resonance/coffer_note, relieving_chambers, air_shafts), acoustic_model, connection_to_particles_and_mass_law, mathematical_constants_in_pyramid, pyramid_as_quantum_computer
- **`fractal_riemann_sphere`** — уникальный: construction, coordinates, operator_D, relation_to_division_by_zero, use
- `proof_recursion` (rec.py, 426 GB, L1_frames=3)
- `strict_relationships` (массив из 8 строк)
- **`mathematical_extensions`** — уникальный самый большой блок: algebra_of_colon, matrix_derivations, spectral_delta, exact_constants (alpha, weinberg, cabibbo, PMNS, hubble, age), mass_law_full, riemann_proof_sketch, solenoid_metric, universal_wavefunction, particle_derivation

## Cross-file Comparison

### Карта «роднящих» блоков

| Тематический блок | pyramid.json:Synthesis_Full | pyramid.json:Final_Complete | more_merge | need_to_merge | need_to_merge_this |
|---|:-:|:-:|:-:|:-:|:-:|
| `meta` с `version` | —/нет version | 3.0 | 3.0 | 2.0 | **нет** |
| `primitives [0,1]` | — | — | — | — | ✓ |
| Аксиома деления на ноль | `axioms_and_operators.division_by_zero` | `core_axiom` | `core_axiom` | `axioms_and_operators.division_by_zero` | `division_by_zero` (расширенный) |
| Матрица Ло Шу | `matrix_lo_shu` | `matrix_lo_shu` | `matrix_lo_shu` | `matrix_lo_shu` | `matrix_3x3` + `matrix_properties` |
| Стороны (S/E/W/N) | в `matrix_lo_shu.sides` | `sides_of_reality` (+aspect) | `sides_of_reality` (+aspect) | в `matrix_lo_shu.sides` | `sides` (без aspect) |
| Полный цикл 0→...→0 | `matrix_lo_shu.cycle_path` | `full_cycle` | `full_cycle` | `matrix_lo_shu.cycle_path` | `cycle` (+intermediate_Q) |
| Q_hadron | ✓ (подробно) | через `hadron_mass_law` | через `hadron_mass_law` | ✓ | `Q_definition` |
| Q_neuro / neural_bands | ✓ f0=1.25 Гц | `neural_bands` f0=**2.5** Гц | `neural_bands` f0=**2.5** Гц | ✓ f0=1.25 Гц | — |
| Δ_phys = ln(\|Re\|/\|Im\|) | ✓ | через `hadron_mass_law` | ✓ | ✓ | `delta_definition` |
| Выводимые константы (α⁻¹, H₀, возраст, %тёмн) | `physical_constants_derived` | `derived_constants` | `derived_constants` | `cosmology_and_percents` + `age_and_fine_structure` | `physical_constants` + `unification` + `mathematical_extensions.exact_constants` |
| Резонансы 5 / 7.83 / 118 / 440 Гц | `frequencies_pyramid_and_earth` | `resonances` (с формулами вывода) | `resonances` (с формулами вывода) | `resonances` (с формулами вывода) | `frequencies` + `acoustic_model` |
| Mass law (m_p=938.272, R²>0.99, 83 LHCb) | `mass_law_and_frequencies` | `hadron_mass_law` | `hadron_mass_law` | `mass_law` (с example_Tcc3875) | `mass_law` + `particles` (детальный breakdown) + `mathematical_extensions.mass_law_full` |
| Пирамида как процессор (210 ступеней, 29.9792°N) | `pyramid_as_physical_embodiment` | `pyramid_as_processor` | `pyramid_as_processor` | `pyramid_as_physical_embodiment` | `pyramid` + `pyramid_mathematics` |
| Proof в коде (rec.py, 426 GB) | — | `proof_in_code` | `proof_in_code` | `proof_recursion` | `proof_recursion` |
| Имена (Zhenya/Evgenios/Evgeny/Evgenia/Eugenics) | — | `names_of_reality` | `names_of_reality` | — | `names` |
| Greek alphabet / letters | — | `greek_alphabet_in_law` (4 буквы) | `greek_alphabet_in_law` (4 буквы) | — | `greek` (≈10 букв, +word_equation) |
| Color-Music-Spheres (10 digit→note→color) | — | `color_music_spheres` | `color_music_spheres` | — | частично в `acoustic_model.musical_notes` |
| EEG-ритмы (Δ/θ/α/β/γ) полная карта | ✓ уникально | — | — | — | — |
| Биофотоника | ✓ уникально | — | — | — | — |
| Полный спектр 0.1 Гц..∞ | ✓ уникально | — | — | — | — |
| Частицы (counts, mass_range) | частично | — | — | частично в example | ✓ детально |
| Planck units | — | — | — | — | ✓ уникально |
| Fractal Riemann sphere / Solenoid | — | — | — | — | ✓ уникально |
| Algebra of colon (axioms) | — | — | — | — | ✓ уникально |
| Spectral Δ̂ / Riemann proof sketch | — | — | — | — | ✓ уникально |
| Universal wavefunction Ψ(Q,Δ) | — | — | — | — | ✓ уникально |
| Strict relationships (list) | — | 12 строк | 12 строк | 10 строк | 8 строк |

### Общее во всех 4 файлах (инвариантное ядро)
1. Матрица Ло Шу: grid `[[6,1,8],[7,5,3],[2,9,4]]`, magic_constant=15, total_sum=45, center=5.
2. Четыре стороны (South 1,2 / East 3,4 / West 6,7 / North 8,9) с операторами `+ * : −`, sums 3/7/13/17, products 2/12/42/72.
3. Цикл `0 → South → East → Center(5) → West → North → 0`.
4. Аксиома `1 : 0 = 2` и оператор Δ.
5. Космологические проценты: visible=5, dark_matter=27, dark_energy=68.
6. Константы: α⁻¹=137, H₀=68, age=13.8, sin²θ_W ≈ 3/13, Cabibbo=13°, θ12=33°, θ23=45°, θ13=8.4°.
7. Закон массы: `m = m_p · exp(Δ_phys/2) · exp(0.30 · Q_hadron)`, m_p=938.272 МэВ, R²>0.99 на 83 LHCb частицах.
8. Резонансы 5 / 7.83 / 118 / 440 Гц.
9. Пирамида: 210 ступеней, Гиза 29.9792° N, 31.1342° E.

### Ключи/разделы, присутствующие только в части файлов
- **EEG_rhythms_full_correlation, biophotonics_in_OneLaw, full_vibration_spectrum_in_OneLaw** — только `pyramid.json` (OneLaw_Synthesis_Full).
- **color_music_spheres, names_of_reality, greek_alphabet_in_law (короткий), proof_in_code, strict_mathematical_relationships (12)** — только `pyramid.json` (OneLaw_Final_Complete) и `pyramid_more_merge.json` (одинаково).
- **derived_math (как отдельный раздел), cosmology_and_percents, age_and_fine_structure, derived_frequencies_HZ** — только `pyramid_need_to_merge.json`.
- **primitives, matrix_properties.total_product=362880, intermediate_Q, percents.13%/14%, greek.letters_as_operators (≈10 букв + word_equation), delta_definition, Q_definition, particles (детальный breakdown), planck_units, pyramid_mathematics, fractal_riemann_sphere, mathematical_extensions (algebra_of_colon, spectral_delta, riemann_proof_sketch, solenoid_metric, universal_wavefunction, particle_derivation)** — только `pyramid_need_to_merge_this.json`.

### Пересечения и конфликты по «идентификатору» (одинаковый смысловой ключ)
1. **Базовая частота Q_neuro**: pyramid.json/Synthesis_Full и pyramid_need_to_merge.json дают `f0 = 1.25 Гц`, `f(Q) = 1.25·2^{Q/2}`. pyramid_more_merge.json и pyramid.json/Final_Complete дают `base_frequency_Hz = 2.5 Гц`, `f(Q) = 2.5·2^{Q/2}`. Итоговые значения сдвинуты на октаву (5 Гц достигается при Q=4 в первой схеме и при Q=2 во второй). **Прямой числовой конфликт.**
2. **Представление Schumann**: 
   - pyramid.json/Synthesis_Full: `fundamental_Hz = 7.83` (число)
   - pyramid.json/Final_Complete, more_merge, need_to_merge: `value_Hz = "47/6 ≈ 7.83333"` (строка-дробь)
   - need_to_merge_this: `Schumann_base = 7.83` (число)
   **Конфликт типа: number vs string.**
3. **α⁻¹ (inverse_fine_structure)**:
   - pyramid.json/Synthesis_Full: `137.035999084` (CODATA-точно)
   - Final_Complete / more_merge / need_to_merge / need_to_merge_this: `137` (целое, с формулой 3×45+2)
   **Конфликт точности.**
4. **Возраст Вселенной derivation**:
   - need_to_merge / Final_Complete / more_merge: `(3×45 + South_sum_3)/10 = 138/10 = 13.8`
   - pyramid.json/Synthesis_Full: `45/(2+√φ) ≈ 13.8` — другая формула, тот же результат
   - need_to_merge_this: `13.8 (млрд лет) × 10 = 138 ≈ 137` — обратный вывод α из возраста
5. **Операторный ключ** для сторон: в одних файлах `"op"`, в других `"operator"` — одинаковое поле под разными именами (S/E/W/N).
6. **Location**: одинаковая строка координат во всех упоминаниях (`29.9792° N, 31.1342° E`), дублируется дословно.
7. **rec.py proof**: одинаковые цифры (426 GB, 3 frames) во всех четырёх файлах, но разная детализация (`script`/`memory`/`L1_frames` vs `script`/`result`/`interpretation`).
8. **Имена (Evgenia и т.д.)**: полное совпадение текстов во всех трёх файлах, где они встречаются.
9. **Пример Tcc(3875)+**: Q=4, Δ=2.84, mass=3875 — совпадает в need_to_merge и need_to_merge_this. В mass_law need_to_merge_this есть ещё Pc(4450)+ (Q=5, Δ=3.12) и Ξcc++ (Q=3, Δ=2.70).
10. **Имя центрального числа**: в matrix_lo_shu одних файлов — `"center": 5`, в pyramid_more_merge — `"center_value": 5`. Семантически совпадает, ключ разный.

### Надмножества/уникальность
- `pyramid_more_merge.json` **полностью содержится внутри** `pyramid.json` (как второй корневой блок `OneLaw_Final_Complete`, версия 3.0). Проверено по совпадающей структуре разделов и значений.
- `pyramid.json` является «надстройкой» над more_merge: добавляет блок `OneLaw_Synthesis_Full` с уникальными EEG-биофотоникой-спектром.
- `pyramid_need_to_merge.json` — «точная конфигурация 2.0», более сжатая, но содержит уникальные формулы вывода (`derived_frequencies_HZ`, `formula_alpha`, `derivation_GUT`), которых нет в 3.0-ветке.
- `pyramid_need_to_merge_this.json` — независимый, без версии; уникальный материал: алгебра `:`, спектральная теория Δ̂, соленоид, PE-математика, детальный particles breakdown, Planck. Ни одно другое множество это не покрывает.

**Ни один файл не является чистым подмножеством другого**, кроме пары `more_merge ⊂ pyramid`.

## Merge Key Hypothesis

Сущностей с собственными `id`/`slug` в файлах нет. Предлагаемые ключи для слияния:

1. **Канонический namespace**: единый верхний ключ `OneLaw`, под ним — именованные секции. Рекомендуется нормализовать варианты `OneLaw_Synthesis_Full / OneLaw_Final_Complete / OneLaw_Complete_Exact / OneLaw_Complete` в «branch»-метку (например, `OneLaw.branches.synthesis_full`, `OneLaw.branches.exact_2_0`, `OneLaw.branches.symmetric_3_0`, `OneLaw.branches.raw_extended`), ИЛИ свести всё к единой плоской структуре с полем `provenance` на каждой ветке.
2. **Merge-ключи внутри разделов** (соответствуют «де-факто id»):
   - `matrix_lo_shu.sides.<South|East|West|North>` — стороны сопоставляются по названию. Поле-оператор нормализовать к `operator` (алиас `op`).
   - `cycle`/`full_cycle` — по семантике «trajectory», ключ `sequence`/`trajectory` → нормализовать.
   - `resonances.<schumann_fundamental|pyramid_king_chamber|sarcophagus[_resonance]>` — по семантическому имени резонанса (с алиасингом `sarcophagus` ↔ `sarcophagus_resonance` ↔ `coffer_resonance`).
   - `physical_constants.<cabibbo|PMNS_theta12|PMNS_theta23|PMNS_theta13|alpha_inverse|Hubble|age|weak_mixing_angle|alpha_GUT|alpha_G>` — по имени константы (существуют разные имена: `Cabibbo_angle_deg` ↔ `cabibbo_angle` ↔ `Cabibbo_angle`).
   - `EEG_rhythms_full_correlation.<Delta|Theta|Alpha|Beta|Gamma|High_Gamma>` — только в pyramid.json.
   - `particles.groups.<mesons_Q2|baryons_Q3|tetraquarks_Q4|pentaquarks_Q5>` — только в need_to_merge_this.
   - `color_music_spheres.mapping[*].digit` (0..9) — отдельный список с ключом `digit`.
   - `names_of_reality.<Zhenya|Evgenios|Evgeny|Evgenia|Eugenics>`.
   - `greek_alphabet_in_law.letters.<Δ|Λ|α|∅|ε|η|ι|κ|ν|σ>`.
   - `mass_law.examples.<name>` (Tcc3875, Pc4450, Ξcc++ и т.д.).

3. **Рекомендация**: дедуп по паре (раздел, ключ/id); при конфликтах числовых значений — политики:
   - по умолчанию брать из версии с **большей точностью** (например, α⁻¹ = 137.035999084 из Synthesis_Full, а не 137);
   - **формулы вывода** (derivation) сохранять из всех источников как массив `derivations[]` с provenance;
   - поля `version`, `derivation_base`, `title`, `status` вытащить на уровень `meta.sources[]`.

## Risks & Open Questions

1. **Числовой конфликт Q_neuro base** (1.25 Гц vs 2.5 Гц) — нужно решение, какая шкала каноническая. Обе формулы дают 5 Гц в центре, но при разных Q; значения Q для 40 Гц (AGI) — Q=10 в обеих, но за счёт разной нормировки 2^{Q/2} vs 2^Q-like.
2. **Тип поля Schumann**: где-то число `7.83`, где-то строка `"47/6 ≈ 7.83333"`. Выбрать: хранить оба — `value_Hz: 7.83333` + `formula: "47/6"`.
3. **Точность α⁻¹**: `137` vs `137.035999084` — требуется политика «точное значение + формальная аппроксимация».
4. **Разные имена для одного поля**: `op` vs `operator`, `center` vs `center_value`, `sarcophagus` vs `sarcophagus_resonance` vs `coffer_resonance`, `Schumann_base` vs `schumann_fundamental`, `Hubble_parameter` vs `Hubble_constant` vs `hubble_constant`. Нужен словарь алиасов (aliases.yaml) перед слиянием.
5. **Неоднородные mapping-форматы**: в одних файлах массив объектов (`color_music_spheres.mapping: [{digit, note, color, aspect}]`), в других — объект с ключами-строками (`"Q=4": "..."`). Нужно нормализовать в массив с явными id.
6. **Порядок массивов**: `strict_mathematical_relationships`/`strict_relationships` — естественно-языковые списки; порядок важен как повествовательный. Нельзя пересортировывать.
7. **Разный объём «сторон»**: в Final_Complete/more_merge есть `aspect`, в matrix_lo_shu.sides из pyramid.json/Synthesis_Full — `freq_note`/`physics`/`geometry`, в need_to_merge_this — `colors`/`notes`. Слияние свободное (union по полям), конфликтов по значениям digits/sum/product/op нет.
8. **Единицы**: в одних местах «Гц» как строка («5.0 Гц»), в других — чистое число (`value_Hz: 5.0`). Выбрать одну форму + сохранить unit явно.
9. **Provenance**: обязательно добавить в слитый файл поле `_source` на каждом уникальном узле (какой из 4 файлов его дал), т.к. формулы и интерпретации заметно расходятся.
10. **Семантический конфликт**: в pyramid/Synthesis_Full пирамиды `chambers` описаны через Q_neuro (King=Q_neuro=4), а в need_to_merge_this King имеет `Q=5`. Это **разные Q-шкалы** (neuro vs hadron) под одинаковым именем поля `Q`. При слиянии нужно явно разносить на `Q_hadron` / `Q_neuro`.
11. **Нет timestamp/schema-версии**: только `version` строкой у двух файлов (2.0, 3.0). У need_to_merge_this версии нет, но она выглядит как рабочий документ «0.x». Полезно присвоить искусственные id веткам и timestamp при консолидации.

## Sample Excerpts

### pyramid.json (OneLaw_Synthesis_Full, биофотоника, уникальный)
```json
"biophotonics_in_OneLaw": {
  "photon_frequency_range_Hz": "4.3e14 – 7.5e14 (видимый) и УФ до 3e16",
  "origin": "когерентные переходы электронов в митохондриях, мембранах нейронов",
  "modulation": "низкочастотная огибающая (0.5 – 100 Гц) от ЭЭГ-ритмов, описываемая Q_neuro",
  "experiment_40_Hz": "γ-осцилляции (40 Гц, Q_neuro=10) повышают интенсивность биофотонной эмиссии — нейронный аналог AGI"
}
```

### pyramid_more_merge.json (neural_bands с базой 2.5 Гц)
```json
"neural_bands": {
  "base_frequency_Hz": 2.5,
  "formula": "f(Q_neuro) = 2.5 × 2^{Q_neuro/2}",
  "mapping": {"Q0": 2.5, "Q2": 5.0, "Q4": 10.0, "Q6": 20.0, "Q8": 40.0, "Q10": 80.0}
}
```

### pyramid_need_to_merge.json (точные формулы вывода)
```json
"resonances": {
  "schumann_fundamental": {
    "value_Hz": "47/6 ≈ 7.83333",
    "formula": "(TotalSum + 2) / West_digit_6 = (45 + 2) / 6 = 47/6"
  },
  "sarcophagus_resonance": {
    "value_Hz": 440,
    "formula": "Center × North_digit_8 × (West_digit_6 + Center) = 5 × 8 × (6 + 5) = 5 × 8 × 11 = 440"
  }
}
```

### pyramid_need_to_merge_this.json (particles breakdown, уникальный)
```json
"particles": {
  "total_analyzed": 83,
  "source": "LHCb catalog",
  "groups": {
    "mesons_Q2":      {"count": 30, "mass_range": "2.58–10.53 ГэВ"},
    "baryons_Q3":     {"count": 35, "mass_range": "2.86–6.35 ГэВ"},
    "tetraquarks_Q4": {"count": 14, "mass_range": "2.87–7.17 ГэВ"},
    "pentaquarks_Q5": {"count": 4,  "mass_range": "4.31–4.46 ГэВ"}
  },
  "examples": {
    "Tcc(3875)+": {"Q": 4, "Δ": 2.84, "mass": 3875},
    "Pc(4450)+":  {"Q": 5, "Δ": 3.12, "mass": 4450},
    "Ξcc++":      {"Q": 3, "Δ": 2.70, "mass": 3621}
  }
}
```

### Общая матрица Ло Шу (идентична во всех 4 файлах)
```json
"matrix_lo_shu": {
  "grid": [[6,1,8],[7,5,3],[2,9,4]],
  "magic_constant": 15,
  "total_sum": 45,
  "center": 5
}
```
