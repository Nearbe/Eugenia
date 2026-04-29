---
name: tests
description: "Skill for the Tests area of Eugenia. 1451 symbols across 206 files."
---

# Tests

1451 symbols | 206 files | Cohesion: 77%

## When to Use

- Working with code in `llama.cpp/`
- Understanding how main, whisper_init_state, whisper_init_from_file_with_params_no_state work
- Modifying tests-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `llama.cpp/tests/test-backend-ops.cpp` | err, add_sentinel, ggml_new_tensor, ggml_new_tensor_1d, ggml_new_tensor_4d (+178) |
| `ggml/tests/test-backend-ops.cpp` | err, add_sentinel, ggml_new_tensor, ggml_new_tensor_1d, ggml_new_tensor_2d (+177) |
| `whisper.cpp/src/whisper.cpp` | format, ggml_graph_compute_helper, is_multilingual, num_languages, whisper_sched_size (+41) |
| `llama.cpp/common/peg-parser.h` | clear, dump, fail, need_more_input, success (+37) |
| `ggml/include/ggml.h` | ggml_ftype_to_ggml_type, ggml_init, ggml_free, ggml_set_no_alloc, ggml_new_tensor (+29) |
| `llama.cpp/tests/test-chat-auto-parser.cpp` | test_standard_json_tools_openai, test_standard_json_tools_cohere, test_standard_json_tools_function_key, test_tagged_args_with_embedded_quotes, build_test_tools (+28) |
| `llama.cpp/tests/test-chat.cpp` | simple_assist_msg, message_with_tool_calls, message_with_tool_calls_and_reasoning, message_with_content_and_tool_call, message_with_reasoning_and_tool_call (+28) |
| `llama.cpp/common/chat.cpp` | common_chat_msgs_parse_oaicompat, common_chat_tools_to_json_oaicompat, common_chat_tools_parse_oaicompat, is_lfm2_template, common_chat_get_asr_prompt (+21) |
| `ggml/include/ggml-backend.h` | ggml_backend_buft_name, ggml_backend_buffer_name, ggml_backend_buffer_free, ggml_backend_buffer_clear, ggml_backend_buffer_set_usage (+20) |
| `llama.cpp/tests/test-alloc.cpp` | allocated_total, dummy_backend_init, make_context, make_input_1d, make_input_with_size (+19) |

## Entry Points

Start here when exploring this area:

- **`main`** (Function) — `whisper.cpp/tests/test-vad.cpp:49`
- **`whisper_init_state`** (Function) — `whisper.cpp/src/whisper.cpp:3373`
- **`whisper_init_from_file_with_params_no_state`** (Function) — `whisper.cpp/src/whisper.cpp:3623`
- **`whisper_init_from_buffer_with_params_no_state`** (Function) — `whisper.cpp/src/whisper.cpp:3667`
- **`whisper_init_with_params_no_state`** (Function) — `whisper.cpp/src/whisper.cpp:3704`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `main` | Function | `whisper.cpp/tests/test-vad.cpp` | 49 |
| `whisper_init_state` | Function | `whisper.cpp/src/whisper.cpp` | 3373 |
| `whisper_init_from_file_with_params_no_state` | Function | `whisper.cpp/src/whisper.cpp` | 3623 |
| `whisper_init_from_buffer_with_params_no_state` | Function | `whisper.cpp/src/whisper.cpp` | 3667 |
| `whisper_init_with_params_no_state` | Function | `whisper.cpp/src/whisper.cpp` | 3704 |
| `whisper_init_from_file_with_params` | Function | `whisper.cpp/src/whisper.cpp` | 3734 |
| `whisper_init_from_buffer_with_params` | Function | `whisper.cpp/src/whisper.cpp` | 3749 |
| `whisper_init_with_params` | Function | `whisper.cpp/src/whisper.cpp` | 3764 |
| `whisper_free_state` | Function | `whisper.cpp/src/whisper.cpp` | 3803 |
| `whisper_free` | Function | `whisper.cpp/src/whisper.cpp` | 3846 |
| `whisper_encode` | Function | `whisper.cpp/src/whisper.cpp` | 3925 |
| `whisper_vad_init_from_file_with_params` | Function | `whisper.cpp/src/whisper.cpp` | 4716 |
| `whisper_vad_init_with_params` | Function | `whisper.cpp/src/whisper.cpp` | 4760 |
| `whisper_vad_reset_state` | Function | `whisper.cpp/src/whisper.cpp` | 5085 |
| `whisper_vad_detect_speech_no_reset` | Function | `whisper.cpp/src/whisper.cpp` | 5089 |
| `whisper_vad_detect_speech` | Function | `whisper.cpp/src/whisper.cpp` | 5168 |
| `whisper_vad_free` | Function | `whisper.cpp/src/whisper.cpp` | 5445 |
| `whisper_bench_ggml_mul_mat_str` | Function | `whisper.cpp/src/whisper.cpp` | 8224 |
| `gpt_params_parse` | Function | `whisper.cpp/examples/common.h` | 43 |
| `gpt_random_prompt` | Function | `whisper.cpp/examples/common.h` | 47 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Init_routes → Contains` | cross_community | 5 |
| `Main → _get_request_headers` | cross_community | 5 |
| `Process_request → Append` | cross_community | 5 |
| `Standard_constructed_tools → Common_peg_parser` | cross_community | 5 |
| `Python_style_tool_calls → Common_peg_parser` | cross_community | 5 |
| `Whisper_full_with_state → Ggml_backend_sched_alloc_graph` | cross_community | 5 |
| `Whisper_full_with_state → Ggml_backend_tensor_set` | cross_community | 5 |
| `Standard_constructed_tools → Add_parser` | intra_community | 4 |
| `Main → N_img_size` | intra_community | 4 |
| `Main → N_patch_size` | intra_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Talk-llama | 99 calls |
| Models | 79 calls |
| Ggml-cpu | 58 calls |
| Perplexity | 33 calls |
| Include | 32 calls |
| Ggml-metal | 32 calls |
| Examples | 25 calls |
| Server | 21 calls |

## How to Explore

1. `gitnexus_context({name: "main"})` — see callers and callees
2. `gitnexus_query({query: "tests"})` — find related execution flows
3. Read key files listed above for implementation details
