---
name: ggml-webgpu
description: "Skill for the Ggml-webgpu area of Eugenia. 405 symbols across 30 files."
---

# Ggml-webgpu

405 symbols | 30 files | Cohesion: 72%

## When to Use

- Working with code in `llama.cpp/`
- Understanding how ggml_compute_forward_arange, ggml_compute_forward_arange, ggml_compute_forward_arange work
- Modifying ggml-webgpu-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `llama.cpp/ggml/src/ggml-webgpu/ggml-webgpu.cpp` | compute_2d_workgroups, ggml_webgpu_u32_from_f32, alloc_slot, ggml_webgpu_tensor_offset, ggml_webgpu_tensor_buf (+67) |
| `ggml/src/ggml-webgpu/ggml-webgpu.cpp` | compute_2d_workgroups, ggml_webgpu_u32_from_f32, alloc_slot, ggml_webgpu_tensor_offset, ggml_webgpu_tensor_buf (+61) |
| `whisper.cpp/ggml/src/ggml-webgpu/ggml-webgpu.cpp` | compute_2d_workgroups, alloc_bufs, ggml_backend_webgpu_build_multi, ggml_backend_webgpu_build, ggml_webgpu_tensor_offset (+55) |
| `llama.cpp/ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp` | get_sum_rows_pipeline, get_row_norm_pipeline, get_argmax_pipeline, get_set_rows_pipeline, get_set_pipeline (+31) |
| `ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp` | ggml_webgpu_flash_attn_make_pipeline_key, ggml_webgpu_flash_attn_max_kv_tile, ggml_webgpu_flash_attn_vec_get_kv_tile, get_sum_rows_pipeline, get_row_norm_pipeline (+29) |
| `ggml/src/ggml-webgpu/pre_wgsl.hpp` | preprocess, acceptOp, parseLogicalOr, parseLogicalAnd, parseEquality (+25) |
| `whisper.cpp/ggml/src/ggml-webgpu/pre_wgsl.hpp` | acceptOp, parseLogicalOr, parseLogicalAnd, parseEquality, parseRelational (+25) |
| `llama.cpp/ggml/src/ggml-webgpu/pre_wgsl.hpp` | acceptOp, parseLogicalOr, parseLogicalAnd, parseEquality, parseRelational (+25) |
| `whisper.cpp/ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp` | get_sum_rows_pipeline, get_row_norm_pipeline, get_argmax_pipeline, get_set_rows_pipeline, get_set_pipeline (+17) |
| `ggml/src/ggml-cpu/ops.cpp` | ggml_compute_forward_arange_f32, ggml_compute_forward_arange |

## Entry Points

Start here when exploring this area:

- **`ggml_compute_forward_arange`** (Function) — `ggml/src/ggml-cpu/ops.cpp:7962`
- **`ggml_compute_forward_arange`** (Function) — `whisper.cpp/ggml/src/ggml-cpu/ops.cpp:7955`
- **`ggml_compute_forward_arange`** (Function) — `llama.cpp/ggml/src/ggml-cpu/ops.cpp:7962`
- **`ggml_webgpu_flash_attn_make_pipeline_key`** (Function) — `ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp:417`
- **`ggml_webgpu_flash_attn_max_kv_tile`** (Function) — `ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp:492`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ggml_compute_forward_arange` | Function | `ggml/src/ggml-cpu/ops.cpp` | 7962 |
| `ggml_compute_forward_arange` | Function | `whisper.cpp/ggml/src/ggml-cpu/ops.cpp` | 7955 |
| `ggml_compute_forward_arange` | Function | `llama.cpp/ggml/src/ggml-cpu/ops.cpp` | 7962 |
| `ggml_webgpu_flash_attn_make_pipeline_key` | Function | `ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp` | 417 |
| `ggml_webgpu_flash_attn_max_kv_tile` | Function | `ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp` | 492 |
| `ggml_webgpu_flash_attn_vec_get_kv_tile` | Function | `ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp` | 511 |
| `ggml_get_unary_op` | Function | `ggml/include/ggml.h` | 851 |
| `ggml_get_glu_op` | Function | `ggml/include/ggml.h` | 852 |
| `ggml_webgpu_flash_attn_wg_mem_bytes` | Function | `ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp` | 469 |
| `ggml_sycl_flash_attn_ext_supported` | Function | `ggml/src/ggml-sycl/fattn.hpp` | 19 |
| `ggml_backend_webgpu_reg` | Function | `ggml/src/ggml-webgpu/ggml-webgpu.cpp` | 3646 |
| `ggml_backend_webgpu_init` | Function | `ggml/src/ggml-webgpu/ggml-webgpu.cpp` | 3712 |
| `ggml_backend_webgpu_reg` | Function | `llama.cpp/ggml/src/ggml-webgpu/ggml-webgpu.cpp` | 4173 |
| `ggml_backend_webgpu_init` | Function | `llama.cpp/ggml/src/ggml-webgpu/ggml-webgpu.cpp` | 4239 |
| `ggml_webgpu_flash_attn_make_pipeline_key` | Function | `llama.cpp/ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp` | 530 |
| `ggml_webgpu_flash_attn_get_decisions` | Function | `llama.cpp/ggml/src/ggml-webgpu/ggml-webgpu-shader-lib.hpp` | 643 |
| `ggml_backend_webgpu_reg` | Function | `whisper.cpp/ggml/src/ggml-webgpu/ggml-webgpu.cpp` | 3619 |
| `ggml_backend_webgpu_init` | Function | `whisper.cpp/ggml/src/ggml-webgpu/ggml-webgpu.cpp` | 3659 |
| `alloc_slot` | Method | `llama.cpp/ggml/src/ggml-webgpu/ggml-webgpu.cpp` | 147 |
| `alloc_slot` | Method | `ggml/src/ggml-webgpu/ggml-webgpu.cpp` | 146 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ggml-metal | 31 calls |
| Ggml-cpu | 17 calls |
| Tests | 17 calls |
| Perplexity | 15 calls |
| Dpct | 12 calls |
| Server | 6 calls |
| Ggml-hexagon | 4 calls |
| Ggml-cann | 3 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_compute_forward_arange"})` — see callers and callees
2. `gitnexus_query({query: "ggml-webgpu"})` — find related execution flows
3. Read key files listed above for implementation details
