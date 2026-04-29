---
name: ggml-hexagon
description: "Skill for the Ggml-hexagon area of Eugenia. 292 symbols across 18 files."
---

# Ggml-hexagon

292 symbols | 18 files | Cohesion: 66%

## When to Use

- Working with code in `llama.cpp/`
- Understanding how ggml_op_desc, backend_backend_graph_compute, backend_backend_graph_compute work
- Modifying ggml-hexagon-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `llama.cpp/ggml/src/ggml-hexagon/ggml-hexagon.cpp` | ggml_hexagon_dump_op_supp, ggml_hexagon_supported_add_id, ggml_hexagon_supported_unary, ggml_hexagon_supported_sum_rows, ggml_hexagon_supported_activations (+86) |
| `ggml/src/ggml-hexagon/ggml-hexagon.cpp` | ggml_hexagon_dump_op_supp, ggml_hexagon_dump_op_prof, ggml_hexagon_supported_add_id, ggml_hexagon_supported_unary, ggml_hexagon_supported_sum_rows (+83) |
| `whisper.cpp/ggml/src/ggml-hexagon/ggml-hexagon.cpp` | ggml_hexagon_dump_op_supp, ggml_hexagon_supported_add_id, ggml_hexagon_supported_unary, ggml_hexagon_supported_sum_rows, ggml_hexagon_supported_activations (+69) |
| `ggml/src/ggml-hexagon/op-desc.h` | format_op_dims, format_tensor_strides, format_op_strides, format_op_types, tensor_buff_name (+2) |
| `whisper.cpp/ggml/src/ggml-hexagon/op-desc.h` | format_op_dims, format_tensor_strides, format_op_strides, format_op_types, tensor_buff_name (+2) |
| `llama.cpp/ggml/src/ggml-hexagon/op-desc.h` | format_op_dims, format_tensor_strides, format_op_strides, format_op_types, tensor_buff_name (+2) |
| `whisper.cpp/ggml/src/ggml-hexagon/htp-drv.cpp` | wstr_to_str, get_driver_path, htpdrv_init |
| `ggml/src/ggml-virtgpu/backend/backend-dispatched-backend.cpp` | validate_graph_operation, backend_backend_graph_compute |
| `whisper.cpp/ggml/src/ggml-virtgpu/backend/backend-dispatched-backend.cpp` | validate_graph_operation, backend_backend_graph_compute |
| `llama.cpp/ggml/src/ggml-virtgpu/backend/backend-dispatched-backend.cpp` | validate_graph_operation, backend_backend_graph_compute |

## Entry Points

Start here when exploring this area:

- **`ggml_op_desc`** (Function) — `ggml/include/ggml.h:747`
- **`backend_backend_graph_compute`** (Function) — `ggml/src/ggml-virtgpu/backend/backend-dispatched-backend.cpp:22`
- **`backend_backend_graph_compute`** (Function) — `whisper.cpp/ggml/src/ggml-virtgpu/backend/backend-dispatched-backend.cpp:22`
- **`backend_backend_graph_compute`** (Function) — `llama.cpp/ggml/src/ggml-virtgpu/backend/backend-dispatched-backend.cpp:22`
- **`ggml_backend_buffer_get_usage`** (Function) — `ggml/include/ggml-backend.h:65`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ggml_op_desc` | Function | `ggml/include/ggml.h` | 747 |
| `backend_backend_graph_compute` | Function | `ggml/src/ggml-virtgpu/backend/backend-dispatched-backend.cpp` | 22 |
| `backend_backend_graph_compute` | Function | `whisper.cpp/ggml/src/ggml-virtgpu/backend/backend-dispatched-backend.cpp` | 22 |
| `backend_backend_graph_compute` | Function | `llama.cpp/ggml/src/ggml-virtgpu/backend/backend-dispatched-backend.cpp` | 22 |
| `ggml_backend_buffer_get_usage` | Function | `ggml/include/ggml-backend.h` | 65 |
| `htp_iface_etm` | Function | `llama.cpp/ggml/src/ggml-hexagon/htp/main.c` | 126 |
| `htp_iface_profiler` | Function | `llama.cpp/ggml/src/ggml-hexagon/htp/main.c` | 138 |
| `htpdrv_init` | Function | `ggml/src/ggml-hexagon/htp-drv.cpp` | 307 |
| `htpdrv_init` | Function | `llama.cpp/ggml/src/ggml-hexagon/htp-drv.cpp` | 307 |
| `htpdrv_init` | Function | `whisper.cpp/ggml/src/ggml-hexagon/htp-drv.cpp` | 307 |
| `c_name` | Method | `ggml/src/ggml-hexagon/ggml-hexagon.cpp` | 143 |
| `flush` | Method | `ggml/src/ggml-hexagon/ggml-hexagon.cpp` | 149 |
| `mmap` | Method | `ggml/src/ggml-hexagon/ggml-hexagon.cpp` | 175 |
| `unmap` | Method | `ggml/src/ggml-hexagon/ggml-hexagon.cpp` | 198 |
| `alloc` | Method | `ggml/src/ggml-hexagon/ggml-hexagon.cpp` | 211 |
| `free` | Method | `ggml/src/ggml-hexagon/ggml-hexagon.cpp` | 233 |
| `ggml_hexagon_opshm` | Method | `ggml/src/ggml-hexagon/ggml-hexagon.cpp` | 1533 |
| `c_name` | Method | `llama.cpp/ggml/src/ggml-hexagon/ggml-hexagon.cpp` | 161 |
| `flush` | Method | `llama.cpp/ggml/src/ggml-hexagon/ggml-hexagon.cpp` | 167 |
| `mmap` | Method | `llama.cpp/ggml/src/ggml-hexagon/ggml-hexagon.cpp` | 193 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Ggml_backend_hexagon_device_supports_op → Ggml_backend_buffer_is_hexagon` | cross_community | 4 |
| `Ggml_backend_hexagon_device_supports_op → Ggml_backend_hexagon_buffer_get_sess` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Ggml-metal | 37 calls |
| Ggml-zdnn | 18 calls |
| Ggml_ | 18 calls |
| Ggml-cpu | 12 calls |
| Ggml-webgpu | 10 calls |
| Tests | 6 calls |
| Ggml-blas | 6 calls |
| Perplexity | 4 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_op_desc"})` — see callers and callees
2. `gitnexus_query({query: "ggml-hexagon"})` — find related execution flows
3. Read key files listed above for implementation details
