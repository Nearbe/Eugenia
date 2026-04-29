---
name: talk-llama
description: "Skill for the Talk-llama area of Eugenia. 708 symbols across 72 files."
---

# Talk-llama

708 symbols | 72 files | Cohesion: 64%

## When to Use

- Working with code in `whisper.cpp/`
- Understanding how ggml_set_input, format, ggml_backend_sched_synchronize work
- Modifying talk-llama-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `whisper.cpp/examples/talk-llama/llama-context.cpp` | synchronize, get_logits, output_resolve_row, get_logits_ith, get_embeddings (+74) |
| `whisper.cpp/examples/talk-llama/llama-sampler.cpp` | llama_sampler_dist_backend_apply, llama_sampler_init, llama_sampler_init_empty, llama_sampler_greedy_clone, llama_sampler_init_greedy (+66) |
| `whisper.cpp/examples/talk-llama/llama-vocab.cpp` | tokenize, add_new_bigram, find_bpe_rank, insert, llm_tokenizer_ugm (+44) |
| `whisper.cpp/examples/talk-llama/llama-graph.cpp` | build_inp_pos_bucket_dec, build_attn, set_params, llm_graph_context, set_input (+35) |
| `whisper.cpp/examples/talk-llama/llama-kv-cache.cpp` | build_input_k_idxs, build_input_v_idxs, state_write, state_write_meta, state_write_data (+33) |
| `llama.cpp/src/llama-graph.cpp` | build_attn_inp_kq_mask, add_input, build_inp_embd, build_inp_pos, build_inp_attn_scale (+28) |
| `whisper.cpp/examples/talk-llama/llama-grammar.cpp` | llama_grammar_is_end_of_sequence, llama_grammar_match_char, llama_grammar_match_partial_char, llama_grammar_match_token, llama_grammar_advance_stack (+28) |
| `llama.cpp/src/llama-kv-cache.cpp` | build_input_k_idxs, build_input_v_idxs, build_input_k_rot, build_input_v_rot, state_write (+17) |
| `llama.cpp/src/llama-graph.h` | get_kq_mask, get_kq_mask_swa, get_k_idxs, get_v_idxs, get_kq_mask (+15) |
| `whisper.cpp/examples/talk-llama/llama-model-loader.cpp` | validate_override, get_arr_n, get_key, get_key_or_arr, require_weight (+13) |

## Entry Points

Start here when exploring this area:

- **`ggml_set_input`** (Function) — `ggml/include/ggml.h:863`
- **`format`** (Function) — `llama.cpp/src/llama-impl.h:65`
- **`ggml_backend_sched_synchronize`** (Function) — `ggml/include/ggml-backend.h:343`
- **`llama_get_logits`** (Function) — `whisper.cpp/examples/talk-llama/llama-context.cpp:3061`
- **`llama_get_logits_ith`** (Function) — `whisper.cpp/examples/talk-llama/llama-context.cpp:3067`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `llama_kv_cache_context` | Class | `llama.cpp/src/llama-graph.h` | 23 |
| `llama_memory_recurrent_context` | Class | `llama.cpp/src/llama-graph.h` | 25 |
| `llama_memory_recurrent` | Class | `llama.cpp/src/llama-memory-recurrent.h` | 16 |
| `llama_kv_cache` | Class | `llama.cpp/src/llama-kv-cache.h` | 19 |
| `llama_kv_cache_iswa` | Class | `llama.cpp/src/llama-kv-cache-iswa.h` | 13 |
| `ggml_set_input` | Function | `ggml/include/ggml.h` | 863 |
| `format` | Function | `llama.cpp/src/llama-impl.h` | 65 |
| `ggml_backend_sched_synchronize` | Function | `ggml/include/ggml-backend.h` | 343 |
| `llama_get_logits` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3061 |
| `llama_get_logits_ith` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3067 |
| `llama_get_embeddings` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3081 |
| `llama_get_embeddings_ith` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3087 |
| `llama_get_embeddings_seq` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3093 |
| `llama_get_sampled_token_ith` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3103 |
| `llama_get_sampled_probs_ith` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3109 |
| `llama_get_sampled_logits_ith` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3115 |
| `llama_get_sampled_candidates_ith` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3121 |
| `llama_get_sampled_candidates_count_ith` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3127 |
| `llama_get_sampled_logits_count_ith` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3133 |
| `llama_get_sampled_probs_count_ith` | Function | `whisper.cpp/examples/talk-llama/llama-context.cpp` | 3139 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → __dtype_to_type` | cross_community | 7 |
| `Main → __type_name` | cross_community | 6 |
| `Main → __get_shape` | cross_community | 6 |
| `Main → __is_contiguous` | cross_community | 5 |
| `Main → __get_strides` | cross_community | 5 |
| `Main → __get_data` | cross_community | 4 |
| `Set_input → _get_request_headers` | cross_community | 4 |
| `Main → Whisper_print_usage` | intra_community | 3 |
| `Build_attn → GGML_ASSERT` | cross_community | 3 |
| `Build_attn → Cb` | cross_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tests | 126 calls |
| Include | 38 calls |
| Models | 31 calls |
| Perplexity | 27 calls |
| Examples | 11 calls |
| Cluster_323 | 10 calls |
| Dpct | 9 calls |
| Ggml-rpc | 8 calls |

## How to Explore

1. `gitnexus_context({name: "ggml_set_input"})` — see callers and callees
2. `gitnexus_query({query: "talk-llama"})` — find related execution flows
3. Read key files listed above for implementation details
