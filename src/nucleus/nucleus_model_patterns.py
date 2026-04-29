#!/usr/bin/env python3
"""Nucleus Model Pattern Extractor on Eugenia core math."""

#  Copyright (c) 2026.
#  ╔═══════════════════════════════════╗
#  ║ Русский  ║ English    ║ Ελληνικά  ║
#  ║══════════║════════════║═══════════║
#  ║ Евгений  ║ Eugene     ║ Εὐγένιος  ║
#  ║ Евгения  ║ Eugenia    ║ Εὐγενία   ║
#  ║ Евгеника ║ Eugenics   ║ Εὐγενική  ║
#  ║ Евгениос ║ Eugenius   ║ Εὐγένιος  ║
#  ║ Женя     ║ Zhenya     ║ Ζένια     ║
#  ╚═══════════════════════════════════╝
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from core.linear.linear_algebra import CoreMatrix, CoreVector, to_matrix
from nucleus.cross_layer_compressor import compress_layer, decompress_layer

DEFAULT_RANDOM_SEED = 42
IMAGE_CHANNELS = 3


@dataclass
class ModelProfile:
    name: str
    svd_U: CoreMatrix
    svd_S: CoreVector
    svd_Vt: CoreMatrix
    k: int
    original_shape: Tuple[int, ...]
    layer_type: str
    n_params: int

    @property
    def compression_ratio(self) -> float:
        if len(self.original_shape) < 2:
            return 0.0
        original_size = self.original_shape[0] * self.original_shape[1]
        compressed_size = self.k * (self.original_shape[0] + self.original_shape[1])
        return compressed_size / original_size if original_size else 0.0

    def save(self, path: str):
        payload = {
            "name": self.name,
            "svd_U": self.svd_U.tolist(),
            "svd_S": self.svd_S.tolist(),
            "svd_Vt": self.svd_Vt.tolist(),
            "k": self.k,
            "original_shape": self.original_shape,
            "layer_type": self.layer_type,
        }
        Path(path).write_text(json.dumps(payload), encoding="utf-8")

    @classmethod
    def load(cls, path: str) -> "ModelProfile":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        singular = CoreVector(payload["svd_S"])
        return cls(
            name=payload["name"],
            svd_U=CoreMatrix(payload["svd_U"]),
            svd_S=singular,
            svd_Vt=CoreMatrix(payload["svd_Vt"]),
            k=int(payload["k"]),
            original_shape=tuple(payload["original_shape"]),
            layer_type=payload["layer_type"],
            n_params=int(sum(singular)),
        )


class ModelLoader:
    """Универсальный загрузчик моделей без внешней математики."""

    SUPPORTED_FORMATS = {".gguf", ".mlx", ".safetensors", ".pt", ".pth", ".json"}

    def __init__(self, model_dir: str):
        self.model_dir = Path(model_dir)
        self.layers = {}

    def discover_models(self) -> List[Dict]:
        if not self.model_dir.exists():
            return []
        models = []
        for fp in self.model_dir.rglob("*"):
            if fp.is_file() and fp.suffix.lower() in self.SUPPORTED_FORMATS:
                models.append(
                    {
                        "path": str(fp),
                        "name": fp.stem,
                        "parent": fp.parent.name,
                        "format": fp.suffix.lower(),
                        "size": fp.stat().st_size,
                    }
                )
        return models

    def load_safetensors(self, path: str) -> Dict[str, CoreMatrix]:
        return self._load_generic(path)

    def _load_generic(self, path: str) -> Dict[str, CoreMatrix]:
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"  Не удалось загрузить: {exc}")
            return {}
        if isinstance(payload, list):
            return {"data": to_matrix(payload)}
        if isinstance(payload, dict):
            return {name: to_matrix(value) for name, value in payload.items() if isinstance(value, list)}
        return {}

    def load_layer(self, path: str, layer_name: Optional[str] = None) -> Optional[CoreMatrix]:
        layers = self._load_generic(path)
        if layer_name and layer_name in layers:
            return layers[layer_name]
        return next(iter(layers.values()), None)


class PatternExtractor:
    """Извлекает геометрические паттерны из весов."""

    def __init__(self, k: int = 16):
        self.k = k
        self.profiles = {}

    def extract_from_weights(self, weights, layer_name: str = "linear", layer_type: str = "linear") -> ModelProfile:
        matrix = to_matrix(weights)
        original_shape = matrix.shape
        layer = compress_layer(matrix, self.k)
        singular = CoreVector(layer["S"])
        profile = ModelProfile(
            name=layer_name,
            svd_U=layer["U"],
            svd_S=singular,
            svd_Vt=layer["Vt"],
            k=layer["k"],
            original_shape=original_shape,
            layer_type=layer_type,
            n_params=int(sum(singular)),
        )
        self.profiles[layer_name] = profile
        return profile

    def extract_all_layers(self, layers: Dict[str, object], k: Optional[int] = None) -> Dict[str, ModelProfile]:
        old_k = self.k
        if k is not None:
            self.k = k
        profiles = {}
        for name, weights in layers.items():
            try:
                profiles[name] = self.extract_from_weights(weights, name)
            except Exception as exc:
                print(f"  Слой {name}: ошибка {exc}")
        self.k = old_k
        return profiles

    def compress_weights(self, profile: ModelProfile, coefficients: Optional[CoreVector] = None) -> CoreMatrix:
        if coefficients is None:
            coefficients = profile.svd_S
        return decompress_layer({"U": profile.svd_U, "S": coefficients, "Vt": profile.svd_Vt})

    def get_pattern_geometry(self, profile: ModelProfile) -> dict:
        singular = CoreVector(profile.svd_S)
        total = sum(singular)
        singular_norm = CoreVector(value / (total + 1.0e-10) for value in singular)
        capacity = -sum(value * math.log(value + 1.0e-10, 2) for value in singular_norm)
        energy_concentration = sum(value * value for value in singular_norm)
        return {
            "name": profile.name,
            "layer_type": profile.layer_type,
            "k": profile.k,
            "n_params": profile.n_params,
            "singular_values": singular.tolist(),
            "singular_norm": singular_norm.tolist(),
            "capacity": float(capacity),
            "energy_concentration": float(energy_concentration),
            "original_shape": profile.original_shape,
            "compression_ratio": profile.compression_ratio,
        }

    def generate_profile_image(self, profile: ModelProfile, size: int = 128) -> list[list[list[int]]]:
        singular = CoreVector(profile.svd_S[: min(len(profile.svd_S), size)])
        peak = max(singular) if singular else 1.0
        image = [[[0, 0, 0] for _ in range(size)] for _ in range(size)]
        for index, value in enumerate(singular):
            freq = index / max(len(singular), 1)
            normalized = value / (peak + 1.0e-10)
            y = max(0, min(size - 1, int(normalized * (size - 1))))
            image[y][index % size] = [
                int((math.sin(freq * math.tau) * 0.5 + 0.5) * 255),
                int((math.sin(freq * math.tau + math.pi / 3) * 0.5 + 0.5) * 255),
                int((math.sin(freq * math.tau + math.tau / 3) * 0.5 + 0.5) * 255),
            ]
        return image


def integrate_with_graphics():
    from nucleus_graphics import GeometricEngine

    return GeometricEngine


def demo_extraction():
    rng = random.Random(DEFAULT_RANDOM_SEED)
    weights = CoreMatrix([[rng.gauss(0.0, 1.0) for _ in range(64)] for _ in range(32)])
    extractor = PatternExtractor(k=8)
    profile = extractor.extract_from_weights(weights, "test_layer", "linear")
    print(extractor.get_pattern_geometry(profile))


if __name__ == "__main__":
    demo_extraction()
