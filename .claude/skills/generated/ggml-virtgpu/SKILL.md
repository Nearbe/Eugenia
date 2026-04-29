---
name: ggml-virtgpu
description: "Skill for the Ggml-virtgpu area of Eugenia. 261 symbols across 50 files."
---

# Ggml-virtgpu

261 symbols | 50 files | Cohesion: 89%

## When to Use

- Working with code in `ggml/`
- Understanding how remote_call_finish, apir_device_get_count, apir_device_get_name work
- Modifying ggml-virtgpu-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `ggml/src/ggml-virtgpu/virtgpu-forward.gen.h` | apir_device_get_count, apir_device_get_name, apir_device_get_description, apir_device_get_type, apir_device_get_memory (+16) |
| `llama.cpp/ggml/src/ggml-virtgpu/virtgpu.cpp` | virtgpu_init_capset, virtgpu_init_context, virtgpu_ioctl_context_init, virtgpu_ioctl_get_caps, virtgpu_handshake (+7) |
| `ggml/src/ggml-virtgpu/virtgpu.cpp` | virtgpu_open_device, virtgpu_open, virtgpu_init_capset, virtgpu_init_context, virtgpu_ioctl_context_init (+7) |
| `whisper.cpp/ggml/src/ggml-virtgpu/virtgpu.cpp` | virtgpu_open_device, virtgpu_open, virtgpu_init_capset, virtgpu_ioctl_get_caps, virtgpu_handshake (+7) |
| `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | apir_device_get_count, apir_device_get_name, apir_device_get_description, apir_device_get_type, apir_device_get_memory (+4) |
| `whisper.cpp/ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | apir_device_get_count, apir_device_get_name, apir_device_get_description, apir_device_get_type, apir_device_get_memory (+4) |
| `llama.cpp/ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | apir_device_get_count, apir_device_get_name, apir_device_get_description, apir_device_get_type, apir_device_get_memory (+4) |
| `ggml/src/ggml-virtgpu/ggml-backend-device.cpp` | ggml_backend_remoting_device_get_buffer_from_ptr_type, ggml_backend_remoting_device_buffer_from_ptr, ggml_backend_remoting_device_get_name, ggml_backend_remoting_device_get_description, ggml_backend_remoting_device_get_type (+3) |
| `whisper.cpp/ggml/src/ggml-virtgpu/ggml-backend-device.cpp` | ggml_backend_remoting_device_get_buffer_from_ptr_type, ggml_backend_remoting_device_buffer_from_ptr, ggml_backend_remoting_device_get_name, ggml_backend_remoting_device_get_description, ggml_backend_remoting_device_get_type (+3) |
| `llama.cpp/ggml/src/ggml-virtgpu/ggml-backend-device.cpp` | ggml_backend_remoting_device_get_buffer_from_ptr_type, ggml_backend_remoting_device_buffer_from_ptr, ggml_backend_remoting_device_get_name, ggml_backend_remoting_device_get_description, ggml_backend_remoting_device_get_type (+3) |

## Entry Points

Start here when exploring this area:

- **`remote_call_finish`** (Function) — `ggml/src/ggml-virtgpu/virtgpu.h:116`
- **`apir_device_get_count`** (Function) — `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp:3`
- **`apir_device_get_name`** (Function) — `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp:19`
- **`apir_device_get_description`** (Function) — `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp:40`
- **`apir_device_get_type`** (Function) — `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp:63`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `remote_call_finish` | Function | `ggml/src/ggml-virtgpu/virtgpu.h` | 116 |
| `apir_device_get_count` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | 3 |
| `apir_device_get_name` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | 19 |
| `apir_device_get_description` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | 40 |
| `apir_device_get_type` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | 63 |
| `apir_device_get_memory` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | 84 |
| `apir_device_supports_op` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | 106 |
| `apir_device_get_buffer_type` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | 125 |
| `apir_device_get_props` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | 142 |
| `apir_buffer_get_base` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-buffer.cpp` | 2 |
| `apir_buffer_cpy_tensor` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-buffer.cpp` | 121 |
| `apir_buffer_clear` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-buffer.cpp` | 145 |
| `apir_buffer_free_buffer` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-buffer.cpp` | 160 |
| `apir_buffer_type_get_name` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-buffer-type.cpp` | 2 |
| `apir_buffer_type_get_alignment` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-buffer-type.cpp` | 26 |
| `apir_buffer_type_get_max_size` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-buffer-type.cpp` | 45 |
| `apir_buffer_type_alloc_buffer` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-buffer-type.cpp` | 64 |
| `apir_buffer_type_get_alloc_size` | Function | `ggml/src/ggml-virtgpu/virtgpu-forward-buffer-type.cpp` | 88 |
| `apir_device_get_count` | Function | `whisper.cpp/ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | 3 |
| `apir_device_get_name` | Function | `whisper.cpp/ggml/src/ggml-virtgpu/virtgpu-forward-device.cpp` | 19 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Create_virtgpu → Open` | cross_community | 4 |
| `Create_virtgpu → GGML_ABORT` | cross_community | 4 |
| `Create_virtgpu → GGML_LOG_ERROR` | cross_community | 4 |
| `Create_virtgpu → GGML_LOG_INFO` | cross_community | 4 |
| `Create_virtgpu → Open` | cross_community | 4 |
| `Create_virtgpu → GGML_ABORT` | cross_community | 4 |
| `Create_virtgpu → GGML_LOG_ERROR` | cross_community | 4 |
| `Create_virtgpu → GGML_LOG_INFO` | cross_community | 4 |
| `Create_virtgpu → Open` | cross_community | 4 |
| `Create_virtgpu → GGML_ABORT` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Server | 3 calls |

## How to Explore

1. `gitnexus_context({name: "remote_call_finish"})` — see callers and callees
2. `gitnexus_query({query: "ggml-virtgpu"})` — find related execution flows
3. Read key files listed above for implementation details
