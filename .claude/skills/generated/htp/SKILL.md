---
name: htp
description: "Skill for the Htp area of Eugenia. 597 symbols across 82 files."
---

# Htp

597 symbols | 82 files | Cohesion: 79%

## When to Use

- Working with code in `ggml/`
- Understanding how dma_queue_flush, op_matmul, op_matmul_id work
- Modifying htp-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `ggml/src/ggml-hexagon/htp/matmul-ops.c` | q8x4x2_row_size, matmul_2d, matvec_2d, matmul_id, matvec_id (+29) |
| `llama.cpp/ggml/src/ggml-hexagon/htp/matmul-ops.c` | q8x4x2_row_size, matmul_2d, matvec_2d, matmul_id, matvec_id (+29) |
| `whisper.cpp/ggml/src/ggml-hexagon/htp/matmul-ops.c` | matmul_2d, matvec_2d, matmul_id, matvec_id, hvx_vec_load_iq4nlx4x8_full (+28) |
| `whisper.cpp/ggml/src/ggml-hexagon/htp/hmx-matmul-ops.c` | core_dot_chunk_fp16, core_mma_chunk_fp16, get_x4x2_row_stride, transfer_activation_chunk_threaded, dequantize_x4x2_weight_chunk_to_fp16_tiles (+21) |
| `llama.cpp/ggml/src/ggml-hexagon/htp/hmx-matmul-ops.c` | swap_ptr, get_x4x2_row_stride, hmx_compute_chunks, transfer_activation_chunk_threaded, interleave_fp16_weight_chunk_to_tiles (+20) |
| `ggml/src/ggml-hexagon/htp/hmx-matmul-ops.c` | get_x4x2_row_stride, hmx_compute_chunks, transfer_activation_chunk_threaded, dequantize_x4x2_weight_chunk_to_fp16_tiles, transfer_output_chunk_threaded (+20) |
| `whisper.cpp/ggml/src/ggml-hexagon/htp/main.c` | vtcm_acquire, vtcm_release, htp_packet_callback, profile_start, profile_stop (+19) |
| `ggml/src/ggml-hexagon/htp/htp-ctx.h` | op_matmul, op_matmul_id, op_binary, op_unary, op_sum_rows (+11) |
| `ggml/src/ggml-hexagon/htp/hex-dma.h` | dma_queue_flush, dma_make_ptr, dma_queue_pop, dma_queue_pop_nowait, dma_queue_depth (+10) |
| `ggml/src/ggml-hexagon/htp/hvx-arith.h` | hvx_min_scalar_f32_aa, hvx_min_scalar_f32_au, hvx_min_scalar_f32_ua, hvx_min_scalar_f32_uu, hvx_min_scalar_f32 (+10) |

## Entry Points

Start here when exploring this area:

- **`dma_queue_flush`** (Function) — `ggml/src/ggml-hexagon/htp/hex-dma.h:94`
- **`op_matmul`** (Function) — `ggml/src/ggml-hexagon/htp/htp-ctx.h:83`
- **`op_matmul_id`** (Function) — `ggml/src/ggml-hexagon/htp/htp-ctx.h:84`
- **`op_binary`** (Function) — `ggml/src/ggml-hexagon/htp/htp-ctx.h:85`
- **`op_unary`** (Function) — `ggml/src/ggml-hexagon/htp/htp-ctx.h:86`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `dma_queue_flush` | Function | `ggml/src/ggml-hexagon/htp/hex-dma.h` | 94 |
| `op_matmul` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 83 |
| `op_matmul_id` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 84 |
| `op_binary` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 85 |
| `op_unary` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 86 |
| `op_sum_rows` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 87 |
| `op_activations` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 88 |
| `op_softmax` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 89 |
| `op_rope` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 91 |
| `op_flash_attn_ext` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 92 |
| `op_set_rows` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 93 |
| `op_get_rows` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 94 |
| `op_cpy` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 95 |
| `op_repeat` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 96 |
| `op_argsort` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 97 |
| `op_ssm_conv` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 98 |
| `op_cumsum` | Function | `ggml/src/ggml-hexagon/htp/htp-ctx.h` | 99 |
| `transfer_activation_chunk_threaded` | Function | `llama.cpp/ggml/src/ggml-hexagon/htp/hmx-matmul-ops.c` | 205 |
| `hmx_mat_mul_permuted_w16a32_batched` | Function | `llama.cpp/ggml/src/ggml-hexagon/htp/hmx-matmul-ops.c` | 856 |
| `hmx_mat_mul_permuted_w16a32` | Function | `llama.cpp/ggml/src/ggml-hexagon/htp/hmx-matmul-ops.c` | 1049 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Hmx_mat_mul_permuted_w16a32_batched → Hmx_mul_overflow` | cross_community | 5 |
| `Hmx_mat_mul_permuted_w16a32_batched → Hmx_add_overflow` | cross_community | 5 |
| `Hmx_mat_mul_permuted_w16a32_batched → Dma_make_ptr` | cross_community | 5 |
| `Hmx_mat_mul_permuted_w16a32_batched → Dma_queue_pop` | cross_community | 5 |
| `Hmx_mat_mul_permuted_w16a32_batched → Hmx_mul_overflow` | cross_community | 5 |
| `Hmx_mat_mul_permuted_w16a32_batched → Hmx_add_overflow` | cross_community | 5 |
| `Hmx_mat_mul_permuted_w16a32_batched → Dma_make_ptr` | cross_community | 5 |
| `Hmx_mat_mul_permuted_w16a32_batched → Dma_queue_pop` | cross_community | 5 |
| `Hmx_mat_mul_permuted_w16a32_batched → Hmx_mul_overflow` | cross_community | 5 |
| `Hmx_mat_mul_permuted_w16a32_batched → Hmx_add_overflow` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ggml-cpu | 3 calls |

## How to Explore

1. `gitnexus_context({name: "dma_queue_flush"})` — see callers and callees
2. `gitnexus_query({query: "htp"})` — find related execution flows
3. Read key files listed above for implementation details
