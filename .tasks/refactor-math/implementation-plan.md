# ШАГ 3: реализация строгого математического среза

Пользователь подтвердил план.

## Цель
Навести порядок в математическом ядре проекта: сделать минимальный строгий срез `src/core`, стабилизировать контракты, добавить тесты, не ломая публичный API без необходимости.

## Обязательные ограничения
- Работать минимально и аккуратно: не переписывать весь проект целиком.
- Сначала исправить математические дефекты, затем добавить тесты.
- Сохранять обратную совместимость импортов, где возможно.
- Не трогать vendored/external директории (`ggml`, `llama.cpp`, `whisper.cpp`).
- Руководствоваться документацией `Universe`, особенно:
  - `Universe/Math/_СИСТЕМА_U_СЖАТО.md`
  - `Universe/Math/13_Деление_на_ноль_как_линейное_преобразование.md`
  - `Universe/Math/23_Соленоид.md`
  - `Universe/Math/24_p-адические_числа.md`

## Файлы высокого приоритета

Core:
- `src/core/D.py`
- `src/core/H.py`
- `src/core/L.py`
- `src/core/safe_divide.py`
- `src/core/delta_field.py`
- `src/core/inverse_delta_field.py`
- `src/core/complex_delta_field.py`
- `src/core/inverse_complex_delta_field.py`
- `src/core/delta_distance.py`
- `src/core/v2_adic_valuation.py`
- `src/core/p_adic_distance.py`
- `src/core/encode_solenoid_trajectory.py`
- `src/core/solenoid_distance.py`
- `src/core/solenoid_similarity.py`
- `src/core/linear_algebra.py`
- `src/core/__init__.py`

Nucleus, только если прямо ломается от core-контрактов:
- `src/nucleus/geometric_extractor.py`
- `src/nucleus/knowledge_graph.py`
- `src/nucleus/correlation_compressor.py`

Tests to create:
- `tests/test_core_operators.py`
- `tests/test_delta_field.py`
- `tests/test_p_adic.py`
- `tests/test_solenoid.py`
- `tests/test_linear_algebra.py`
- `tests/test_nucleus_compression.py` if feasible and stable.

## Конкретные математические требования

### D/H/L/safe_divide
- `D(x) = 2x`, `H(x) = x/2`; support scalar and vector/list consistently.
- Test `H(D(x)) == x` and `D(H(x)) == x` for scalar/list.
- `L(x)` should be explicitly documented as binary depth for positive magnitude; invalid domain should be deterministic and tested.
- `safe_divide(a, 0)` should keep documented U-system behavior `D(a)` / `2a` if this is existing public contract; document clearly.

### Δ-field
- Prefer natural logarithm contract from Universe: `Δ = ln(|Re| + eps) - ln(|Im| + eps)` or equivalent existing pixel formula if current pipeline requires it.
- If changing base from log2 to ln is risky, introduce clear constants/API and tests that pin the chosen contract.
- Boundary behavior must be finite and deterministic.
- Inverse transform should roundtrip representative values within tolerance.

### p-adic / D-adic
- Fix `v2_adic_valuation(0)`: valuation of zero should behave as `+inf` in distance formula.
- `p_adic_distance(x, x)` must return `0.0`.
- For integers, implement/test `d_2(x, y) = 2^{-v2(x-y)}` with `d(x,x)=0`.
- Add ultrametric inequality tests for representative triples.
- For floats, do not pretend rigorous p-adic integer valuation if not possible; either restrict/document or coerce deterministic integer deltas explicitly.

### Solenoid
- Fix binary encoding for fractional values: extract bits from fractional part by repeated doubling, not `int(x) & 1` only.
- `solenoid_distance` must be a prefix metric: equal sequences distance `0`; if one is a strict prefix of the other, distance should be positive and depend on shared prefix length.
- Add deterministic tests for exact equality, first-bit mismatch, partial common prefix, strict-prefix case.
- `solenoid_similarity` should map distance to a stable `[0, 1]`-like score.

### linear_algebra
- Add/strengthen shape validation for matrix rectangularity and matmul incompatible shapes.
- Preserve list-backed behavior and public names.
- Add tests for vector norm/dot, rectangular validation, matmul shape errors.

## Verification requested
After editing, run available checks if possible:
- `python3 -m pytest tests/ -v` or relevant subset.
- `ruff check` if practical.
- If full suite unavailable, at least run the newly created tests.

## Output artifact
Write an implementation summary to `implementation-summary.md` in this task folder with:
- files changed;
- key decisions;
- tests added;
- exact test command output or blocker.
