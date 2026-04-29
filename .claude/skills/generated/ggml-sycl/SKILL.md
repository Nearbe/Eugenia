---
name: ggml-sycl
description: "Skill for the Ggml-sycl area of Eugenia. 1455 symbols across 121 files."
---

# Ggml-sycl

1455 symbols | 121 files | Cohesion: 67%

## When to Use

- Working with code in `ggml/`
- Understanding how ggml_sycl_op_rwkv_wkv6, ggml_sycl_op_rwkv_wkv7, ggml_sycl_upscale work
- Modifying ggml-sycl-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `llama.cpp/ggml/src/ggml-sycl/ggml-sycl.cpp` | ggml_sycl_compute_forward, ggml_sycl_swap, k_argsort_f32_i32, sum_rows_f32_sycl, argsort_f32_i32_sycl (+106) |
| `ggml/src/ggml-sycl/ggml-sycl.cpp` | ggml_sycl_compute_forward, k_sum_rows_f32, ggml_sycl_swap, k_argsort_f32_i32, sum_rows_f32_sycl (+105) |
| `whisper.cpp/ggml/src/ggml-sycl/ggml-sycl.cpp` | ggml_sycl_compute_forward, k_sum_rows_f32, ggml_sycl_swap, k_argsort_f32_i32, sum_rows_f32_sycl (+104) |
| `ggml/src/ggml-sycl/element_wise.cpp` | op_gelu, op_silu, op_gelu_quick, op_relu, op_sqrt (+55) |
| `whisper.cpp/ggml/src/ggml-sycl/element_wise.cpp` | op_gelu, op_silu, op_gelu_quick, op_relu, op_sqrt (+55) |
| `llama.cpp/ggml/src/ggml-sycl/element_wise.cpp` | op_gelu, op_silu, op_gelu_quick, op_relu, op_sqrt (+55) |
| `ggml/src/ggml-sycl/mmq.cpp` | vec_dot_q2_K_q8_1_impl_mmq, vec_dot_q3_K_q8_1_impl_mmq, vec_dot_q3_K_q8_1_mul_mat, vec_dot_q4_K_q8_1_impl_mmq, vec_dot_q5_K_q8_1_impl_mmq (+36) |
| `whisper.cpp/ggml/src/ggml-sycl/mmq.cpp` | vec_dot_q2_K_q8_1_impl_mmq, vec_dot_q3_K_q8_1_impl_mmq, vec_dot_q3_K_q8_1_mul_mat, vec_dot_q4_K_q8_1_impl_mmq, vec_dot_q5_K_q8_1_impl_mmq (+36) |
| `llama.cpp/ggml/src/ggml-sycl/mmq.cpp` | vec_dot_q2_K_q8_1_impl_mmq, vec_dot_q3_K_q8_1_impl_mmq, vec_dot_q3_K_q8_1_mul_mat, vec_dot_q4_K_q8_1_impl_mmq, vec_dot_q5_K_q8_1_impl_mmq (+36) |
| `llama.cpp/ggml/src/ggml-sycl/mmvq.cpp` | mul_mat_vec_q, mul_mat_vec_q4_0_q8_1_sycl, mul_mat_vec_q4_1_q8_1_sycl, mul_mat_vec_mxfp4_q8_1_sycl, mul_mat_vec_nvfp4_q8_1_sycl (+34) |

## Entry Points

Start here when exploring this area:

- **`ggml_sycl_op_rwkv_wkv6`** (Function) — `ggml/src/ggml-sycl/wkv.hpp:5`
- **`ggml_sycl_op_rwkv_wkv7`** (Function) — `ggml/src/ggml-sycl/wkv.hpp:7`
- **`ggml_sycl_upscale`** (Function) — `ggml/src/ggml-sycl/upscale.hpp:8`
- **`ggml_sycl_op_timestep_embedding`** (Function) — `ggml/src/ggml-sycl/tsembd.hpp:17`
- **`ggml_sycl_ssm_conv`** (Function) — `ggml/src/ggml-sycl/ssm_conv.hpp:4`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ggml_sycl_op_rwkv_wkv6` | Function | `ggml/src/ggml-sycl/wkv.hpp` | 5 |
| `ggml_sycl_op_rwkv_wkv7` | Function | `ggml/src/ggml-sycl/wkv.hpp` | 7 |
| `ggml_sycl_upscale` | Function | `ggml/src/ggml-sycl/upscale.hpp` | 8 |
| `ggml_sycl_op_timestep_embedding` | Function | `ggml/src/ggml-sycl/tsembd.hpp` | 17 |
| `ggml_sycl_ssm_conv` | Function | `ggml/src/ggml-sycl/ssm_conv.hpp` | 4 |
| `ggml_sycl_op_soft_max` | Function | `ggml/src/ggml-sycl/softmax.hpp` | 19 |
| `ggml_sycl_op_soft_max_back` | Function | `ggml/src/ggml-sycl/softmax.hpp` | 21 |
| `ggml_sycl_op_set_rows` | Function | `ggml/src/ggml-sycl/set_rows.hpp` | 5 |
| `ggml_sycl_op_set` | Function | `ggml/src/ggml-sycl/set.hpp` | 4 |
| `ggml_sycl_rope` | Function | `ggml/src/ggml-sycl/rope.hpp` | 19 |
| `ggml_sycl_rope_back` | Function | `ggml/src/ggml-sycl/rope.hpp` | 21 |
| `ggml_sycl_roll` | Function | `ggml/src/ggml-sycl/roll.hpp` | 17 |
| `ggml_sycl_op_pad_reflect_1d` | Function | `ggml/src/ggml-sycl/pad_reflect_1d.hpp` | 7 |
| `ggml_sycl_pad` | Function | `ggml/src/ggml-sycl/pad.hpp` | 19 |
| `ggml_sycl_op_out_prod` | Function | `ggml/src/ggml-sycl/outprod.hpp` | 5 |
| `ggml_sycl_op_gated_linear_attn` | Function | `ggml/src/ggml-sycl/gla.hpp` | 5 |
| `ggml_sycl_gated_delta_net` | Function | `ggml/src/ggml-sycl/gated_delta_net.hpp` | 7 |
| `ggml_sycl_flash_attn_ext` | Function | `ggml/src/ggml-sycl/fattn.hpp` | 17 |
| `ggml_sycl_sqrt` | Function | `ggml/src/ggml-sycl/element_wise.hpp` | 31 |
| `ggml_sycl_sin` | Function | `ggml/src/ggml-sycl/element_wise.hpp` | 33 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → _arctan_inverse` | cross_community | 8 |
| `Ggml_sycl_compute_forward → GGML_LOG_ERROR` | cross_community | 5 |
| `Ggml_sycl_compute_forward → GGML_ASSERT` | cross_community | 5 |
| `Ggml_sycl_compute_forward → SYCL_CHECK` | cross_community | 5 |
| `Ggml_sycl_compute_forward → GGML_LOG_ERROR` | cross_community | 5 |
| `Ggml_sycl_compute_forward → GGML_ASSERT` | cross_community | 5 |
| `Ggml_sycl_compute_forward → SYCL_CHECK` | cross_community | 5 |
| `Ggml_sycl_compute_forward → GGML_LOG_ERROR` | cross_community | 5 |
| `Ggml_sycl_compute_forward → GGML_ASSERT` | cross_community | 5 |
| `Ggml_sycl_compute_forward → SYCL_CHECK` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ggml-metal | 71 calls |
| Transcendental | 13 calls |
| Ggml-cann | 13 calls |
| Dpct | 12 calls |
| Ggml-openvino | 12 calls |
| Perplexity | 12 calls |
| Tests | 11 calls |
| Ggml-cpu | 9 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_sycl_op_rwkv_wkv6"})` — see callers and callees
2. `gitnexus_query({query: "ggml-sycl"})` — find related execution flows
3. Read key files listed above for implementation details
