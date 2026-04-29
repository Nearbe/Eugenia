---
name: models
description: "Skill for the Models area of Eugenia. 367 symbols across 246 files."
---

# Models

367 symbols | 246 files | Cohesion: 52%

## When to Use

- Working with code in `llama.cpp/`
- Understanding how ggml_add, ggml_compute_forward_top_k, ggml_compute_forward_top_k work
- Modifying models-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `llama.cpp/src/models/gemma3n-iswa.cpp` | ggml_view_2d_slice, llm_build_gemma3n_iswa, calc_magnitude, build_inp_per_layer, project_per_layer_inputs (+5) |
| `whisper.cpp/examples/talk-llama/models/gemma3n-iswa.cpp` | llm_build_gemma3n_iswa, calc_magnitude, get_per_layer_inputs, project_per_layer_inputs, laurel (+5) |
| `llama.cpp/src/models/models.h` | build_delta_net, build_mamba_layer, build_rwkv7_channel_mix, build_rwkv6_time_mix, build_rwkv6_channel_mix (+2) |
| `llama.cpp/src/models/qwen3next.cpp` | build_norm_gated, build_qkvz, build_layer_attn_linear, llm_build_qwen3next, build_layer_attn (+1) |
| `llama.cpp/src/models/qwen35moe.cpp` | build_qkvz, build_norm_gated, build_layer_attn_linear, llm_build_qwen35moe, build_layer_attn (+1) |
| `llama.cpp/src/models/qwen35.cpp` | build_qkvz, build_norm_gated, build_layer_attn_linear, llm_build_qwen35, build_layer_attn (+1) |
| `whisper.cpp/examples/talk-llama/models/qwen3next.cpp` | build_norm_gated, build_qkvz, build_layer_attn_linear, llm_build_qwen3next, build_layer_attn (+1) |
| `whisper.cpp/examples/talk-llama/models/qwen35moe.cpp` | build_qkvz, build_norm_gated, build_layer_attn_linear, llm_build_qwen35moe, build_layer_attn (+1) |
| `whisper.cpp/examples/talk-llama/models/qwen35.cpp` | build_qkvz, build_norm_gated, build_layer_attn_linear, llm_build_qwen35, build_layer_attn (+1) |
| `llama.cpp/tools/mtmd/models/mobilenetv5.cpp` | rms_norm_2d, build_edge_residual, build_inverted_residual, build_mobilenet_attn, build |

## Entry Points

Start here when exploring this area:

- **`ggml_add`** (Function) — `ggml/include/ggml.h:881`
- **`ggml_compute_forward_top_k`** (Function) — `ggml/src/ggml-cpu/ops.cpp:8149`
- **`ggml_compute_forward_top_k`** (Function) — `whisper.cpp/ggml/src/ggml-cpu/ops.cpp:8142`
- **`ggml_compute_forward_top_k`** (Function) — `llama.cpp/ggml/src/ggml-cpu/ops.cpp:8149`
- **`copy`** (Function) — `ggml/examples/python/ggml/utils.py:19`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ggml_add` | Function | `ggml/include/ggml.h` | 881 |
| `ggml_compute_forward_top_k` | Function | `ggml/src/ggml-cpu/ops.cpp` | 8149 |
| `ggml_compute_forward_top_k` | Function | `whisper.cpp/ggml/src/ggml-cpu/ops.cpp` | 8142 |
| `ggml_compute_forward_top_k` | Function | `llama.cpp/ggml/src/ggml-cpu/ops.cpp` | 8149 |
| `copy` | Function | `ggml/examples/python/ggml/utils.py` | 19 |
| `ggml_conv_2d_dw` | Function | `ggml/include/ggml.h` | 2113 |
| `ggml_conv_2d_direct` | Function | `ggml/include/ggml.h` | 2146 |
| `ggml_conv_2d_sk_p0` | Function | `ggml/include/ggml.h` | 2094 |
| `build_lora_mm` | Method | `llama.cpp/src/llama-graph.cpp` | 968 |
| `build_qkv` | Method | `llama.cpp/src/llama-graph.cpp` | 1063 |
| `get_scale` | Method | `llama.cpp/src/llama-adapter.h` | 52 |
| `tensor_for` | Method | `llama.cpp/src/llama-adapter.cpp` | 13 |
| `apply_to` | Method | `llama.cpp/src/llama-adapter.cpp` | 21 |
| `build_lora_mm` | Method | `whisper.cpp/examples/talk-llama/llama-graph.cpp` | 900 |
| `build_inp_embd` | Method | `whisper.cpp/examples/talk-llama/llama-graph.cpp` | 1553 |
| `tensor_for` | Method | `whisper.cpp/examples/talk-llama/llama-adapter.cpp` | 13 |
| `apply_to` | Method | `whisper.cpp/examples/talk-llama/llama-adapter.cpp` | 21 |
| `llm_build_xverse` | Method | `llama.cpp/src/models/xverse.cpp` | 2 |
| `llm_build_wavtokenizer_dec` | Method | `llama.cpp/src/models/wavtokenizer-dec.cpp` | 2 |
| `llm_build_t5` | Method | `llama.cpp/src/models/t5.cpp` | 3 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → __dtype_to_type` | cross_community | 7 |
| `Main → __type_name` | cross_community | 6 |
| `Main → __get_shape` | cross_community | 6 |
| `Create_client_socket → __dtype_to_type` | cross_community | 6 |
| `Create_client_socket → __type_name` | cross_community | 6 |
| `Main → __is_contiguous` | cross_community | 5 |
| `Main → __get_strides` | cross_community | 5 |
| `Whisper_full_with_state → __get_data` | cross_community | 5 |
| `Create_client_socket → __get_shape` | cross_community | 5 |
| `Create_client_socket → __is_contiguous` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tests | 33 calls |
| Talk-llama | 11 calls |
| Ggml | 7 calls |
| Perplexity | 4 calls |
| Ggml-rpc | 4 calls |
| Ggml-sycl | 2 calls |
| Cluster_333 | 1 calls |
| Ggml-cpu | 1 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_add"})` — see callers and callees
2. `gitnexus_query({query: "models"})` — find related execution flows
3. Read key files listed above for implementation details
