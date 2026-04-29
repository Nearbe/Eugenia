---
name: examples
description: "Skill for the Examples area of Eugenia. 373 symbols across 33 files."
---

# Examples

373 symbols | 33 files | Cohesion: 66%

## When to Use

- Working with code in `ggml/`
- Understanding how stb_vorbis_decode_frame_pushdata, stb_vorbis_seek_frame, inverse_mdct work
- Modifying examples-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `ggml/examples/stb_image.h` | stbi__rewind, stbi__jpeg_test, stbi__jpeg_load, stbi__jpeg_info, stbi__png_test (+154) |
| `whisper.cpp/examples/stb_vorbis.c` | stb_vorbis_decode_frame_pushdata, stb_vorbis_seek_frame, error, ilog, get8 (+74) |
| `ggml/examples/stb_image_write.h` | stbiw__writefv, stbiw__writef, stbiw__write_flush, stbiw__write1, stbiw__write3 (+33) |
| `whisper.cpp/examples/grammar-parser.cpp` | get_symbol_id, is_word_char, parse_name, parse_char, parse_sequence (+7) |
| `whisper.cpp/examples/common.cpp` | replace, json_parse, get_next_arg, gpt_params_parse, gpt_print_usage (+3) |
| `ggml/examples/common.cpp` | replace, json_parse, get_next_arg, gpt_params_parse, gpt_print_usage (+3) |
| `whisper.cpp/examples/common.h` | trim, vad_simple, similarity, write_audio, write (+3) |
| `llama.cpp/examples/pydantic_models_to_grammar_examples.py` | create_completion, example_struct, example_concurrent, example_rce, example_calculator (+1) |
| `ggml/examples/common.h` | write_header, write_audio, write, open_wav, open (+1) |
| `whisper.cpp/examples/command/command.cpp` | transcribe, read_allowed_commands, process_command_list, always_prompt_transcription, process_general_transcription |

## Entry Points

Start here when exploring this area:

- **`stb_vorbis_decode_frame_pushdata`** (Function) — `whisper.cpp/examples/stb_vorbis.c:196`
- **`stb_vorbis_seek_frame`** (Function) — `whisper.cpp/examples/stb_vorbis.c:297`
- **`inverse_mdct`** (Function) — `whisper.cpp/examples/stb_vorbis.c:2387`
- **`replace`** (Function) — `whisper.cpp/examples/common.cpp:140`
- **`json_parse`** (Function) — `whisper.cpp/examples/common.cpp:154`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `DataType` | Class | `llama.cpp/examples/convert_legacy_llama.py` | 60 |
| `QuantizedDataType` | Class | `llama.cpp/examples/convert_legacy_llama.py` | 81 |
| `stb_vorbis_decode_frame_pushdata` | Function | `whisper.cpp/examples/stb_vorbis.c` | 196 |
| `stb_vorbis_seek_frame` | Function | `whisper.cpp/examples/stb_vorbis.c` | 297 |
| `inverse_mdct` | Function | `whisper.cpp/examples/stb_vorbis.c` | 2387 |
| `replace` | Function | `whisper.cpp/examples/common.cpp` | 140 |
| `json_parse` | Function | `whisper.cpp/examples/common.cpp` | 154 |
| `common_json_parse` | Function | `llama.cpp/common/json-partial.cpp` | 22 |
| `parse_cpu_range` | Function | `llama.cpp/common/common.cpp` | 289 |
| `parse_cpu_mask` | Function | `llama.cpp/common/common.cpp` | 326 |
| `common_tokenize` | Function | `llama.cpp/common/common.cpp` | 1570 |
| `trim_whitespace` | Function | `llama.cpp/common/chat-auto-parser-helpers.cpp` | 14 |
| `replace` | Function | `ggml/examples/common.cpp` | 140 |
| `json_parse` | Function | `ggml/examples/common.cpp` | 154 |
| `trim` | Function | `whisper.cpp/examples/common.h` | 53 |
| `vad_simple` | Function | `whisper.cpp/examples/common.h` | 242 |
| `similarity` | Function | `whisper.cpp/examples/common.h` | 251 |
| `sdl_poll_events` | Function | `whisper.cpp/examples/common-sdl.h` | 48 |
| `command_get_audio` | Function | `whisper.cpp/examples/command.wasm/emscripten.cpp` | 73 |
| `command_main` | Function | `whisper.cpp/examples/command.wasm/emscripten.cpp` | 87 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → Whisper_print_usage` | intra_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tests | 13 calls |
| Vdot | 4 calls |
| Stream.wasm | 4 calls |
| Models | 3 calls |
| Transcendental | 3 calls |
| Perplexity | 3 calls |
| Dpct | 2 calls |
| Ggml-sycl | 2 calls |

## How to Explore

1. `gitnexus_context({name: "stb_vorbis_decode_frame_pushdata"})` — see callers and callees
2. `gitnexus_query({query: "examples"})` — find related execution flows
3. Read key files listed above for implementation details
