---
name: ggml-backend
description: "Skill for the Ggml_backend_ area of Eugenia. 210 symbols across 8 files."
---

# Ggml_backend_

210 symbols | 8 files | Cohesion: 63%

## When to Use

- Working with code in `ggml/`
- Understanding how ggml_backend_buft_is_meta, ggml_backend_meta_alloc_ctx_tensors_from_buft, ggml_backend_buft_is_meta work
- Modifying ggml_backend_-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `whisper.cpp/ggml/src/ggml-backend.cpp` | ggml_backend_tensor_set_async, ggml_backend_tensor_get_async, ggml_backend_tensor_set, ggml_backend_tensor_get, ggml_backend_synchronize (+52) |
| `ggml/src/ggml-backend.cpp` | ggml_backend_buft_name, ggml_backend_buffer_name, ggml_backend_offload_op, ggml_backend_dev_offload_op, ggml_backend_sched_backend_from_buffer (+49) |
| `llama.cpp/ggml/src/ggml-backend.cpp` | ggml_backend_buft_name, ggml_backend_buffer_name, ggml_backend_offload_op, ggml_backend_dev_offload_op, ggml_backend_sched_backend_from_buffer (+47) |
| `ggml/src/ggml-backend-meta.cpp` | ggml_backend_meta_buft_n_bufts, ggml_backend_meta_buffer_type_get_name, ggml_backend_meta_buft_simple_buft, ggml_backend_meta_buffer_type_alloc_buffer, ggml_backend_meta_buffer_type_get_alignment (+16) |
| `llama.cpp/ggml/src/ggml-backend-meta.cpp` | ggml_backend_meta_buft_n_bufts, ggml_backend_meta_buffer_type_get_name, ggml_backend_meta_buft_simple_buft, ggml_backend_meta_buffer_type_alloc_buffer, ggml_backend_meta_buffer_type_get_alignment (+16) |
| `ggml/src/ggml-backend-impl.h` | ggml_backend_buffer_is_meta, ggml_backend_buft_is_meta, ggml_backend_meta_alloc_ctx_tensors_from_buft |
| `ggml/src/ggml-alloc.c` | ggml_backend_alloc_ctx_tensors_from_buft |
| `llama.cpp/ggml/src/ggml-alloc.c` | ggml_backend_alloc_ctx_tensors_from_buft |

## Entry Points

Start here when exploring this area:

- **`ggml_backend_buft_is_meta`** (Function) — `ggml/src/ggml-backend-meta.cpp:338`
- **`ggml_backend_meta_alloc_ctx_tensors_from_buft`** (Function) — `ggml/src/ggml-backend-meta.cpp:1418`
- **`ggml_backend_buft_is_meta`** (Function) — `llama.cpp/ggml/src/ggml-backend-meta.cpp:338`
- **`ggml_backend_meta_alloc_ctx_tensors_from_buft`** (Function) — `llama.cpp/ggml/src/ggml-backend-meta.cpp:1452`
- **`ggml_backend_tensor_set_async`** (Function) — `whisper.cpp/ggml/src/ggml-backend.cpp:253`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ggml_backend_buft_is_meta` | Function | `ggml/src/ggml-backend-meta.cpp` | 338 |
| `ggml_backend_meta_alloc_ctx_tensors_from_buft` | Function | `ggml/src/ggml-backend-meta.cpp` | 1418 |
| `ggml_backend_buft_is_meta` | Function | `llama.cpp/ggml/src/ggml-backend-meta.cpp` | 338 |
| `ggml_backend_meta_alloc_ctx_tensors_from_buft` | Function | `llama.cpp/ggml/src/ggml-backend-meta.cpp` | 1452 |
| `ggml_backend_tensor_set_async` | Function | `whisper.cpp/ggml/src/ggml-backend.cpp` | 253 |
| `ggml_backend_tensor_get_async` | Function | `whisper.cpp/ggml/src/ggml-backend.cpp` | 267 |
| `ggml_backend_tensor_set` | Function | `whisper.cpp/ggml/src/ggml-backend.cpp` | 281 |
| `ggml_backend_tensor_get` | Function | `whisper.cpp/ggml/src/ggml-backend.cpp` | 296 |
| `ggml_backend_synchronize` | Function | `whisper.cpp/ggml/src/ggml-backend.cpp` | 327 |
| `ggml_backend_tensor_copy` | Function | `whisper.cpp/ggml/src/ggml-backend.cpp` | 390 |
| `ggml_backend_tensor_copy_async` | Function | `whisper.cpp/ggml/src/ggml-backend.cpp` | 413 |
| `ggml_backend_buft_name` | Function | `ggml/src/ggml-backend.cpp` | 32 |
| `ggml_backend_buffer_name` | Function | `ggml/src/ggml-backend.cpp` | 102 |
| `ggml_backend_offload_op` | Function | `ggml/src/ggml-backend.cpp` | 464 |
| `ggml_backend_dev_offload_op` | Function | `ggml/src/ggml-backend.cpp` | 632 |
| `ggml_backend_buffer_get_usage` | Function | `ggml/src/ggml-backend.cpp` | 187 |
| `ggml_backend_event_record` | Function | `ggml/src/ggml-backend.cpp` | 537 |
| `ggml_backend_event_synchronize` | Function | `ggml/src/ggml-backend.cpp` | 544 |
| `ggml_backend_event_wait` | Function | `ggml/src/ggml-backend.cpp` | 551 |
| `ggml_backend_sched_get_tensor_backend` | Function | `ggml/src/ggml-backend.cpp` | 1968 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tests | 27 calls |
| Ggml_ | 22 calls |
| Ggml_backend_buf | 15 calls |
| Include | 4 calls |
| Cluster_577 | 3 calls |
| Ggml-hexagon | 3 calls |
| Cluster_554 | 3 calls |
| Ggml-zdnn | 3 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_backend_buft_is_meta"})` — see callers and callees
2. `gitnexus_query({query: "ggml_backend_"})` — find related execution flows
3. Read key files listed above for implementation details
