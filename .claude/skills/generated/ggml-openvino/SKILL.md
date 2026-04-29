---
name: ggml-openvino
description: "Skill for the Ggml-openvino area of Eugenia. 279 symbols across 34 files."
---

# Ggml-openvino

279 symbols | 34 files | Cohesion: 73%

## When to Use

- Working with code in `ggml/`
- Understanding how ov_graph_compute, create_ov_output_tensor, ov_graph_compute_dynamic work
- Modifying ggml-openvino-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `ggml/src/ggml-openvino/ggml-decoder.h` | same_rope_params, can_reuse_dynamically, can_reuse_statically, kv_buffer_changed, get_input_ggml_tensor (+29) |
| `llama.cpp/ggml/src/ggml-openvino/ggml-openvino.cpp` | is_op_unsupported_case, ggml_backend_openvino_device_supports_op, ggml_backend_openvino_buffer_memset_tensor, ggml_backend_openvino_buffer_clear, ggml_backend_openvino_buffer_set_tensor (+20) |
| `ggml/src/ggml-openvino/ggml-openvino.cpp` | is_op_unsupported_case, ggml_backend_openvino_device_supports_op, ggml_backend_openvino_buffer_memset_tensor, ggml_backend_openvino_buffer_clear, ggml_backend_openvino_buffer_init_tensor (+19) |
| `whisper.cpp/ggml/src/ggml-openvino/ggml-openvino.cpp` | is_op_unsupported_case, ggml_backend_openvino_device_supports_op, ggml_backend_openvino_buffer_memset_tensor, ggml_backend_openvino_buffer_clear, ggml_backend_openvino_buffer_type (+19) |
| `ggml/src/ggml-openvino/ggml-decoder.cpp` | get_graph_input_shape, node_is_used_as_src, compute_model_inputs, get_shape, get_ov_type (+11) |
| `whisper.cpp/ggml/src/ggml-openvino/ggml-decoder.cpp` | get_graph_input_shape, node_is_used_as_src, compute_model_inputs, get_shape, get_ov_type (+11) |
| `llama.cpp/ggml/src/ggml-openvino/ggml-decoder.cpp` | get_graph_input_shape, node_is_used_as_src, compute_model_inputs, get_shape, get_ov_type (+11) |
| `ggml/src/ggml-openvino/utils.cpp` | ov_graph_compute, create_ov_output_tensor, ov_graph_compute_dynamic, ov_graph_compute_static, is_naive (+8) |
| `whisper.cpp/ggml/src/ggml-openvino/utils.cpp` | ov_graph_compute, create_ov_output_tensor, ov_graph_compute_dynamic, ov_graph_compute_static, is_naive (+8) |
| `llama.cpp/ggml/src/ggml-openvino/utils.cpp` | ov_graph_compute, create_ov_output_tensor, ov_graph_compute_dynamic, ov_graph_compute_static, is_naive (+8) |

## Entry Points

Start here when exploring this area:

- **`ov_graph_compute`** (Function) — `ggml/src/ggml-openvino/utils.cpp:38`
- **`create_ov_output_tensor`** (Function) — `ggml/src/ggml-openvino/utils.cpp:64`
- **`ov_graph_compute_dynamic`** (Function) — `ggml/src/ggml-openvino/utils.cpp:80`
- **`ov_graph_compute_static`** (Function) — `ggml/src/ggml-openvino/utils.cpp:269`
- **`is_naive`** (Function) — `ggml/src/ggml-openvino/utils.cpp:472`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `Tensor` | Class | `llama.cpp/convert_llama_ggml_to_gguf.py` | 100 |
| `ov_graph_compute` | Function | `ggml/src/ggml-openvino/utils.cpp` | 38 |
| `create_ov_output_tensor` | Function | `ggml/src/ggml-openvino/utils.cpp` | 64 |
| `ov_graph_compute_dynamic` | Function | `ggml/src/ggml-openvino/utils.cpp` | 80 |
| `ov_graph_compute_static` | Function | `ggml/src/ggml-openvino/utils.cpp` | 269 |
| `is_naive` | Function | `ggml/src/ggml-openvino/utils.cpp` | 472 |
| `naive_compute` | Function | `ggml/src/ggml-openvino/utils.cpp` | 483 |
| `get_ov_input_tensor` | Function | `ggml/src/ggml-openvino/utils.cpp` | 562 |
| `get_ov_input_tensor_static_decode` | Function | `ggml/src/ggml-openvino/utils.cpp` | 572 |
| `get_ov_input_tensor_static_prefill` | Function | `ggml/src/ggml-openvino/utils.cpp` | 615 |
| `print_input_tensor_info` | Function | `ggml/src/ggml-openvino/utils.cpp` | 698 |
| `print_output_tensor_info` | Function | `ggml/src/ggml-openvino/utils.cpp` | 744 |
| `get_inp_pos_tensor` | Function | `ggml/src/ggml-openvino/utils.cpp` | 801 |
| `ggml_openvino_get_remote_context` | Function | `ggml/src/ggml-openvino/ggml-openvino-extra.h` | 22 |
| `ggml_openvino_is_npu` | Function | `ggml/src/ggml-openvino/ggml-openvino-extra.h` | 82 |
| `ov_graph_compute` | Function | `whisper.cpp/ggml/src/ggml-openvino/utils.cpp` | 38 |
| `create_ov_output_tensor` | Function | `whisper.cpp/ggml/src/ggml-openvino/utils.cpp` | 64 |
| `ov_graph_compute_dynamic` | Function | `whisper.cpp/ggml/src/ggml-openvino/utils.cpp` | 80 |
| `ov_graph_compute_static` | Function | `whisper.cpp/ggml/src/ggml-openvino/utils.cpp` | 269 |
| `is_naive` | Function | `whisper.cpp/ggml/src/ggml-openvino/utils.cpp` | 472 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Ov_graph_compute_dynamic → Get_input_ggml_tensor` | intra_community | 5 |
| `Ov_graph_compute_dynamic → Get_shape` | intra_community | 5 |
| `Ov_graph_compute_dynamic → Tensor` | intra_community | 5 |
| `Ov_graph_compute_dynamic → Get_ov_type` | intra_community | 5 |
| `Ov_graph_compute_dynamic → Get_model_extra_inputs` | intra_community | 4 |
| `Ov_graph_compute_dynamic → Get_model_extra_input_values` | intra_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ggml-metal | 13 calls |
| Ggml-webgpu | 9 calls |
| Models | 6 calls |
| Ggml-cpu | 3 calls |
| Talk-llama | 3 calls |
| Examples | 3 calls |
| Perplexity | 3 calls |
| Tests | 2 calls |

## How to Explore

1. `gitnexus_context({name: "ov_graph_compute"})` — see callers and callees
2. `gitnexus_query({query: "ggml-openvino"})` — find related execution flows
3. Read key files listed above for implementation details
