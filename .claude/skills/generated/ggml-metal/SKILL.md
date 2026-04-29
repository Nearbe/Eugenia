---
name: ggml-metal
description: "Skill for the Ggml-metal area of Eugenia. 674 symbols across 42 files."
---

# Ggml-metal

674 symbols | 42 files | Cohesion: 75%

## When to Use

- Working with code in `ggml/`
- Understanding how ggml_is_contiguous_rows, ggml_metal_op_encode, ggml_metal_op_concat work
- Modifying ggml-metal-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `ggml/src/ggml-metal/ggml-metal-device.h` | ggml_metal_pipeline_max_theads_per_threadgroup, ggml_metal_encoder_set_pipeline, ggml_metal_encoder_set_bytes, ggml_metal_encoder_set_buffer, ggml_metal_encoder_set_threadgroup_memory_size (+86) |
| `ggml/src/ggml-metal/ggml-metal-ops.cpp` | ggml_metal_get_buffer_id, n_nodes, node, can_fuse, ggml_metal_op_concurrency_reset (+57) |
| `llama.cpp/ggml/src/ggml-metal/ggml-metal-ops.cpp` | ggml_metal_get_buffer_id, node, can_fuse, ggml_metal_op_concurrency_reset, ggml_metal_op_concurrency_check (+57) |
| `whisper.cpp/ggml/src/ggml-metal/ggml-metal-ops.cpp` | ggml_metal_get_buffer_id, node, can_fuse, ggml_metal_op_concurrency_reset, ggml_metal_op_concurrency_check (+56) |
| `ggml/src/ggml-metal/ggml-metal-device.cpp` | ggml_metal_library_get_pipeline_base, ggml_metal_library_get_pipeline_cpy, ggml_metal_library_get_pipeline_pool_1d, ggml_metal_library_get_pipeline_pool_2d, ggml_metal_library_get_pipeline_get_rows (+54) |
| `llama.cpp/ggml/src/ggml-metal/ggml-metal-device.cpp` | ggml_metal_library_get_pipeline_base, ggml_metal_library_get_pipeline_cpy, ggml_metal_library_get_pipeline_pool_1d, ggml_metal_library_get_pipeline_pool_2d, ggml_metal_library_get_pipeline_get_rows (+54) |
| `whisper.cpp/ggml/src/ggml-metal/ggml-metal-device.cpp` | ggml_metal_library_get_pipeline_base, ggml_metal_library_get_pipeline_cpy, ggml_metal_library_get_pipeline_pool_1d, ggml_metal_library_get_pipeline_pool_2d, ggml_metal_library_get_pipeline_get_rows (+53) |
| `ggml/src/ggml-metal/ggml-metal.cpp` | ggml_backend_metal_device_offload_op, ggml_backend_metal_buffer_type_get_alloc_size, ggml_backend_metal_buffer_shared_free_buffer, ggml_backend_metal_buffer_private_free_buffer, ggml_backend_metal_buffer_shared_get_base (+33) |
| `whisper.cpp/ggml/src/ggml-metal/ggml-metal.cpp` | ggml_backend_metal_device_offload_op, ggml_backend_metal_buffer_type_get_alloc_size, ggml_backend_metal_buffer_shared_free_buffer, ggml_backend_metal_buffer_private_free_buffer, ggml_backend_metal_buffer_shared_get_base (+33) |
| `llama.cpp/ggml/src/ggml-metal/ggml-metal.cpp` | ggml_backend_metal_device_offload_op, ggml_backend_metal_buffer_type_get_alloc_size, ggml_backend_metal_buffer_shared_free_buffer, ggml_backend_metal_buffer_private_free_buffer, ggml_backend_metal_buffer_shared_get_base (+33) |

## Entry Points

Start here when exploring this area:

- **`ggml_is_contiguous_rows`** (Function) — `ggml/include/ggml.h:779`
- **`ggml_metal_op_encode`** (Function) — `ggml/src/ggml-metal/ggml-metal-ops.cpp:497`
- **`ggml_metal_op_concat`** (Function) — `ggml/src/ggml-metal/ggml-metal-ops.cpp:515`
- **`ggml_metal_op_repeat`** (Function) — `ggml/src/ggml-metal/ggml-metal-ops.cpp:573`
- **`ggml_metal_op_acc`** (Function) — `ggml/src/ggml-metal/ggml-metal-ops.cpp:617`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ggml_is_contiguous_rows` | Function | `ggml/include/ggml.h` | 779 |
| `ggml_metal_op_encode` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 497 |
| `ggml_metal_op_concat` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 515 |
| `ggml_metal_op_repeat` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 573 |
| `ggml_metal_op_acc` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 617 |
| `ggml_metal_op_unary` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 734 |
| `ggml_metal_op_glu` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 829 |
| `ggml_metal_op_sum` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 887 |
| `ggml_metal_op_sum_rows` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 924 |
| `ggml_metal_op_cumsum` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 989 |
| `ggml_metal_op_get_rows` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 1132 |
| `ggml_metal_op_set_rows` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 1177 |
| `ggml_metal_op_diag` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 1239 |
| `ggml_metal_op_soft_max` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 1281 |
| `ggml_metal_op_ssm_conv` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 1371 |
| `ggml_metal_op_ssm_scan` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 1444 |
| `ggml_metal_op_rwkv` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 1542 |
| `ggml_metal_op_gated_delta_net` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 1583 |
| `ggml_metal_op_solve_tri` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 1658 |
| `ggml_metal_op_set` | Function | `ggml/src/ggml-metal/ggml-metal-ops.cpp` | 1715 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → Ggml_type_name` | cross_community | 5 |
| `Ggml_sycl_compute_forward → Ggml_is_contiguous` | cross_community | 3 |
| `Ggml_sycl_compute_forward → Ggml_is_contiguous` | cross_community | 3 |
| `Ggml_sycl_compute_forward → Ggml_is_contiguous` | cross_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ggml-cpu | 18 calls |
| Ggml-openvino | 15 calls |
| Ggml-webgpu | 14 calls |
| Tests | 9 calls |
| Ggml-hexagon | 9 calls |
| Ggml-blas | 6 calls |
| Ggml_ | 4 calls |
| Ggml-sycl | 3 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_is_contiguous_rows"})` — see callers and callees
2. `gitnexus_query({query: "ggml-metal"})` — find related execution flows
3. Read key files listed above for implementation details
