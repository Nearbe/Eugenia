---
name: server
description: "Skill for the Server area of Eugenia. 543 symbols across 52 files."
---

# Server

543 symbols | 52 files | Cohesion: 59%

## When to Use

- Working with code in `llama.cpp/`
- Understanding how common_speculative_begin, common_speculative_accept, lora_all_alora work
- Modifying server-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `whisper.cpp/examples/server/httplib.h` | message_digest, error, send, set_connection_timeout, set_read_timeout (+193) |
| `llama.cpp/tools/server/server-context.cpp` | prompt_save, prompt_load, prompt_clear, init_sampler, can_split (+53) |
| `llama.cpp/tools/server/server-common.h` | lora_all_alora, are_lora_equal, lora_get_enabled_ids, insert, get_tokens (+30) |
| `llama.cpp/tools/server/server-models.cpp` | unload_all, close_write, write, to_lower_copy, should_strip_proxy_header (+29) |
| `llama.cpp/tools/server/server-common.cpp` | tokenize_mixed, oaicompat_completion_params_parse, format_prompt_infill, random_string, get_media_marker (+18) |
| `llama.cpp/tools/server/server-task.cpp` | load, usage_json_oaicompat, to_json_oaicompat, to_json_oaicompat_chat, to_json_oaicompat_chat_stream (+16) |
| `llama.cpp/tools/server/server-task.h` | need_embd, need_sampling, is_parent, is_child, n_tokens (+11) |
| `llama.cpp/tools/server/server-queue.cpp` | add_waiting_task_id, post_task, remove_waiting_task_id, remove_waiting_task_ids, recv_with_timeout (+11) |
| `llama.cpp/tools/server/server-queue.h` | send, is_sleeping, post_task, next, post_tasks (+4) |
| `llama.cpp/common/chat.h` | common_chat_templates_source, to_json_oaicompat, common_reasoning_format_name, common_reasoning_format_from_name, common_chat_templates_support_enable_thinking (+4) |

## Entry Points

Start here when exploring this area:

- **`common_speculative_begin`** (Function) — `llama.cpp/common/speculative.h:23`
- **`common_speculative_accept`** (Function) — `llama.cpp/common/speculative.h:33`
- **`lora_all_alora`** (Function) — `llama.cpp/tools/server/server-common.h:102`
- **`are_lora_equal`** (Function) — `llama.cpp/tools/server/server-common.h:112`
- **`lora_get_enabled_ids`** (Function) — `llama.cpp/tools/server/server-common.h:117`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `MatcherBase` | Class | `whisper.cpp/examples/server/httplib.h` | 875 |
| `PathParamsMatcher` | Class | `whisper.cpp/examples/server/httplib.h` | 901 |
| `ClientImpl` | Class | `whisper.cpp/examples/server/httplib.h` | 1220 |
| `SSLClient` | Class | `whisper.cpp/examples/server/httplib.h` | 1979 |
| `mmap` | Class | `whisper.cpp/examples/server/httplib.h` | 2613 |
| `ThreadPool` | Class | `whisper.cpp/examples/server/httplib.h` | 769 |
| `Server` | Class | `whisper.cpp/examples/server/httplib.h` | 944 |
| `common_speculative_begin` | Function | `llama.cpp/common/speculative.h` | 23 |
| `common_speculative_accept` | Function | `llama.cpp/common/speculative.h` | 33 |
| `lora_all_alora` | Function | `llama.cpp/tools/server/server-common.h` | 102 |
| `are_lora_equal` | Function | `llama.cpp/tools/server/server-common.h` | 112 |
| `lora_get_enabled_ids` | Function | `llama.cpp/tools/server/server-common.h` | 117 |
| `whisper_lang_str_full` | Function | `whisper.cpp/src/whisper.cpp` | 4009 |
| `main` | Function | `whisper.cpp/examples/server/server.cpp` | 620 |
| `message_digest` | Function | `whisper.cpp/examples/server/httplib.h` | 5481 |
| `debug_get_array_str` | Function | `whisper.cpp/ggml/src/ggml-sycl/common.hpp` | 612 |
| `debug_get_tensor_str` | Function | `whisper.cpp/ggml/src/ggml-sycl/common.hpp` | 628 |
| `debug_get_array_str` | Function | `llama.cpp/ggml/src/ggml-sycl/common.hpp` | 620 |
| `debug_get_tensor_str` | Function | `llama.cpp/ggml/src/ggml-sycl/common.hpp` | 636 |
| `common_chat_templates_source` | Function | `llama.cpp/common/chat.h` | 226 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Process_request → Is_hex` | cross_community | 6 |
| `Create_client_socket → __dtype_to_type` | cross_community | 6 |
| `Create_client_socket → __type_name` | cross_community | 6 |
| `Init_routes → Contains` | cross_community | 5 |
| `Init_routes → LOG_WRN` | cross_community | 5 |
| `Init_routes → Has_model` | cross_community | 5 |
| `Init_routes → SRV_INF` | cross_community | 5 |
| `Process_request → To_lower` | cross_community | 5 |
| `Process_request → To_utf8` | cross_community | 5 |
| `Process_request → Append` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tests | 37 calls |
| Dpct | 29 calls |
| Perplexity | 25 calls |
| Mtmd | 10 calls |
| Ggml-metal | 6 calls |
| Examples | 6 calls |
| Cluster_396 | 5 calls |
| Cli | 4 calls |

## How to Explore

1. `gitnexus_context({name: "common_speculative_begin"})` — see callers and callees
2. `gitnexus_query({query: "server"})` — find related execution flows
3. Read key files listed above for implementation details
