---
name: include
description: "Skill for the Include area of Eugenia. 157 symbols across 43 files."
---

# Include

157 symbols | 43 files | Cohesion: 51%

## When to Use

- Working with code in `ggml/`
- Understanding how llama_decode, ggml_backend_meta_n_backends, ggml_backend_meta_simple_backend work
- Modifying include-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `ggml/include/ggml-backend.h` | ggml_backend_tensor_get_async, ggml_backend_tensor_set_2d_async, ggml_backend_tensor_get_2d_async, ggml_backend_synchronize, ggml_backend_tensor_set_2d (+17) |
| `ggml/src/ggml-backend-meta.cpp` | ggml_backend_meta_set_tensor_async, ggml_backend_meta_get_tensor_async, ggml_backend_meta_synchronize, ggml_backend_meta_n_backends, ggml_backend_meta_simple_backend (+13) |
| `llama.cpp/ggml/src/ggml-backend-meta.cpp` | ggml_backend_meta_split_axis_name, ggml_backend_meta_buffer_n_bufs, ggml_backend_meta_buffer_simple_tensor, ggml_backend_meta_get_split_state, ggml_backend_meta_buffer_init_tensor (+13) |
| `llama.cpp/src/llama-context.cpp` | build_seq_to_output_row, copy_tensor_async_ints, copy_tensor_async_floats, copy_tensor_async_candidates, needs_raw_logits (+11) |
| `ggml/include/gguf.h` | gguf_set_val_u8, gguf_set_val_i8, gguf_set_val_u16, gguf_set_val_i16, gguf_set_val_u32 (+11) |
| `llama.cpp/src/llama-quant.cpp` | remap_imatrix, llama_model_quantize_impl, llama_model_quantize, tensor_allows_quantization, llama_tensor_quantize_impl |
| `whisper.cpp/examples/talk-llama/llama-context.cpp` | set_sampler, opt_epoch_iter, ~llama_context, graph_compute |
| `llama.cpp/src/llama-memory.h` | next, get_ubatch, init_batch, clear |
| `ggml/include/ggml-opt.h` | ggml_opt_labels, ggml_opt_prepare_alloc, ggml_opt_free, ggml_opt_get_default_optimizer_params |
| `llama.cpp/common/common.cpp` | reset_samplers, common_init_from_params, common_control_vector_load, common_opt_lr_pars |

## Entry Points

Start here when exploring this area:

- **`llama_decode`** (Function) — `llama.cpp/src/llama-context.cpp:3450`
- **`ggml_backend_meta_n_backends`** (Function) — `ggml/src/ggml-backend-meta.cpp:2080`
- **`ggml_backend_meta_simple_backend`** (Function) — `ggml/src/ggml-backend-meta.cpp:2086`
- **`ggml_backend_tensor_get_async`** (Function) — `ggml/include/ggml-backend.h:86`
- **`ggml_backend_tensor_set_2d_async`** (Function) — `ggml/include/ggml-backend.h:87`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `llama_decode` | Function | `llama.cpp/src/llama-context.cpp` | 3450 |
| `ggml_backend_meta_n_backends` | Function | `ggml/src/ggml-backend-meta.cpp` | 2080 |
| `ggml_backend_meta_simple_backend` | Function | `ggml/src/ggml-backend-meta.cpp` | 2086 |
| `ggml_backend_tensor_get_async` | Function | `ggml/include/ggml-backend.h` | 86 |
| `ggml_backend_tensor_set_2d_async` | Function | `ggml/include/ggml-backend.h` | 87 |
| `ggml_backend_tensor_get_2d_async` | Function | `ggml/include/ggml-backend.h` | 88 |
| `ggml_backend_synchronize` | Function | `ggml/include/ggml-backend.h` | 97 |
| `ggml_backend_meta_split_axis_name` | Function | `llama.cpp/ggml/src/ggml-backend-meta.cpp` | 25 |
| `ggml_backend_buffer_is_meta` | Function | `llama.cpp/ggml/src/ggml-backend-meta.cpp` | 1427 |
| `ggml_backend_meta_n_backends` | Function | `llama.cpp/ggml/src/ggml-backend-meta.cpp` | 2114 |
| `ggml_backend_meta_simple_backend` | Function | `llama.cpp/ggml/src/ggml-backend-meta.cpp` | 2120 |
| `llama_model_quantize` | Function | `llama.cpp/src/llama-quant.cpp` | 1303 |
| `gguf_set_val_u8` | Function | `ggml/include/gguf.h` | 132 |
| `gguf_set_val_i8` | Function | `ggml/include/gguf.h` | 133 |
| `gguf_set_val_u16` | Function | `ggml/include/gguf.h` | 134 |
| `gguf_set_val_i16` | Function | `ggml/include/gguf.h` | 135 |
| `gguf_set_val_u32` | Function | `ggml/include/gguf.h` | 136 |
| `gguf_set_val_i32` | Function | `ggml/include/gguf.h` | 137 |
| `gguf_set_val_f32` | Function | `ggml/include/gguf.h` | 138 |
| `gguf_set_val_u64` | Function | `ggml/include/gguf.h` | 139 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Ggml_compute_backward → Ggml_is_empty` | cross_community | 5 |
| `Common_init_from_params → GGML_ASSERT` | cross_community | 4 |
| `Build_attn → GGML_ASSERT` | cross_community | 3 |
| `Build_attn → Cb` | cross_community | 3 |
| `Build_attn → Ggml_add` | cross_community | 3 |
| `Build_attn → Ggml_backend_sched_set_tensor_backend` | cross_community | 3 |
| `Build_attn → GGML_ASSERT` | cross_community | 3 |
| `Build_attn → Cb` | cross_community | 3 |
| `Build_attn → Ggml_add` | cross_community | 3 |
| `Build_attn → Ggml_backend_sched_set_tensor_backend` | cross_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tests | 89 calls |
| Talk-llama | 50 calls |
| Ggml-metal | 16 calls |
| Ggml_ | 13 calls |
| Perplexity | 9 calls |
| Ggml-rpc | 8 calls |
| Ggml_backend_ | 7 calls |
| Cluster_323 | 6 calls |

## How to Explore

1. `gitnexus_context({name: "llama_decode"})` — see callers and callees
2. `gitnexus_query({query: "include"})` — find related execution flows
3. Read key files listed above for implementation details
