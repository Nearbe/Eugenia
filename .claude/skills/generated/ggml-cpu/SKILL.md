---
name: ggml-cpu
description: "Skill for the Ggml-cpu area of Eugenia. 1331 symbols across 98 files."
---

# Ggml-cpu

1331 symbols | 98 files | Cohesion: 60%

## When to Use

- Working with code in `ggml/`
- Understanding how ggml_fp16_to_fp32_row, ggml_bf16_to_fp32_row, log2 work
- Modifying ggml-cpu-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `ggml/src/ggml-cpu/ops.cpp` | ggml_compute_forward_rms_norm_back_f32, ggml_compute_forward_rms_norm_back, ggml_compute_forward_soft_max_f32, ggml_compute_forward_soft_max, ggml_compute_forward_soft_max_ext_back_f32 (+183) |
| `whisper.cpp/ggml/src/ggml-cpu/ops.cpp` | ggml_compute_forward_rms_norm_back_f32, ggml_compute_forward_rms_norm_back, ggml_compute_forward_soft_max_f32, ggml_compute_forward_soft_max, ggml_compute_forward_soft_max_ext_back_f32 (+183) |
| `llama.cpp/ggml/src/ggml-cpu/ops.cpp` | ggml_compute_forward_soft_max_f32, ggml_compute_forward_soft_max, ggml_compute_forward_soft_max_ext_back_f32, ggml_compute_forward_soft_max_ext_back, ggml_compute_forward_flash_attn_ext_f16_one_chunk (+183) |
| `ggml/src/ggml-cpu/ops.h` | ggml_compute_forward_dup, ggml_compute_forward_add1, ggml_compute_forward_sum_rows, ggml_compute_forward_argmax, ggml_compute_forward_repeat_back (+77) |
| `ggml/src/ggml-cpu/vec.h` | ggml_vec_dot_f32, ggml_vec_soft_max_f32, ggml_vec_log_soft_max_f32, ggml_vec_acc1_f32, ggml_vec_sub_f32 (+59) |
| `llama.cpp/ggml/src/ggml-cpu/ggml-cpu.c` | ggml_compute_forward, ggml_get_i32_1d, ggml_set_i32_1d, ggml_get_i32_nd, ggml_set_i32_nd (+34) |
| `whisper.cpp/ggml/src/ggml-cpu/ggml-cpu.c` | ggml_compute_forward, ggml_get_i32_1d, ggml_set_i32_1d, ggml_get_i32_nd, ggml_set_i32_nd (+34) |
| `ggml/src/ggml-cpu/ggml-cpu.c` | ggml_compute_forward, ggml_get_i32_1d, ggml_set_i32_1d, ggml_get_i32_nd, ggml_set_i32_nd (+34) |
| `ggml/src/ggml-cpu/repack.cpp` | gemv, compute_forward, forward_mul_mat_one_chunk, forward_mul_mat, forward_mul_mat_id (+21) |
| `whisper.cpp/ggml/src/ggml-cpu/repack.cpp` | gemv, compute_forward, forward_mul_mat_one_chunk, forward_mul_mat, forward_mul_mat_id (+21) |

## Entry Points

Start here when exploring this area:

- **`ggml_fp16_to_fp32_row`** (Function) — `ggml/include/ggml.h:372`
- **`ggml_bf16_to_fp32_row`** (Function) — `ggml/include/ggml.h:379`
- **`log2`** (Function) — `src/core/transcendental/log2.py:19`
- **`isinf`** (Function) — `src/core/transcendental/isinf.py:14`
- **`ggml_vec_dot_f32`** (Function) — `ggml/src/ggml-cpu/vec.h:41`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ggml_fp16_to_fp32_row` | Function | `ggml/include/ggml.h` | 372 |
| `ggml_bf16_to_fp32_row` | Function | `ggml/include/ggml.h` | 379 |
| `log2` | Function | `src/core/transcendental/log2.py` | 19 |
| `isinf` | Function | `src/core/transcendental/isinf.py` | 14 |
| `ggml_vec_dot_f32` | Function | `ggml/src/ggml-cpu/vec.h` | 41 |
| `ggml_vec_soft_max_f32` | Function | `ggml/src/ggml-cpu/vec.h` | 47 |
| `ggml_vec_log_soft_max_f32` | Function | `ggml/src/ggml-cpu/vec.h` | 48 |
| `ggml_vec_dot_f16` | Function | `ggml/src/ggml-cpu/vec.cpp` | 263 |
| `ggml_compute_forward_rms_norm_back` | Function | `ggml/src/ggml-cpu/ops.cpp` | 3941 |
| `ggml_compute_forward_soft_max` | Function | `ggml/src/ggml-cpu/ops.cpp` | 5348 |
| `ggml_compute_forward_soft_max_ext_back` | Function | `ggml/src/ggml-cpu/ops.cpp` | 5453 |
| `ggml_compute_forward_flash_attn_back` | Function | `ggml/src/ggml-cpu/ops.cpp` | 9230 |
| `ggml_compute_forward_cross_entropy_loss` | Function | `ggml/src/ggml-cpu/ops.cpp` | 10969 |
| `ggml_compute_forward_cross_entropy_loss_back` | Function | `ggml/src/ggml-cpu/ops.cpp` | 11052 |
| `ggml_vec_dot_f16` | Function | `whisper.cpp/ggml/src/ggml-cpu/vec.cpp` | 263 |
| `ggml_compute_forward_rms_norm_back` | Function | `whisper.cpp/ggml/src/ggml-cpu/ops.cpp` | 3938 |
| `ggml_compute_forward_soft_max` | Function | `whisper.cpp/ggml/src/ggml-cpu/ops.cpp` | 5342 |
| `ggml_compute_forward_soft_max_ext_back` | Function | `whisper.cpp/ggml/src/ggml-cpu/ops.cpp` | 5447 |
| `ggml_compute_forward_flash_attn_back` | Function | `whisper.cpp/ggml/src/ggml-cpu/ops.cpp` | 9223 |
| `ggml_compute_forward_cross_entropy_loss` | Function | `whisper.cpp/ggml/src/ggml-cpu/ops.cpp` | 10974 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → Is_fullness` | cross_community | 6 |
| `Main → Is_fullness` | cross_community | 6 |
| `Gptj_eval → Is_fullness` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ggml-metal | 181 calls |
| Arm | 33 calls |
| X86 | 29 calls |
| Ggml-openvino | 24 calls |
| S390 | 21 calls |
| Tests | 18 calls |
| Ggml-webgpu | 18 calls |
| Ggml-cann | 12 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_fp16_to_fp32_row"})` — see callers and callees
2. `gitnexus_query({query: "ggml-cpu"})` — find related execution flows
3. Read key files listed above for implementation details
