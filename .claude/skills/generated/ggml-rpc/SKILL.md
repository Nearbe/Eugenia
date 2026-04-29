---
name: ggml-rpc
description: "Skill for the Ggml-rpc area of Eugenia. 167 symbols across 12 files."
---

# Ggml-rpc

167 symbols | 12 files | Cohesion: 57%

## When to Use

- Working with code in `ggml/`
- Understanding how ggml_backend_buffer_get_base, rpc_transport_init, rpc_transport_shutdown work
- Modifying ggml-rpc-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `whisper.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | buffer_get_base, set_tensor_hash, ggml_backend_rpc_guid, ggml_backend_rpc_init, ggml_backend_is_rpc (+43) |
| `ggml/src/ggml-rpc/ggml-rpc.cpp` | buffer_get_base, set_tensor_hash, ggml_backend_rpc_start_server, ggml_backend_rpc_guid, ggml_backend_rpc_init (+38) |
| `llama.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | buffer_get_base, set_tensor_hash, ggml_backend_rpc_start_server, ggml_backend_rpc_guid, ggml_backend_rpc_init (+38) |
| `ggml/src/ggml-rpc/transport.cpp` | socket_t, is_valid_fd, set_no_delay, set_reuse_addr, accept (+4) |
| `llama.cpp/ggml/src/ggml-rpc/transport.cpp` | socket_t, is_valid_fd, set_no_delay, set_reuse_addr, accept (+4) |
| `ggml/src/ggml-rpc/transport.h` | accept, create_server, rpc_transport_init, rpc_transport_shutdown, recv_data (+4) |
| `llama.cpp/src/llama-kv-cache.cpp` | memory_breakdown |
| `ggml/include/ggml-backend.h` | ggml_backend_buffer_get_base |
| `whisper.cpp/examples/talk-llama/llama-kv-cache.cpp` | memory_breakdown |
| `ggml/include/ggml.h` | ggml_new_tensor_4d |

## Entry Points

Start here when exploring this area:

- **`ggml_backend_buffer_get_base`** (Function) — `ggml/include/ggml-backend.h:56`
- **`rpc_transport_init`** (Function) — `ggml/src/ggml-rpc/transport.h:32`
- **`rpc_transport_shutdown`** (Function) — `ggml/src/ggml-rpc/transport.h:33`
- **`ggml_backend_rpc_start_server`** (Function) — `ggml/src/ggml-rpc/ggml-rpc.cpp:1710`
- **`ggml_backend_rpc_start_server`** (Function) — `llama.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp:1710`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `ggml_backend_buffer_get_base` | Function | `ggml/include/ggml-backend.h` | 56 |
| `rpc_transport_init` | Function | `ggml/src/ggml-rpc/transport.h` | 32 |
| `rpc_transport_shutdown` | Function | `ggml/src/ggml-rpc/transport.h` | 33 |
| `ggml_backend_rpc_start_server` | Function | `ggml/src/ggml-rpc/ggml-rpc.cpp` | 1710 |
| `ggml_backend_rpc_start_server` | Function | `llama.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | 1710 |
| `ggml_backend_rpc_init` | Function | `ggml/src/ggml-rpc/ggml-rpc.cpp` | 790 |
| `ggml_backend_is_rpc` | Function | `ggml/src/ggml-rpc/ggml-rpc.cpp` | 808 |
| `ggml_backend_rpc_add_server` | Function | `ggml/src/ggml-rpc/ggml-rpc.cpp` | 1955 |
| `ggml_backend_rpc_init` | Function | `whisper.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | 941 |
| `ggml_backend_is_rpc` | Function | `whisper.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | 959 |
| `ggml_backend_rpc_add_server` | Function | `whisper.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | 2086 |
| `ggml_backend_rpc_init` | Function | `llama.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | 790 |
| `ggml_backend_is_rpc` | Function | `llama.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | 808 |
| `ggml_backend_rpc_add_server` | Function | `llama.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | 1955 |
| `ggml_new_tensor_4d` | Function | `ggml/include/ggml.h` | 830 |
| `ggml_backend_rpc_get_device_memory` | Function | `ggml/src/ggml-rpc/ggml-rpc.cpp` | 822 |
| `ggml_backend_rpc_get_device_memory` | Function | `whisper.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | 973 |
| `ggml_backend_rpc_get_device_memory` | Function | `llama.cpp/ggml/src/ggml-rpc/ggml-rpc.cpp` | 822 |
| `ggml_backend_buffer_copy_tensor` | Function | `ggml/src/ggml-backend-impl.h` | 78 |
| `ggml_backend_rpc_buffer_type` | Function | `ggml/src/ggml-rpc/ggml-rpc.cpp` | 756 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tests | 29 calls |
| Dpct | 9 calls |
| Ggml-openvino | 6 calls |
| Talk-llama | 4 calls |
| Ggml-zendnn | 3 calls |
| Server | 2 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_backend_buffer_get_base"})` — see callers and callees
2. `gitnexus_query({query: "ggml-rpc"})` — find related execution flows
3. Read key files listed above for implementation details
