# Pyramid Merge — Normalization Schema

Документ-инструкция для Task 02 (сборка `pyramid_merged.json`) и Task 04 (автоматическая валидация). Фиксирует канонический контур корня, словарь алиасов, правила provenance, разнесение `Q`, форму конфликтных узлов и правила форматирования. Все решения основаны на `research/findings.md` (разделы «Cross-file Comparison», «Risks & Open Questions», «Sample Excerpts») и `PLAN.md` («Specification» R1–R9, «Shared Context → Key Decisions»).

Источниковые идентификаторы (5 логических источников при 4 физических файлах):

- `pyramid.json#Synthesis_Full`
- `pyramid.json#Final_Complete`
- `pyramid_more_merge.json`
- `pyramid_need_to_merge.json`
- `pyramid_need_to_merge_this.json`

---

## 1. Canonical root layout

Верхнеуровневый корень — единственный ключ `OneLaw`. Под ним плоский union всех разделов всех 4 файлов, без вложенных `branches.*`. Уникальные ветки-источники различаются через `_source` на уровне узлов, а не через отдельные namespaces.

Канонический порядок и имена разделов:

```json
{
  "OneLaw": {
    "meta": { },
    "primitives": [0, 1],
    "matrix_lo_shu": {
      "grid": [[6,1,8],[7,5,3],[2,9,4]],
      "magic_constant": 15,
      "total_sum": 45,
      "total_product": 362880,
      "rows": 3,
      "center": 5,
      "center_identity": "0 = 5",
      "sides": { "South": { }, "East": { }, "West": { }, "North": { } },
      "cycle": {
        "sequence": ["0","South(1,2)","East(3,4)","Center(5)","West(6,7)","North(8,9)","0"],
        "steps_total": 10,
        "direct_Re": "…",
        "reverse_Im": "…",
        "intermediate_Q": [2,3,4,5],
        "max_Q": 10,
        "meaning": "…",
        "symmetry_note": "…"
      }
    },
    "axioms_and_operators": {
      "division_by_zero": { },
      "delta": { "mathematical": "…", "physical": "…", "equilibrium": "…", "significance": "…" },
      "Q_hadron": { "definition": "…", "range": "0..5, 10 for AGI", "mapping": [ ] },
      "Q_neuro": {
        "note": "Пирамида Хеопса задаёт направленность операций; обе шкалы семантически значимы.",
        "scales": { "direct": { }, "symmetric": { } }
      }
    },
    "resonances": {
      "schumann_fundamental": { },
      "pyramid_center_Hz": 5.0,
      "pyramid_king_chamber": { },
      "sarcophagus_resonance": { },
      "derived_frequencies_Hz": { }
    },
    "frequencies": { "full_map": { }, "golden_relation": "…" },
    "derived_math": { "sqrt5": "…", "golden_ratio": "…", "trigonometry": { }, "powers_of_2": "…" },
    "physical_constants": {
      "alpha_inverse": { },
      "alpha_GUT_inverse": 40,
      "alpha_G": "…",
      "weak_mixing_angle_sin2_theta_W": "…",
      "Cabibbo_angle_deg": 13,
      "PMNS_theta12_deg": 33,
      "PMNS_theta23_deg": 45,
      "PMNS_theta13_deg": 8.4,
      "CP_epsilon_K": "…"
    },
    "cosmology": {
      "visible_matter_percent": 5,
      "dark_matter_percent": 27,
      "dark_energy_percent": 68,
      "total_percent": 100,
      "Hubble_constant": 68,
      "age_universe_Gyr": 13.8,
      "derivations": [ ]
    },
    "mass_law": {
      "formula": "m = m_p · exp(Δ_phys/2) · exp(0.30 · Q_hadron)",
      "m_p_MeV": 938.272,
      "validation": { "R_squared": ">0.99", "dataset": "83 LHCb particles" },
      "particles": { "total_analyzed": 83, "groups": { }, "examples": { } },
      "examples": { "Tcc(3875)+": { }, "Pc(4450)+": { }, "Ξcc++": { } }
    },
    "pyramid": {
      "location": "29.9792° N, 31.1342° E",
      "type": "…",
      "built_by": "…",
      "steps_total": 210,
      "steps_formula": "…",
      "chambers": {
        "subterranean": { },
        "queen_chamber": { },
        "king_chamber": { },
        "relieving_chambers": { },
        "air_shafts": { }
      },
      "sarcophagus": { },
      "cycle_path": "…",
      "purpose": "…",
      "pyramid_mathematics": {
        "basic_geometry": { },
        "geometric_derivation_from_matrix": { },
        "chambers_and_cycle": { },
        "mathematical_constants_in_pyramid": { },
        "pyramid_as_quantum_computer": "…"
      },
      "acoustic_model": { "musical_notes": { }, "standing_waves": "…" }
    },
    "greek_alphabet": {
      "language": "Ελληνικά",
      "letters_short": { "Δ": "…", "Λ": "…", "α": "…", "∅": "…" },
      "letters_as_operators": { "Δ": "…", "Λ": "…", "α": "…", "∅": "…", "ε": "…", "η": "…", "ι": "…", "κ": "…", "ν": "…", "σ": "…" },
      "word_equation": "…"
    },
    "names_of_reality": {
      "Zhenya": "…", "Evgenios": "…", "Evgeny": "…", "Evgenia": "…", "Eugenics": "…"
    },
    "color_music_spheres": {
      "principle": "…",
      "goosebumps_frequency": "…",
      "mapping": [ ]
    },
    "proof_in_code": {
      "script": "rec.py",
      "virtual_memory_GB": 426,
      "L1_frames": 3,
      "result": "…",
      "interpretation": "…"
    },
    "mathematical_extensions": {
      "algebra_of_colon": { },
      "matrix_derivations": { },
      "spectral_delta": { },
      "exact_constants": { },
      "mass_law_full": { },
      "riemann_proof_sketch": { },
      "solenoid_metric": { },
      "universal_wavefunction": { },
      "particle_derivation": { }
    },
    "EEG_rhythms": {
      "Delta": { }, "Theta": { }, "Alpha": { }, "Beta": { }, "Gamma": { }, "High_Gamma": { }
    },
    "biophotonics": {
      "photon_frequency_range_Hz": "…",
      "origin": "…",
      "modulation": "…",
      "carrier_relation": "…",
      "experiment_40_Hz": "…",
      "pyramid_role": "…"
    },
    "full_vibration_spectrum": {
      "from_0_1Hz_to_infinity": { }
    },
    "fractal_riemann_sphere": {
      "construction": "…",
      "coordinates": "…",
      "operator_D": "…",
      "relation_to_division_by_zero": "…",
      "use": "…"
    },
    "planck_units": {
      "planck_mass": "…",
      "planck_length": "…",
      "planck_time": "…",
      "relation_to_phi": "…",
      "possible_derivation": "…"
    },
    "strict_relationships": [ ]
  }
}
```

Правила целостности:

- Инвариантное ядро (grid Ло Шу, стороны S/E/W/N с operators/sums/products, цикл `0→…→0`, проценты 5/27/68, m_p=938.272, R²>0.99 на 83 LHCb, 210 ступеней, координаты Гизы) присутствует **ровно один раз** (S4 из PLAN.md).
- Блок `meta` всегда первым внутри `OneLaw`; `strict_relationships` — последним.
- Все массивы «natural-language» (`strict_relationships`, `strict_mathematical_relationships` → канонически `strict_relationships`) сохраняют исходный порядок; не сортируются (findings §Risks п.6).

---

## 2. Alias dictionary

Таблица `original → canonical`. Канонический ключ — тот, что используется в Canonical root layout выше.

| Original (встречается в) | Canonical | Примечание |
|---|---|---|
| `op` (`sides_of_reality.*`) | `operator` | findings §Risks п.5; применяется ко всем 4 сторонам |
| `center_value` (`more_merge`, `Final_Complete`) | `center` | findings §Risks п.10 |
| `sarcophagus` (`Synthesis_Full.frequencies_pyramid_and_earth`) | `sarcophagus_resonance` | findings §Risks п.4 |
| `coffer_resonance` (`need_to_merge_this.frequencies`) | `sarcophagus_resonance` | findings §Risks п.4 |
| `Schumann_base` (`need_to_merge_this.frequencies`) | `schumann_fundamental` | findings §Risks п.4 |
| `schumann_resonance` (`Synthesis_Full`) | `schumann_fundamental` | унификация Schumann-узла |
| `Hubble_parameter` (`need_to_merge_this`) | `Hubble_constant` | findings §Risks п.4; каноническое имя — `Hubble_constant` (внутри `cosmology`) |
| `hubble` / `hubble_constant` (need_to_merge cosmology) | `Hubble_constant` | унификация регистра |
| `matrix_3x3` (`need_to_merge_this`) | `matrix_lo_shu.grid` | findings §Cross-file: need_to_merge_this перекладывает grid в отдельный ключ |
| `matrix_properties` (`need_to_merge_this`) | поля вливаются в `matrix_lo_shu` (`magic_constant`, `total_sum`, `total_product`, `center`) | плоский merge |
| `full_cycle` (`more_merge`, `Final_Complete`) | `matrix_lo_shu.cycle` | findings §Cross-file |
| `cycle` (`need_to_merge_this`) | `matrix_lo_shu.cycle` | тот же узел |
| `cycle_path` / `cycle_path_full` (`Synthesis_Full`, `need_to_merge`) | `matrix_lo_shu.cycle.sequence` | порядок сохраняется |
| `cycle.trajectory` (`need_to_merge_this`) | `matrix_lo_shu.cycle.sequence` | findings §Risks п.10 |
| `frequencies.pyramid_center` (`need_to_merge_this`) | `resonances.pyramid_center_Hz` | findings §Risks п.4 |
| `pyramid_center_king_chamber` (`Synthesis_Full.frequencies_pyramid_and_earth`) | `resonances.pyramid_center_Hz` (5 Гц) | распакован из комбо-ключа |
| `pyramid_king_chamber_118_Hz` (`Synthesis_Full`) | `resonances.pyramid_king_chamber` | нормализация имени |
| `sarcophagus_440_Hz` (`Synthesis_Full`) | `resonances.sarcophagus_resonance` | |
| `frequencies_pyramid_and_earth` (`Synthesis_Full`) | `resonances` | раздел-контейнер |
| `core_axiom` (`Final_Complete`, `more_merge`) | `axioms_and_operators.division_by_zero` + `axioms_and_operators.delta` | разнести по двум каноническим подузлам |
| `physical_delta` (`Synthesis_Full`, `need_to_merge`) | `axioms_and_operators.delta` | единый узел |
| `delta_definition` (`need_to_merge_this`) | `axioms_and_operators.delta` | поля `mathematical`/`physical`/`equilibrium`/`significance` |
| `Q_definition` (`need_to_merge_this`) | `axioms_and_operators.Q_hadron` + `axioms_and_operators.Q_neuro` | см. §3 Q disambiguation |
| `neural_bands` (`Final_Complete`, `more_merge`) | `axioms_and_operators.Q_neuro.scales.symmetric` | findings §Risks п.1 |
| `derived_constants` (`Final_Complete`, `more_merge`) | поля → `physical_constants.alpha_inverse`, `cosmology.age_universe_Gyr`, `cosmology` % | плоское разнесение |
| `age_and_fine_structure` (`need_to_merge`) | поля → `physical_constants.alpha_inverse` + `cosmology.age_universe_Gyr` | |
| `cosmology_and_percents` (`need_to_merge`) | `cosmology` | |
| `percents` (`need_to_merge_this`) | `cosmology` (+ сохранить доп. поля `13%`, `14%`, `5%` как есть внутри `cosmology.extra`) | findings §Per-file: need_to_merge_this |
| `physical_constants_derived` (`Synthesis_Full`) | `physical_constants` | |
| `unification` (`need_to_merge_this`) | `physical_constants` (поля `alpha_GUT_inverse`, `alpha_G`, углы PMNS) | |
| `weak_mixing_angle_sin2_theta_W` / `weinberg_angle_sin2` | `physical_constants.weak_mixing_angle_sin2_theta_W` | унифицировать |
| `Cabibbo_angle_deg` / `cabibbo_angle` / `quark_mixing_cabibbo` | `physical_constants.Cabibbo_angle_deg` | |
| `theta_12_PMNS` / `θ12` / `PMNS θ12` | `physical_constants.PMNS_theta12_deg` (аналогично для 23, 13) | |
| `hadron_mass_law` (`Final_Complete`, `more_merge`) | `mass_law` | |
| `mass_law_and_frequencies` (`Synthesis_Full`) | `mass_law` | |
| `pyramid_as_physical_embodiment` (`Synthesis_Full`, `need_to_merge`) | `pyramid` | |
| `pyramid_as_processor` (`Final_Complete`, `more_merge`) | `pyramid` | |
| `steps_count` / `steps_count_original` / `pyramid_steps_required` | `pyramid.steps_total` (=210) | |
| `pyramid_steps_formula` | `pyramid.steps_formula` | |
| `proof_recursion` (`need_to_merge`, `need_to_merge_this`) | `proof_in_code` | findings §Cross-file |
| `greek` (`need_to_merge_this`) | `greek_alphabet` | |
| `greek_alphabet_in_law` (`Final_Complete`, `more_merge`) | `greek_alphabet` | |
| `letters` (`greek_alphabet_in_law`) | `greek_alphabet.letters_short` | отличить от расширенных 10 букв |
| `letters_as_operators` (`need_to_merge_this.greek`) | `greek_alphabet.letters_as_operators` | |
| `names` (`need_to_merge_this`) | `names_of_reality` | |
| `strict_mathematical_relationships` (`Final_Complete`, `more_merge`) | `strict_relationships` | массив объединяется с `strict_relationships` из других источников, порядок сохраняется посекционно |
| `EEG_rhythms_full_correlation` (`Synthesis_Full`) | `EEG_rhythms` | |
| `biophotonics_in_OneLaw` (`Synthesis_Full`) | `biophotonics` | |
| `full_vibration_spectrum_in_OneLaw` (`Synthesis_Full`) | `full_vibration_spectrum` | |
| `derived_frequencies_from_OneLaw` / `derived_frequencies_HZ` | `resonances.derived_frequencies_Hz` | унификация регистра |
| `matrix_3x3` | `matrix_lo_shu.grid` | (повтор для ясности) |

Итого в таблице 40+ записей (минимум 10 требовался по AC, п.4 findings §Risks покрыт полностью: `op`, `center_value`, `sarcophagus`, `coffer_resonance`, `Schumann_base`, `Hubble_parameter`; findings §Risks п.5 покрыт — normalize mapping-форматов см. §4; findings §Risks п.10 покрыт — `center` vs `center_value`, `Q` дезамбигуация вынесена в §3).

---

## 3. Q disambiguation rules

Поле `Q` в исходниках означает **либо** `Q_hadron` (0..5, 10 для AGI; шкала массы частиц), **либо** `Q_neuro` (0..10; шкала ЭЭГ-частот). В merged оставлять голое `Q` запрещено (R7 из PLAN.md). Правила для каждого места появления:

| Контекст (источник) | Смысл | Канонический перенос |
|---|---|---|
| `Q_definition.Q`, `Q_definition.range=[0,10]`, `Q_definition.mapping` (need_to_merge_this) | Hadron-шкала (mapping 2→мезоны, 3→барионы, 4→тетракварки, 5→пентакварки) с потолком 10 для AGI | `axioms_and_operators.Q_hadron` (range, mapping, relation_with_Δ `Q=e^{|Δ|}`); плюс `axioms_and_operators.Q_neuro.scales.*.mapping` получает свои Q-метки отдельно |
| `Q_definition.mapping` ключи вида `"Q=4": "тетракварки"` (need_to_merge_this) | Hadron | Нормализовать в `Q_hadron.mapping: [{Q: 2, kind: "mesons"}, {Q: 3, kind: "baryons"}, {Q: 4, kind: "tetraquarks"}, {Q: 5, kind: "pentaquarks"}, {Q: 10, kind: "AGI"}]` |
| `intermediate_Q: [2,3,4,5]` (need_to_merge_this.cycle) | Hadron (переходные состояния) | Остаётся в `matrix_lo_shu.cycle.intermediate_Q` (без смены имени, значение — целые Hadron-Q) |
| `max_Q: 10` (need_to_merge_this.cycle) | Hadron (AGI-потолок) | `matrix_lo_shu.cycle.max_Q_hadron: 10` |
| `King chamber` (Synthesis_Full.pyramid_as_physical_embodiment.chambers.king) — `Q_neuro=4`, f=5 Гц | Neuro | `pyramid.chambers.king_chamber.Q_neuro: 4` |
| `King chamber` (need_to_merge_this.pyramid_mathematics.chambers_and_cycle.king_chamber) — поле `Q: 5` | Hadron (структурная роль пентакварка) | `pyramid.chambers.king_chamber.Q_hadron: 5`; итого в king_chamber **два поля**: `Q_neuro: 4` и `Q_hadron: 5` (R7) |
| `Queen chamber`, `Subterranean`, `Grand Gallery` и др. — поля `Q` | По контексту Neuro (Q_neuro=3 для Queen и т.п.) | Переименовать `Q → Q_neuro` везде в `pyramid.chambers.*`, если источник не говорит про частицы |
| `examples.Tcc(3875)+`, `Pc(4450)+`, `Ξcc++` (mass_law) — `Q: 4/5/3` | Hadron (mass_law) | `mass_law.examples.*.Q_hadron: …` |
| `EEG_rhythms.*.Q_neuro` (Synthesis_Full — уже канонично) | Neuro | Оставить как есть, значение — число |
| `EEG_rhythms.*.Q_hadron_analogy` (Synthesis_Full) | Hadron (аналогия) | Оставить, с `_source: pyramid.json#Synthesis_Full` |
| `neural_bands.mapping` ключи `Q0..Q10` (more_merge, Final_Complete) | Neuro | Нормализовать в массив `Q_neuro.scales.symmetric.mapping: [{Q_neuro: 0, f_Hz: 2.5}, …]` |
| Любая таблица вида `f(Q) = C·2^{Q/2}` | Neuro | Внутри `Q_neuro.scales.<direct|symmetric>.formula`, переменная в формуле явно переименована: `f(Q_neuro) = …` |
| Формула `m = m_p · exp(Δ/2) · exp(0.30 · Q)` (mass_law) | Hadron | `mass_law.formula: "m = m_p · exp(Δ_phys/2) · exp(0.30 · Q_hadron)"` |

Правило без исключений: если поле называется просто `Q` — перед записью в merged оно **должно** быть переименовано в `Q_hadron` **или** `Q_neuro` согласно таблице выше. Немаркированных `Q` в merged не остаётся.

---

## 4. Conflict-node shapes

### 4.1 α⁻¹ (`physical_constants.alpha_inverse`)

Источники: Synthesis_Full (137.035999084), Final_Complete/more_merge/need_to_merge/need_to_merge_this (137, формула `3×45+2`). Политика: точное значение + аппроксимация + формула + все derivations с provenance.

```json
"alpha_inverse": {
  "value": 137.035999084,
  "approximation": 137,
  "derivation": "3×45+2",
  "derivations": [
    { "formula": "3×45+2 = 137", "source": "pyramid.json#Final_Complete" },
    { "formula": "3×45+2 = 137", "source": "pyramid_more_merge.json" },
    { "formula": "3×TotalSum + South_sum_2 = 3×45 + 2 = 137", "source": "pyramid_need_to_merge.json" },
    { "formula": "age_Gyr × 10 = 13.8 × 10 = 138 ≈ 137 (inverse derivation)", "source": "pyramid_need_to_merge_this.json" }
  ],
  "_source": [
    "pyramid.json#Synthesis_Full",
    "pyramid.json#Final_Complete",
    "pyramid_more_merge.json",
    "pyramid_need_to_merge.json",
    "pyramid_need_to_merge_this.json"
  ]
}
```

### 4.2 Schumann (`resonances.schumann_fundamental`)

Источники: Synthesis_Full (`7.83`), Final_Complete/more_merge/need_to_merge (строка `"47/6 ≈ 7.83333"` + формула), need_to_merge_this (`7.83`). Политика: числовое значение + приближение + формула как строка, гармоники собираются массивом.

```json
"schumann_fundamental": {
  "value_Hz": 7.83333,
  "approximation_Hz": 7.83,
  "formula": "47/6",
  "derivation": "(TotalSum + 2) / West_digit_6 = (45 + 2) / 6 = 47/6",
  "harmonics_Hz": [14.3, 20.8, 27.3, 33.8, 40.3],
  "_source": [
    "pyramid.json#Synthesis_Full",
    "pyramid.json#Final_Complete",
    "pyramid_more_merge.json",
    "pyramid_need_to_merge.json",
    "pyramid_need_to_merge_this.json"
  ]
}
```

### 4.3 Q_neuro (`axioms_and_operators.Q_neuro`)

Ключевое решение (PLAN.md §Key Decisions): **обе** шкалы сохраняются. Направленность операций задаётся пирамидой Хеопса, и обе шкалы семантически значимы.

```json
"Q_neuro": {
  "definition": "Нейронный аналог Q: номер гармоники ЭЭГ-ритмов",
  "range": [0, 10],
  "note": "Пирамида Хеопса задаёт направленность операций (Re↔Im, прямое/обратное). Обе шкалы семантически значимы: direct описывает прямую развёртку f0=1.25 Гц (основание пирамиды → вершина), symmetric — развёртку f0=2.5 Гц, где 5 Гц достигается уже при Q=2 (симметричное разложение вокруг центра 5). Обе дают одно и то же множество достижимых частот, но сдвинуты на октаву по индексу Q.",
  "scales": {
    "direct": {
      "base_frequency_Hz": 1.25,
      "formula": "f(Q_neuro) = 1.25 · 2^{Q_neuro/2}",
      "mapping": [
        { "Q_neuro": 0,  "f_Hz": 1.25 },
        { "Q_neuro": 2,  "f_Hz": 2.5  },
        { "Q_neuro": 4,  "f_Hz": 5.0  },
        { "Q_neuro": 6,  "f_Hz": 10.0 },
        { "Q_neuro": 8,  "f_Hz": 20.0 },
        { "Q_neuro": 10, "f_Hz": 40.0 }
      ],
      "_source": [
        "pyramid.json#Synthesis_Full",
        "pyramid_need_to_merge.json"
      ]
    },
    "symmetric": {
      "base_frequency_Hz": 2.5,
      "formula": "f(Q_neuro) = 2.5 · 2^{Q_neuro/2}",
      "mapping": [
        { "Q_neuro": 0,  "f_Hz": 2.5  },
        { "Q_neuro": 2,  "f_Hz": 5.0  },
        { "Q_neuro": 4,  "f_Hz": 10.0 },
        { "Q_neuro": 6,  "f_Hz": 20.0 },
        { "Q_neuro": 8,  "f_Hz": 40.0 },
        { "Q_neuro": 10, "f_Hz": 80.0 }
      ],
      "_source": [
        "pyramid.json#Final_Complete",
        "pyramid_more_merge.json"
      ]
    }
  }
}
```

### 4.4 Mapping-блоки (нормализация объект↔массив)

В исходниках встречаются две формы одной и той же таблицы:

- массив объектов: `color_music_spheres.mapping: [{digit, note, color, aspect}]` (Final_Complete, more_merge);
- объект с ключами-строками: `neural_bands.mapping: {"Q0": 2.5, "Q2": 5.0, …}` (Final_Complete, more_merge); `Q_definition.mapping: {"Q=2": "мезоны", …}` (need_to_merge_this).

Правило: **всегда** массив объектов с явным первичным ключом. Первичный ключ объявляется для каждого mapping:

| Mapping | Первичный ключ | Схема элемента |
|---|---|---|
| `color_music_spheres.mapping` | `digit` (0..9) | `{ "digit": <int>, "note": <str>, "color": <str>, "aspect": <str> }` |
| `axioms_and_operators.Q_neuro.scales.<direct|symmetric>.mapping` | `Q_neuro` | `{ "Q_neuro": <int>, "f_Hz": <number> }` |
| `axioms_and_operators.Q_hadron.mapping` | `Q_hadron` | `{ "Q_hadron": <int>, "kind": <str>, "mass_range": <str|optional>, "count": <int|optional> }` |
| `mass_law.particles.groups` (объект с ключами `mesons_Q2`...) | `kind` | `{ "kind": <str>, "Q_hadron": <int>, "count": <int>, "mass_range": <str> }` |
| `resonances.derived_frequencies_Hz` | `multiplier` (или `label`) | `{ "label": "10 Гц", "value_Hz": 10.0, "derivation": "…" }` |

Для массивов, полученных из объекта-словаря, порядок элементов задаётся сортировкой по первичному ключу (численно, если ключ число — см. §7).

---

## 5. Provenance rules

### 5.1 Где обязательно писать `_source`

- На **любом конфликтном узле** (numeric conflict, type conflict, formula mismatch): α⁻¹, Schumann, Q_neuro.scales.*, matrix_lo_shu.cycle (если найден конфликт sequence), chambers.king_chamber (Q_hadron vs Q_neuro), rec.py proof (разная детализация в разных файлах).
- На **любом уникальном узле**, присутствующем только в части исходников: `EEG_rhythms`, `biophotonics`, `full_vibration_spectrum`, `planck_units`, `fractal_riemann_sphere`, `mathematical_extensions.*`, `matrix_lo_shu.total_product`, `matrix_lo_shu.cycle.intermediate_Q`, `matrix_lo_shu.cycle.max_Q`, `greek_alphabet.letters_as_operators`, `greek_alphabet.word_equation`, `mass_law.particles`, `pyramid.pyramid_mathematics`, `resonances.derived_frequencies_Hz`, `cosmology.derivations` (содержат derivations из разных источников).
- На **разделе-контейнере** можно ставить агрегированный `_source` **только если весь раздел целиком из одного источника** (например, `EEG_rhythms._source: ["pyramid.json#Synthesis_Full"]`). Иначе `_source` ставится на внутренних узлах.

### 5.2 Где `_source` НЕ обязателен

- Инвариантное ядро (findings §Cross-file «Общее во всех 4 файлах»): `matrix_lo_shu.grid`, `matrix_lo_shu.magic_constant`, `matrix_lo_shu.total_sum`, `matrix_lo_shu.center`, `matrix_lo_shu.sides.*.digits/operator/sum/product`, `matrix_lo_shu.cycle.sequence` (базовая последовательность), `axioms_and_operators.division_by_zero.axiom`, `cosmology.visible_matter_percent/dark_matter_percent/dark_energy_percent`, `physical_constants.PMNS_theta12/23/13_deg`, `physical_constants.Cabibbo_angle_deg`, `mass_law.m_p_MeV`, `mass_law.validation`, `pyramid.location`, `pyramid.steps_total`, базовые значения резонансов 5/118/440 Гц.
- В этих местах `_source` опускается для краткости. Полный список источников узла всегда восстанавливается по `meta.sources[]` + отсутствию противоречий.

### 5.3 Формат идентификатора источника

Строго одна из 5 строк (строковый enum):

- `"pyramid.json#Synthesis_Full"`
- `"pyramid.json#Final_Complete"`
- `"pyramid_more_merge.json"`
- `"pyramid_need_to_merge.json"`
- `"pyramid_need_to_merge_this.json"`

Никаких URL, путей, относительных префиксов. `#` только в двух случаях (pyramid.json с двумя блоками).

### 5.4 `_source` как поле

- Всегда массив строк, даже если источник один: `"_source": ["pyramid.json#Synthesis_Full"]`.
- Порядок элементов в массиве: по тому же каноническому порядку источников, что и в §5.3 (т.е. Synthesis_Full, Final_Complete, more_merge, need_to_merge, need_to_merge_this). Сортируется автоматически валидатором (Task 04).
- Дубликаты запрещены.

### 5.5 `derivations[]`

Когда у узла есть несколько формальных формул вывода одного и того же значения из разных источников, они собираются массивом объектов:

```json
"derivations": [
  { "formula": "3×45+2 = 137", "source": "pyramid.json#Final_Complete" },
  { "formula": "45/(2+√φ) ≈ 13.8 (обратно к 137)", "source": "pyramid.json#Synthesis_Full" }
]
```

Правила:

- Каждый элемент — объект `{"formula": <str>, "source": <str>}`. Никаких других ключей.
- `source` — один из 5 идентификаторов §5.3 (строка, не массив).
- Порядок элементов в `derivations[]` — в каноническом порядке источников §5.3.
- Если у узла есть одна-единственная формула — допустимо хранить её скалярно (`"derivation": "…"`) без `derivations[]`. Если формул 2+ из разных источников — обязательно массив.

---

## 6. meta.sources[] layout

Поле `OneLaw.meta.sources` — массив ровно из 5 элементов (5 логических источников при 4 физических файлах; `pyramid.json` участвует дважды: как `Synthesis_Full` и как `Final_Complete`).

Схема элемента:

```json
{
  "filename": "pyramid.json",
  "root_key": "OneLaw_Synthesis_Full",
  "version": null,
  "derivation_base": null,
  "status": null,
  "source_id": "pyramid.json#Synthesis_Full",
  "note": "Первый из двух корневых блоков pyramid.json. Без поля version."
}
```

Поля:

| Поле | Тип | Обязательно | Правило заполнения |
|---|---|---|---|
| `filename` | string | да | Имя файла в корне репо, без пути. |
| `root_key` | string | да | Ключ корневого объекта: `OneLaw_Synthesis_Full`, `OneLaw_Final_Complete`, `OneLaw_Complete_Exact`, `OneLaw_Complete`. |
| `version` | string \| null | да | Значение `meta.version` из исходника; `null` если нет. |
| `derivation_base` | string \| null | да | Значение `meta.derivation_base` из исходника; `null` если нет. |
| `status` | string \| null | да | Значение `meta.status` из исходника; `null` если нет. |
| `source_id` | string | да | Один из 5 идентификаторов §5.3. Совпадает с идентификаторами в `_source`. |
| `note` | string \| null | нет | Комментарий (например, что `pyramid.json` раздвоён). |

Полный ожидаемый массив (5 элементов, каноническая очерёдность):

1. `pyramid.json#Synthesis_Full` — `root_key: "OneLaw_Synthesis_Full"`, `version: null`, `derivation_base: null`, `status: null`, `note: "Первый корневой блок pyramid.json; расширенная аналитика, EEG + биофотоника + спектр"`.
2. `pyramid.json#Final_Complete` — `root_key: "OneLaw_Final_Complete"`, `version: "3.0"`, `derivation_base: "1:0 = 0:1 = Δ, ∅ = 0 = 5"` (из meta соответствующего блока), `status: <из исходника>`, `note: "Второй корневой блок pyramid.json; идентичен pyramid_more_merge.json"`.
3. `pyramid_more_merge.json` — `root_key: "OneLaw_Final_Complete"`, `version: "3.0"`, `derivation_base: "1:0 = 0:1 = Δ, ∅ = 0 = 5"`, `status: <из исходника>`, `note: null`.
4. `pyramid_need_to_merge.json` — `root_key: "OneLaw_Complete_Exact"`, `version: "2.0"`, `derivation_base: "1:0=2 и матрица Ло Шу 3×3"`, `status: <из исходника>`, `note: null`.
5. `pyramid_need_to_merge_this.json` — `root_key: "OneLaw_Complete"`, `version: null`, `derivation_base: null`, `status: null`, `note: "Без meta/version; самый объёмный, содержит уникальные mathematical_extensions, planck_units, fractal_riemann_sphere"`.

Также внутри `meta`:

- `meta.title`: человекочитаемое название, по согласованию собирается из title-ов исходников (Task 02 выбирает один или агрегирует).
- `meta.version`: `"merged-1.0"` (синтетический — результат слияния).
- `meta.generated_from`: массив `[{filename: ..., sha256: ...}]` — опционально, если Task 02 считает hash исходников до их удаления.

---

## 7. Ordering rules

### 7.1 Сохранять исходный порядок (не сортировать)

- `strict_relationships` (и все его исходные алиасы `strict_mathematical_relationships`) — natural-language список, порядок критичен как повествовательный (findings §Risks п.6). При merge: конкатенация без сортировки, с сохранением исходного порядка внутри каждого источника; дубликаты строк удаляются, но относительный порядок первого появления сохраняется.
- `matrix_lo_shu.cycle.sequence` (и исходные `cycle_path`, `trajectory`): порядок семантический (`0 → South → East → Center → West → North → 0`), НЕ сортировать.
- `resonances.schumann_fundamental.harmonics_Hz`: по возрастанию частоты (как в исходнике Synthesis_Full).
- `matrix_lo_shu.grid`: массив массивов, порядок строк/столбцов фиксирован.
- Примеры в `mass_law.examples`: порядок как в исходниках (Tcc(3875)+ → Pc(4450)+ → Ξcc++).

### 7.2 Канонически сортировать

- Массивы, полученные из mapping-объектов (§4.4), сортируются по первичному ключу:
  - `color_music_spheres.mapping` — по `digit` (0..9, возрастание).
  - `Q_neuro.scales.*.mapping` — по `Q_neuro` (возрастание).
  - `Q_hadron.mapping` — по `Q_hadron` (возрастание).
  - `mass_law.particles.groups` — по `Q_hadron` (возрастание), тай-брейк по `kind` лексикографически.
- `meta.sources[]` — в каноническом порядке §6 (фиксированный).
- Ключи объектов в JSON: порядок задаётся явным шаблоном §1 (meta первый, strict_relationships последний). Python `json.dump` сохраняет порядок вставки при `sort_keys=False` — использовать именно его. **`sort_keys=True` запрещён**.
- `_source` внутри любого узла — в каноническом порядке §5.3.

---

## 8. JSON formatting rules

- Кодировка: UTF-8, без BOM.
- `json.dump(..., ensure_ascii=False, indent=2, sort_keys=False)` — точный вызов.
- Отступ: 2 пробела. Без табов.
- Переносы строк: `\n` (LF). Без `\r\n`.
- Финальный символ файла: одна пустая строка после закрывающей `}`.
- Кириллица, греческий алфавит, математические символы (Δ, Λ, α, ∅, √, °, ≈, ×, ²) пишутся в тексте как есть, без `\uXXXX` экранирования.
- Числа:
  - Там, где значение по сути число (величина, частота, угол, проценты, количество) — хранится как JSON number, не строка. Примеры: `"value_Hz": 7.83333`, `"Hubble_constant": 68`, `"m_p_MeV": 938.272`.
  - Точное значение α⁻¹ хранится как `137.035999084` (число), `approximation: 137` (число).
  - `dark_matter_percent: 27` (число), не `"27%"`.
- Формулы — всегда строки: `"formula": "f(Q_neuro) = 1.25 · 2^{Q_neuro/2}"`, `"derivation": "3×45+2"`. Выражение `47/6` внутри `derivation`/`formula` — строка; числовой эквивалент дублируется в отдельном поле `value_Hz`.
- Булевы и null: стандартные JSON-литералы `true`, `false`, `null`.
- Ключи объектов — только ASCII (`snake_case`), за исключением явно осмысленных неASCII-ключей (`"Δ"`, `"Λ"`, `"α"`, `"∅"` в `greek_alphabet.letters_short` / `letters_as_operators`). Эти 4+ ключа разрешены как есть.
- Запрещены trailing commas, single-quoted strings, JSON5-расширения. Итоговый файл должен успешно парситься `json.loads` без настроек.
- Файл должен быть идемпотентным: повторная сериализация после `json.loads` даёт тот же байт-в-байт результат (при `ensure_ascii=False`, `indent=2`, тот же порядок ключей).
