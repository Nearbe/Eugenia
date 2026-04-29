---
name: loongarch
description: "Skill for the Loongarch area of Eugenia. 162 symbols across 6 files."
---

# Loongarch

162 symbols | 6 files | Cohesion: 86%

## When to Use

- Working with code in `ggml/`
- Understanding how ggml_vec_dot_q4_0_q8_0, ggml_vec_dot_q4_1_q8_1, ggml_vec_dot_q5_0_q8_0 work
- Modifying loongarch-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `ggml/src/ggml-cpu/arch/loongarch/quants.c` | lsx_madd_h, lsx_set_w, lsx_shuffle_b, lsx_hadd_h, hsum_float_4x4 (+47) |
| `whisper.cpp/ggml/src/ggml-cpu/arch/loongarch/quants.c` | lsx_madd_h, lsx_set_w, lsx_shuffle_b, lsx_hadd_h, hsum_float_4x4 (+47) |
| `llama.cpp/ggml/src/ggml-cpu/arch/loongarch/quants.c` | lsx_madd_h, lsx_set_w, lsx_shuffle_b, lsx_hadd_h, hsum_float_4x4 (+47) |
| `ggml/src/ggml-cpu/ggml-cpu-impl.h` | __lsx_vreplfr2vr_s, __lasx_xvreplfr2vr_s |
| `whisper.cpp/ggml/src/ggml-cpu/ggml-cpu-impl.h` | __lsx_vreplfr2vr_s, __lasx_xvreplfr2vr_s |
| `llama.cpp/ggml/src/ggml-cpu/ggml-cpu-impl.h` | __lsx_vreplfr2vr_s, __lasx_xvreplfr2vr_s |

## Entry Points

Start here when exploring this area:

- **`ggml_vec_dot_q4_0_q8_0`** (Function) — `ggml/src/ggml-cpu/arch/loongarch/quants.c:646`
- **`ggml_vec_dot_q4_1_q8_1`** (Function) — `ggml/src/ggml-cpu/arch/loongarch/quants.c:774`
- **`ggml_vec_dot_q5_0_q8_0`** (Function) — `ggml/src/ggml-cpu/arch/loongarch/quants.c:833`
- **`ggml_vec_dot_q5_1_q8_1`** (Function) — `ggml/src/ggml-cpu/arch/loongarch/quants.c:886`
- **`ggml_vec_dot_q8_0_q8_0`** (Function) — `ggml/src/ggml-cpu/arch/loongarch/quants.c:942`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ggml_vec_dot_q4_0_q8_0` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 646 |
| `ggml_vec_dot_q4_1_q8_1` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 774 |
| `ggml_vec_dot_q5_0_q8_0` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 833 |
| `ggml_vec_dot_q5_1_q8_1` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 886 |
| `ggml_vec_dot_q8_0_q8_0` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 942 |
| `ggml_vec_dot_q2_K_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 989 |
| `ggml_vec_dot_q3_K_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 1069 |
| `ggml_vec_dot_q4_K_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 1172 |
| `ggml_vec_dot_q5_K_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 1269 |
| `ggml_vec_dot_q6_K_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 1372 |
| `ggml_vec_dot_iq2_xxs_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 1490 |
| `ggml_vec_dot_iq2_xs_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 1553 |
| `ggml_vec_dot_iq2_s_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 1692 |
| `ggml_vec_dot_iq3_xxs_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 1787 |
| `ggml_vec_dot_iq3_s_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 1855 |
| `ggml_vec_dot_iq1_s_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 1966 |
| `ggml_vec_dot_iq4_nl_q8_0` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 2042 |
| `ggml_vec_dot_iq4_xs_q8_K` | Function | `ggml/src/ggml-cpu/arch/loongarch/quants.c` | 2101 |
| `ggml_vec_dot_q4_0_q8_0` | Function | `whisper.cpp/ggml/src/ggml-cpu/arch/loongarch/quants.c` | 646 |
| `ggml_vec_dot_q4_1_q8_1` | Function | `whisper.cpp/ggml/src/ggml-cpu/arch/loongarch/quants.c` | 774 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ggml-cpu | 43 calls |
| Wasm | 6 calls |
| Riscv | 5 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_vec_dot_q4_0_q8_0"})` — see callers and callees
2. `gitnexus_query({query: "loongarch"})` — find related execution flows
3. Read key files listed above for implementation details
