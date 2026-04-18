"""
GGUF Weight Extractor

Parses GGUF (GPT-Generated Unified Format) model files and extracts
weight tensors as NumPy arrays for downstream pattern analysis.

GGUF format structure:
  - Header: magic "gguf" + version + metadata count + tensor count + tensor offset
  - Metadata: key-value pairs (tensor names, shapes, dtypes)
  - Tensor data: raw weight arrays at specified offsets

Supported dtypes: int8, uint8, float16, float32, float64
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

# GGUF magic number (bytes: "GGUF" = 0x47475546)
# When read as uint32 LE: 0x47475546
# When read as uint32 BE: 0x46554747
_GGUF_MAGIC_LE: int = 0x47475546
_GGUF_MAGIC_BE: int = 0x46554747

# GGUF version
_GGUF_VERSION: int = 1

# Tensor data types (GGUF tensor_type enum)
_TENSOR_TYPE_MAP: dict[int, np.dtype] = {
    0: np.dtype("int8"),  # GGUF_TYPE_INT8
    1: np.dtype("uint8"),  # GGUF_TYPE_UINT8
    2: np.dtype("float16"),  # GGUF_TYPE_FLOAT16
    3: np.dtype("float32"),  # GGUF_TYPE_FLOAT32
    4: np.dtype("float64"),  # GGUF_TYPE_FLOAT64
}

# Element sizes in bytes per dtype
_DTYPE_BYTE_SIZE: dict[np.dtype, int] = {
    np.dtype("int8"): 1,
    np.dtype("uint8"): 1,
    np.dtype("float16"): 2,
    np.dtype("float32"): 4,
    np.dtype("float64"): 8,
}


@dataclass
class TensorInfo:
    """Metadata about a single tensor in the GGUF file."""

    name: str
    shape: tuple[int, ...]
    dtype: np.dtype
    offset: int  # byte offset from start of tensor data section

    @property
    def element_count(self) -> int:
        """Total number of elements in the tensor."""
        return int(np.prod(self.shape)) if self.shape else 0

    @property
    def byte_size(self) -> int:
        """Total size in bytes."""
        return self.element_count * _DTYPE_BYTE_SIZE.get(self.dtype, 0)


@dataclass
class GGUFMetadata:
    """Parsed metadata from a GGUF file header."""

    version: int = 0
    tensor_count: int = 0
    metadata_offset: int = 0
    tensor_offset: int = 0
    kv_pairs: dict[str, Any] = field(default_factory=dict)
    tensors: list[TensorInfo] = field(default_factory=list)


class GGUFExtractor:
    """Extract weight tensors from GGUF model files.

    Usage:
        extractor = GGUFExtractor("path/to/model.gguf")
        weights = extractor.extract_tensor("model.layers.0.self_attn.q_proj.weight")
        # Returns numpy array with correct shape and dtype

    The extracted weights are ready for SVD decomposition, correlation analysis,
    or any other pattern extraction downstream.
    """

    def __init__(self, path: str | Path) -> None:
        """Open a GGUF file for reading.

        Args:
            path: Path to the .gguf model file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a valid GGUF format.
        """
        self._path = Path(path)
        if not self._path.exists():
            raise FileNotFoundError(f"GGUF file not found: {self._path}")

        self._metadata = self._parse_header()

    @property
    def path(self) -> Path:
        """Path to the GGUF file."""
        return self._path

    @property
    def metadata(self) -> GGUFMetadata:
        """Parsed metadata (lazy-loaded on first access)."""
        return self._metadata

    @property
    def tensor_names(self) -> list[str]:
        """List of all tensor names in the file."""
        return [t.name for t in self._metadata.tensors]

    @property
    def tensor_count(self) -> int:
        """Total number of tensors."""
        return self._metadata.tensor_count

    def get_tensor_info(self, name: str) -> TensorInfo | None:
        """Get metadata for a tensor by name.

        Args:
            name: Tensor name (e.g., "model.layers.0.self_attn.q_proj.weight").

        Returns:
            TensorInfo or None if not found.
        """
        for t in self._metadata.tensors:
            if t.name == name:
                return t
        return None

    def get_tensor_shape(self, name: str) -> tuple[int, ...] | None:
        """Get the shape of a tensor by name."""
        info = self.get_tensor_info(name)
        return info.shape if info else None

    def get_tensor_dtype(self, name: str) -> np.dtype | None:
        """Get the dtype of a tensor by name."""
        info = self.get_tensor_info(name)
        return info.dtype if info else None

    def extract_tensor(self, name: str) -> np.ndarray | None:
        """Extract a single tensor as a NumPy array.

        Args:
            name: Tensor name to extract.

        Returns:
            NumPy array with correct shape and dtype, or None if not found.

        Raises:
            IOError: If the file cannot be read at the tensor offset.
        """
        info = self.get_tensor_info(name)
        if info is None:
            return None

        # Read raw bytes from file at tensor offset
        with open(self._path, "rb") as f:
            f.seek(info.offset)
            raw_bytes = f.read(info.byte_size)

        if len(raw_bytes) != info.byte_size:
            raise IOError(
                f"Expected {info.byte_size} bytes for tensor '{name}', got {len(raw_bytes)}"
            )

        # Convert raw bytes to numpy array
        arr = np.frombuffer(raw_bytes, dtype=info.dtype)

        # Reshape to tensor shape
        if info.shape:
            arr = arr.reshape(info.shape)

        return arr

    def extract_all_tensors(self) -> dict[str, np.ndarray]:
        """Extract all tensors from the GGUF file.

        Returns:
            Dict mapping tensor names to NumPy arrays.

        Note:
            This can use significant memory for large models (e.g., 111GB weights).
            Consider extracting only needed tensors instead.
        """
        result: dict[str, np.ndarray] = {}
        for name in self.tensor_names:
            tensor = self.extract_tensor(name)
            if tensor is not None:
                result[name] = tensor
        return result

    def get_layer_tensors(self, layer_index: int) -> list[str]:
        """Get all tensor names belonging to a specific model layer.

        Args:
            layer_index: Zero-based layer index (e.g., 0 for first transformer block).

        Returns:
            List of tensor names in that layer.
        """
        prefix = f"model.layers.{layer_index}."
        return [name for name in self.tensor_names if name.startswith(prefix)]

    def get_weight_keys(self, pattern: str = "*.weight") -> list[str]:
        """Get all tensor names matching a glob pattern.

        Args:
            pattern: Glob-style pattern (e.g., "*.weight", "model.layers.*.q_proj.weight").

        Returns:
            List of matching tensor names.
        """
        import fnmatch

        return [name for name in self.tensor_names if fnmatch.fnmatch(name, pattern)]

    def get_model_info(self) -> dict[str, Any]:
        """Extract model metadata from GGUF kv pairs.

        Returns:
            Dict with model info (name, architecture, vocab size, etc.).
        """
        info: dict[str, Any] = {}

        # Common GGUF metadata keys for LLMs
        key_map = {
            "general.name": "name",
            "general.architecture": "architecture",
            "general.file_type": "file_type",
            "general.quantization_version": "quantization_version",
            "llm.vocab_size": "vocab_size",
            "llm.context_length": "context_length",
            "llm.embedding_length": "embedding_size",
            "llm.block_count": "num_layers",
            "llm.attention.head_count": "num_attention_heads",
            "llm.attention.head_count_kv": "num_kv_heads",
            "llm.feed_forward_length": "ffn_dim",
            "llm.rope.dimension_count": "rope_dim",
            "llm.norm.epsilon": "norm_epsilon",
            "llm.token_dropout_probability": "token_dropout_p",
        }

        for gguf_key, info_key in key_map.items():
            if gguf_key in self._metadata.kv_pairs:
                info[info_key] = self._metadata.kv_pairs[gguf_key]

        return info

    # ---- Internal: GGUF header parsing ----

    def _parse_header(self) -> GGUFMetadata:
        """Parse the GGUF file header and return metadata.

        Reads:
          - Magic number (uint32)
          - Version (uint32)
          - Metadata KV count (uint64)
          - Tensor count (uint64)
          - Tensor data offset (uint64)
          - Metadata KV pairs
          - Tensor info entries

        Returns:
            Parsed GGUFMetadata.
        """
        with open(self._path, "rb") as f:
            # Read header
            magic = struct.unpack("<I", f.read(4))[0]  # uint32 LE
            if magic not in (_GGUF_MAGIC_LE, _GGUF_MAGIC_BE):
                # Try reading as big-endian to confirm
                magic_be = struct.unpack(">I", f.read(4))[0]
                if magic_be not in (_GGUF_MAGIC_LE, _GGUF_MAGIC_BE):
                    raise ValueError(
                        f"Not a valid GGUF file (magic=0x{magic:08x}, "
                        f"expected 0x{_GGUF_MAGIC_LE:08x} or 0x{_GGUF_MAGIC_BE:08x})"
                    )
                # File is big-endian — need to read all subsequent values as BE
                version = struct.unpack(">I", f.read(4))[0]
                metadata_kv_count = struct.unpack(">Q", f.read(8))[0]
                tensor_count = struct.unpack(">Q", f.read(8))[0]
                tensor_offset = struct.unpack(">Q", f.read(8))[0]

                metadata = GGUFMetadata(
                    version=version,
                    tensor_count=tensor_count,
                    metadata_offset=f.tell(),
                    tensor_offset=tensor_offset,
                )

                # Read metadata KV pairs (big-endian)
                for _ in range(metadata_kv_count):
                    name = self._read_string_be(f)
                    tensor_type = struct.unpack(">I", f.read(4))[0]
                    value = self._read_value_be(f, tensor_type)
                    metadata.kv_pairs[name] = value

                # Read tensor info entries (big-endian)
                for _ in range(tensor_count):
                    name = self._read_string_be(f)
                    ndim = struct.unpack(">I", f.read(4))[0]
                    shape = tuple(struct.unpack(">Q", f.read(8))[0] for _ in range(ndim))
                    dtype_type = struct.unpack(">I", f.read(4))[0]
                    dtype = _TENSOR_TYPE_MAP.get(dtype_type, np.dtype("float32"))
                    offset = struct.unpack(">Q", f.read(8))[0]

                    metadata.tensors.append(
                        TensorInfo(
                            name=name,
                            shape=shape,
                            dtype=dtype,
                            offset=offset + tensor_offset,
                        )
                    )

                return metadata

            if magic != _GGUF_MAGIC_LE:
                raise ValueError(
                    f"Not a valid GGUF file (magic=0x{magic:08x}, expected 0x{_GGUF_MAGIC_LE:08x})"
                )

            version = struct.unpack("<I", f.read(4))[0]
            if version != _GGUF_VERSION:
                raise ValueError(f"Unsupported GGUF version: {version}")

            metadata_kv_count = struct.unpack("<Q", f.read(8))[0]  # uint64 LE
            tensor_count = struct.unpack("<Q", f.read(8))[0]  # uint64 LE
            tensor_offset = struct.unpack("<Q", f.read(8))[0]  # uint64 LE

            metadata = GGUFMetadata(
                version=version,
                tensor_count=tensor_count,
                metadata_offset=f.tell(),
                tensor_offset=tensor_offset,
            )

            # Read metadata KV pairs
            for _ in range(metadata_kv_count):
                name = self._read_string(f)
                tensor_type = struct.unpack("<I", f.read(4))[0]
                value = self._read_value(f, tensor_type)
                metadata.kv_pairs[name] = value

            # Read tensor info entries
            for _ in range(tensor_count):
                name = self._read_string(f)
                ndim = struct.unpack("<I", f.read(4))[0]
                shape = tuple(struct.unpack("<Q", f.read(8))[0] for _ in range(ndim))
                dtype_type = struct.unpack("<I", f.read(4))[0]
                dtype = _TENSOR_TYPE_MAP.get(dtype_type, np.dtype("float32"))
                offset = struct.unpack("<Q", f.read(8))[0]

                metadata.tensors.append(
                    TensorInfo(
                        name=name,
                        shape=shape,
                        dtype=dtype,
                        offset=offset + tensor_offset,  # absolute offset in file
                    )
                )

        return metadata

    @staticmethod
    def _read_string(f: Any) -> str:
        """Read a GGUF string (uint64 length + UTF-8 bytes)."""
        length = struct.unpack("<Q", f.read(8))[0]  # uint64 LE
        return f.read(length).decode("utf-8")

    @staticmethod
    def _read_value(f: Any, tensor_type: int) -> Any:
        """Read a GGUF metadata value based on tensor type."""
        if tensor_type == 0:  # int8
            return struct.unpack("<b", f.read(1))[0]
        elif tensor_type == 1:  # uint8
            return struct.unpack("<B", f.read(1))[0]
        elif tensor_type == 2:  # float16
            return struct.unpack("<e", f.read(2))[0]  # half-float
        elif tensor_type == 3:  # float32
            return struct.unpack("<f", f.read(4))[0]  # single-float
        elif tensor_type == 4:  # float64
            return struct.unpack("<d", f.read(8))[0]  # double-float
        elif tensor_type == 5:  # bool (uint8)
            return struct.unpack("<B", f.read(1))[0] != 0
        elif tensor_type == 6:  # int16
            return struct.unpack("<h", f.read(2))[0]
        elif tensor_type == 7:  # int32
            return struct.unpack("<i", f.read(4))[0]
        elif tensor_type == 8:  # int64
            return struct.unpack("<q", f.read(8))[0]
        elif tensor_type == 9:  # float16 as uint16
            raw = struct.unpack("<H", f.read(2))[0]
            return np.float16.frombytes(struct.pack("<H", raw)).item()
        elif tensor_type == 10:  # uint16
            return struct.unpack("<H", f.read(2))[0]
        elif tensor_type == 11:  # uint64
            return struct.unpack("<Q", f.read(8))[0]
        elif tensor_type == 12:  # int64 as uint (signed)
            return struct.unpack("<q", f.read(8))[0]
        elif tensor_type == 13:  # string list
            count = struct.unpack("<Q", f.read(8))[0]
            return [GGUFExtractor._read_string(f) for _ in range(count)]
        elif tensor_type == 14:  # int list
            count = struct.unpack("<Q", f.read(8))[0]
            return [struct.unpack("<q", f.read(8))[0] for _ in range(count)]
        elif tensor_type == 15:  # float list
            count = struct.unpack("<Q", f.read(8))[0]
            return [struct.unpack("<f", f.read(4))[0] for _ in range(count)]
        else:
            # Unknown type — try to skip and return None
            return None

    @staticmethod
    def _read_string_be(f: Any) -> str:
        """Read a GGUF string (uint64 length BE + UTF-8 bytes)."""
        length = struct.unpack(">Q", f.read(8))[0]  # uint64 BE
        return f.read(length).decode("utf-8")

    @staticmethod
    def _read_value_be(f: Any, tensor_type: int) -> Any:
        """Read a GGUF metadata value based on tensor type (big-endian)."""
        if tensor_type == 0:  # int8
            return struct.unpack(">b", f.read(1))[0]
        elif tensor_type == 1:  # uint8
            return struct.unpack(">B", f.read(1))[0]
        elif tensor_type == 2:  # float16
            return struct.unpack(">e", f.read(2))[0]
        elif tensor_type == 3:  # float32
            return struct.unpack(">f", f.read(4))[0]
        elif tensor_type == 4:  # float64
            return struct.unpack(">d", f.read(8))[0]
        elif tensor_type == 5:  # bool (uint8)
            return struct.unpack(">B", f.read(1))[0] != 0
        elif tensor_type == 6:  # int16
            return struct.unpack(">h", f.read(2))[0]
        elif tensor_type == 7:  # int32
            return struct.unpack(">i", f.read(4))[0]
        elif tensor_type == 8:  # int64
            return struct.unpack(">q", f.read(8))[0]
        elif tensor_type == 9:  # float16 as uint16
            raw = struct.unpack(">H", f.read(2))[0]
            return np.float16.frombytes(struct.pack(">H", raw)).item()
        elif tensor_type == 10:  # uint16
            return struct.unpack(">H", f.read(2))[0]
        elif tensor_type == 11:  # uint64
            return struct.unpack(">Q", f.read(8))[0]
        elif tensor_type == 12:  # int64 as uint (signed)
            return struct.unpack(">q", f.read(8))[0]
        elif tensor_type == 13:  # string list
            count = struct.unpack(">Q", f.read(8))[0]
            return [GGUFExtractor._read_string_be(f) for _ in range(count)]
        elif tensor_type == 14:  # int list
            count = struct.unpack(">Q", f.read(8))[0]
            return [struct.unpack(">q", f.read(8))[0] for _ in range(count)]
        elif tensor_type == 15:  # float list
            count = struct.unpack(">Q", f.read(8))[0]
            return [struct.unpack(">f", f.read(4))[0] for _ in range(count)]
        else:
            return None

    def __repr__(self) -> str:
        info = self.get_model_info()
        arch = info.get("architecture", "unknown")
        return f"GGUFExtractor(path={self._path}, arch={arch}, tensors={self.tensor_count})"


def extract_gguf_weights(
    path: str | Path,
    pattern: str = "*.weight",
) -> dict[str, np.ndarray]:
    """Convenience function to extract weight tensors matching a pattern.

    Args:
        path: Path to GGUF file.
        pattern: Glob pattern for tensor names (default: "*.weight").

    Returns:
        Dict mapping matching tensor names to NumPy arrays.
    """
    extractor = GGUFExtractor(path)
    matching_names = extractor.get_weight_keys(pattern)

    result: dict[str, np.ndarray] = {}
    for name in matching_names:
        tensor = extractor.extract_tensor(name)
        if tensor is not None:
            result[name] = tensor

    return result


def get_gguf_model_info(path: str | Path) -> dict[str, Any]:
    """Quick helper to get model info from a GGUF file.

    Args:
        path: Path to GGUF file.

    Returns:
        Dict with model metadata (name, architecture, layers, etc.).
    """
    return GGUFExtractor(path).get_model_info()
