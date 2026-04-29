#!/usr/bin/env python3
"""Universal Knowledge Protocol on Eugenia core math."""

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
import hashlib
import struct
from dataclasses import dataclass
from typing import Dict, List

from core.linear.linear_algebra import CoreMatrix, CoreVector, cosine_similarity, mat_vec, to_vector
from nucleus.cross_layer_compressor import compress_layer

FLOAT_BYTES = 4


@dataclass
class UniversalMap:
    """Универсальная карта знаний."""

    P: CoreMatrix
    S: CoreVector
    k: int
    d: int


class UniversalKnowledgeProtocol:
    """Протокол универсальных знаний."""

    def __init__(self, k: int = 32):
        self.k = k
        self.maps: Dict[str, UniversalMap] = {}
        self.signature: str = ""

    def learn(self, weights: Dict[str, object]) -> "UniversalKnowledgeProtocol":
        for name, matrix in weights.items():
            layer = compress_layer(matrix, self.k)
            rows, _ = layer["U"].shape
            self.maps[name] = UniversalMap(P=layer["U"], S=layer["S"], k=self.k, d=rows)
        self._generate_signature()
        return self

    def _generate_signature(self):
        hasher = hashlib.sha256()
        for name in sorted(self.maps.keys()):
            mapping = self.maps[name]
            hasher.update(name.encode())
            hasher.update(repr(mapping.P).encode())
            hasher.update(repr(mapping.S).encode())
        self.signature = hasher.hexdigest()[:16]

    def encode(self, layer: str, x):
        mapping = self.maps.get(layer)
        if mapping is None:
            return CoreVector(to_vector(x))
        projection = mat_vec(mapping.P.T, x)
        return CoreVector(value * mapping.S[index] for index, value in enumerate(projection))

    def similarity(self, layer: str, x1, x2) -> float:
        p1 = self.encode(layer, x1)
        p2 = self.encode(layer, x2)
        if not p1 and not p2:
            return 1.0
        if not p1 or not p2:
            return 0.0
        return float(cosine_similarity(p1, p2))

    def cluster(self, layer: str, items: List[object], n_clusters: int = 5) -> List[List[int]]:
        clusters: list[list[int]] = [[] for _ in range(max(n_clusters, 1))]
        for index, _ in enumerate(items):
            clusters[index % len(clusters)].append(index)
        return clusters

    def get_compressed_size(self) -> int:
        return sum((mapping.P.size + mapping.S.size) * FLOAT_BYTES for mapping in self.maps.values())

    def save(self) -> bytes:
        data = bytearray()
        data += struct.pack("<I", self.k)
        data += struct.pack("<I", len(self.maps))
        for name, mapping in self.maps.items():
            name_bytes = name.encode("utf-8")
            data += struct.pack("<I", len(name_bytes))
            data += name_bytes
            data += struct.pack("<I", mapping.d)
            for row in mapping.P:
                for value in row:
                    data += struct.pack("<f", float(value))
            for value in mapping.S:
                data += struct.pack("<f", float(value))
        data += self.signature.encode("utf-8")
        return bytes(data)

    @classmethod
    def load(cls, data: bytes) -> "UniversalKnowledgeProtocol":
        proto = cls()
        offset = 0
        proto.k = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4
        map_count = struct.unpack("<I", data[offset : offset + 4])[0]
        offset += 4
        for _ in range(map_count):
            name_len = struct.unpack("<I", data[offset : offset + 4])[0]
            offset += 4
            name = data[offset : offset + name_len].decode("utf-8")
            offset += name_len
            d = struct.unpack("<I", data[offset : offset + 4])[0]
            offset += 4
            rows = []
            for _ in range(d):
                row = []
                for _ in range(proto.k):
                    row.append(struct.unpack("<f", data[offset : offset + 4])[0])
                    offset += 4
                rows.append(row)
            singular = CoreVector()
            for _ in range(proto.k):
                singular.append(struct.unpack("<f", data[offset : offset + 4])[0])
                offset += 4
            proto.maps[name] = UniversalMap(P=CoreMatrix(rows), S=singular, k=proto.k, d=d)
        proto.signature = data[offset : offset + 16].decode("utf-8") if offset + 16 <= len(data) else ""
        return proto


def demo():
    weights = {"layer_0": CoreMatrix([[0.1 for _ in range(16)] for _ in range(16)])}
    protocol = UniversalKnowledgeProtocol(k=4).learn(weights)
    print(protocol.signature)


if __name__ == "__main__":
    demo()
