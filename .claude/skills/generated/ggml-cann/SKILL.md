---
name: ggml-cann
description: "Skill for the Ggml-cann area of Eugenia. 459 symbols across 15 files."
---

# Ggml-cann

459 symbols | 15 files | Cohesion: 74%

## When to Use

- Working with code in `ggml/`
- Understanding how ggml_cann_repeat, aclnn_add, aclnn_sub work
- Modifying ggml-cann-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `ggml/src/ggml-cann/aclnn_ops.cpp` | aclnn_repeat, aclnn_cast, ggml_cann_repeat, aclnn_add, aclnn_sub (+74) |
| `whisper.cpp/ggml/src/ggml-cann/aclnn_ops.cpp` | aclnn_repeat, aclnn_cast, ggml_cann_repeat, aclnn_add, aclnn_sub (+74) |
| `llama.cpp/ggml/src/ggml-cann/aclnn_ops.cpp` | aclnn_repeat, aclnn_cast, ggml_cann_repeat, aclnn_add, aclnn_sub (+74) |
| `ggml/src/ggml-cann/ggml-cann.cpp` | ggml_cann_compute_forward, clear, realloc, ggml_backend_cann_graph_compute, ggml_cann_info (+42) |
| `whisper.cpp/ggml/src/ggml-cann/ggml-cann.cpp` | ggml_cann_compute_forward, clear, realloc, ggml_backend_cann_graph_compute, ggml_cann_info (+42) |
| `llama.cpp/ggml/src/ggml-cann/ggml-cann.cpp` | ggml_cann_compute_forward, clear, realloc, ggml_backend_cann_graph_compute, ggml_cann_info (+42) |
| `ggml/src/ggml-cann/aclnn_ops.h` | is_matmul_weight, ggml_cann_repeat, ggml_cann_leaky_relu, ggml_cann_concat, ggml_cann_arange (+41) |
| `ggml/src/ggml-cann/common.h` | create_from_cgraph, matches_cgraph, push, find_and_move_to_front, stream (+7) |
| `ggml/src/ggml-cann/acl_tensor.h` | ggml_cann_type_mapping, ggml_cann_create_tensor, ggml_cann_create_scalar, ggml_cann_create_tensor_list, ggml_cann_create_int_array (+1) |
| `whisper.cpp/ggml/src/ggml-cann/common.h` | ggml_cann_set_device, parse_bool, ggml_backend_cann_context, get_env_as_lowercase, parse_integer (+1) |

## Entry Points

Start here when exploring this area:

- **`ggml_cann_repeat`** (Function) — `ggml/src/ggml-cann/aclnn_ops.cpp:193`
- **`aclnn_add`** (Function) — `ggml/src/ggml-cann/aclnn_ops.cpp:206`
- **`aclnn_sub`** (Function) — `ggml/src/ggml-cann/aclnn_ops.cpp:216`
- **`aclnn_mul`** (Function) — `ggml/src/ggml-cann/aclnn_ops.cpp:226`
- **`aclnn_div`** (Function) — `ggml/src/ggml-cann/aclnn_ops.cpp:234`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ggml_cann_repeat` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 193 |
| `aclnn_add` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 206 |
| `aclnn_sub` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 216 |
| `aclnn_mul` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 226 |
| `aclnn_div` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 234 |
| `ggml_cann_leaky_relu` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 277 |
| `ggml_cann_concat` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 307 |
| `ggml_cann_arange` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 356 |
| `ggml_cann_clamp` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 372 |
| `ggml_cann_scale` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 389 |
| `ggml_cann_argsort` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 403 |
| `ggml_cann_l2_norm` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 433 |
| `ggml_cann_group_norm` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 561 |
| `ggml_cann_acc` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 591 |
| `ggml_cann_pad` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 690 |
| `ggml_cann_pool2d` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 823 |
| `ggml_cann_dup` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 853 |
| `ggml_cann_diag_mask` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 1083 |
| `aclnn_cos` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 1325 |
| `aclnn_sin` | Function | `ggml/src/ggml-cann/aclnn_ops.cpp` | 1333 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Ggml_cann_rope → GGML_ASSERT` | intra_community | 4 |
| `Ggml_cann_rope → Ggml_cann_create_scalar` | intra_community | 4 |
| `Ggml_cann_rope → GGML_CANN_CALL_ACLNN_OP` | intra_community | 4 |
| `Ggml_cann_rope → GGML_ASSERT` | intra_community | 4 |
| `Ggml_cann_rope → Ggml_cann_create_scalar` | intra_community | 4 |
| `Ggml_cann_rope → GGML_CANN_CALL_ACLNN_OP` | intra_community | 4 |
| `Ggml_cann_rope → GGML_ASSERT` | intra_community | 4 |
| `Ggml_cann_rope → Ggml_cann_create_scalar` | intra_community | 4 |
| `Ggml_cann_rope → GGML_CANN_CALL_ACLNN_OP` | intra_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ggml-cpu | 18 calls |
| Ggml-openvino | 9 calls |
| Ggml-webgpu | 9 calls |
| Ggml-metal | 9 calls |
| Vdot | 6 calls |
| Dpct | 3 calls |
| Ggml-hexagon | 3 calls |
| Tests | 3 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_cann_repeat"})` — see callers and callees
2. `gitnexus_query({query: "ggml-cann"})` — find related execution flows
3. Read key files listed above for implementation details
