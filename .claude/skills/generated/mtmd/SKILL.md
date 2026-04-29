---
name: mtmd
description: "Skill for the Mtmd area of Eugenia. 159 symbols across 18 files."
---

# Mtmd

159 symbols | 18 files | Cohesion: 57%

## When to Use

- Working with code in `llama.cpp/`
- Understanding how process_mtmd_prompt, tokenize_input_prompts, mtmd_bitmap_get_n_bytes work
- Modifying mtmd-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `llama.cpp/tools/mtmd/mtmd.cpp` | mtmd_bitmap_get_n_bytes, mtmd_debug_preprocess_image, mtmd_debug_preprocess_audio, tokenize, add_text (+32) |
| `llama.cpp/tools/mtmd/mtmd-image.cpp` | resize, crop, resize_bilinear, resize_bicubic, resize_bicubic_pillow (+25) |
| `llama.cpp/tools/mtmd/clip.cpp` | proj_type, clip_image_build_graph, clip_n_output_tokens_x, clip_n_output_tokens, clip_image_encode (+19) |
| `llama.cpp/tools/mtmd/mtmd-helper.cpp` | decode_embd_batch, set_position_normal, set_position_mrope_2d, set_position_mrope_1d, get_view (+9) |
| `llama.cpp/tools/mtmd/mtmd-audio.cpp` | fill_sin_cos_table, fill_hann_window, fill_mel_filterbank_matrix, initialize, mtmd_audio_streaming_istft (+8) |
| `llama.cpp/tools/mtmd/mtmd.h` | n_bytes, set_id, c_ptr, size, data (+4) |
| `llama.cpp/tools/mtmd/mtmd-cli.cpp` | check_antiprompt, load_media, init_vision_context, chat_add_and_format, eval_message (+1) |
| `llama.cpp/tools/mtmd/clip.h` | clip_n_output_tokens, clip_init, clip_n_mmproj_embd, clip_image_encode, clip_is_minicpmv (+1) |
| `llama.cpp/tools/server/server-common.cpp` | server_tokens, process_mtmd_prompt, tokenize_input_subprompt, tokenize_input_prompts, process_chunk |
| `llama.cpp/tools/mtmd/clip-model.h` | audio_has_stack_frames, set_limit_image_tokens, set_warmup_n_tokens, clip_get_hparams, audio_has_avgpool |

## Entry Points

Start here when exploring this area:

- **`process_mtmd_prompt`** (Function) — `llama.cpp/tools/server/server-common.cpp:715`
- **`tokenize_input_prompts`** (Function) — `llama.cpp/tools/server/server-common.cpp:792`
- **`mtmd_bitmap_get_n_bytes`** (Function) — `llama.cpp/tools/mtmd/mtmd.cpp:1150`
- **`mtmd_debug_preprocess_image`** (Function) — `llama.cpp/tools/mtmd/mtmd.cpp:1462`
- **`mtmd_debug_preprocess_audio`** (Function) — `llama.cpp/tools/mtmd/mtmd.cpp:1485`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `process_mtmd_prompt` | Function | `llama.cpp/tools/server/server-common.cpp` | 715 |
| `tokenize_input_prompts` | Function | `llama.cpp/tools/server/server-common.cpp` | 792 |
| `mtmd_bitmap_get_n_bytes` | Function | `llama.cpp/tools/mtmd/mtmd.cpp` | 1150 |
| `mtmd_debug_preprocess_image` | Function | `llama.cpp/tools/mtmd/mtmd.cpp` | 1462 |
| `mtmd_debug_preprocess_audio` | Function | `llama.cpp/tools/mtmd/mtmd.cpp` | 1485 |
| `clip_n_output_tokens` | Function | `llama.cpp/tools/mtmd/clip.h` | 63 |
| `clip_n_output_tokens_x` | Function | `llama.cpp/tools/mtmd/clip.cpp` | 2863 |
| `clip_n_output_tokens` | Function | `llama.cpp/tools/mtmd/clip.cpp` | 2905 |
| `clip_image_encode` | Function | `llama.cpp/tools/mtmd/clip.cpp` | 3114 |
| `clip_image_batch_encode` | Function | `llama.cpp/tools/mtmd/clip.cpp` | 3123 |
| `mtmd_helper_decode_image_chunk` | Function | `llama.cpp/tools/mtmd/mtmd-helper.cpp` | 235 |
| `mtmd_decode_use_non_causal` | Function | `llama.cpp/tools/mtmd/mtmd.cpp` | 1075 |
| `clip_get_projector_type` | Function | `llama.cpp/tools/mtmd/clip-impl.h` | 672 |
| `mtmd_bitmap_init` | Function | `llama.cpp/tools/mtmd/mtmd.cpp` | 1114 |
| `mtmd_bitmap_init_from_audio` | Function | `llama.cpp/tools/mtmd/mtmd.cpp` | 1126 |
| `mtmd_helper_bitmap_init_from_buf` | Function | `llama.cpp/tools/mtmd/mtmd-helper.cpp` | 480 |
| `mtmd_helper_bitmap_init_from_file` | Function | `llama.cpp/tools/mtmd/mtmd-helper.cpp` | 510 |
| `main` | Function | `llama.cpp/tests/test-mtmd-c-api.c` | 5 |
| `mtmd_input_chunks_free` | Function | `llama.cpp/tools/mtmd/mtmd.h` | 158 |
| `mtmd_input_chunks_init` | Function | `llama.cpp/tools/mtmd/mtmd.cpp` | 1178 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → LOG` | intra_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tests | 26 calls |
| Perplexity | 15 calls |
| Server | 11 calls |
| Models | 9 calls |
| Examples | 2 calls |
| Talk-llama | 2 calls |
| Ggml-metal | 1 calls |

## How to Explore

1. `gitnexus_context({name: "process_mtmd_prompt"})` — see callers and callees
2. `gitnexus_query({query: "mtmd"})` — find related execution flows
3. Read key files listed above for implementation details
