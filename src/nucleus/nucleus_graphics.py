#!/usr/bin/env python3
"""Nucleus Graphics Engine on Eugenia core math."""

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
import math
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from core.linear.linear_algebra import CoreMatrix, CoreVector, linspace, mean, to_matrix
from nucleus.cross_layer_compressor import compress_layer, decompress_layer

Pixel = tuple[int, int, int]
Image = list[list[Pixel]]


def compute_betti_numbers(binary) -> Tuple[int, int]:
    return (1, 0)


def compute_euler_characteristic(betti: Tuple[int, int]) -> int:
    return betti[0] - betti[1]


def compute_information_capacity(bits) -> float:
    values = [float(value) for row in to_matrix(bits) for value in row]
    p = mean(values)
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p, 2) - (1.0 - p) * math.log(1.0 - p, 2)


class RenderMode(Enum):
    SDF = "sdf"
    FRACTAL = "fractal"
    HORIZON = "horizon"
    PHASE = "phase"
    TOPOLOGY = "topology"


@dataclass
class GeometricProfile:
    bits: list[CoreMatrix]
    thresholds: CoreVector
    centroids: list[tuple[float, float]]
    betti: Tuple[int, int]
    euler: int
    capacity: float
    complexity: float

    @property
    def pattern_id(self) -> str:
        return f"{self.betti[0]}_{self.betti[1]}_{self.euler}_{self.capacity:.2f}"


@dataclass
class RenderParams:
    width: int = 512
    height: int = 512
    zoom: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    iterations: int = 100
    escape_radius: float = 4.0
    Julia_c: Optional[complex] = None


class GeometricEngine:
    """Геометрический движок — генерирует из паттернов."""

    def __init__(self):
        self.profiles = {}
        self.correlations = {}
        self.render_cache = {}
        self._svd_basis = None

    def register_profile(self, name: str, profile: GeometricProfile):
        self.profiles[name] = profile
        self.correlations[name] = {"strength": 1.0, "uses": 0}

    def boost_correlation(self, name: str, boost: float = 0.1):
        if name in self.correlations:
            self.correlations[name]["strength"] = min(10.0, self.correlations[name]["strength"] + boost)
            self.correlations[name]["uses"] += 1

    def get_correlation_strength(self, name: str) -> float:
        return self.correlations.get(name, {}).get("strength", 1.0)

    def compute_profile(self, data, n_thresholds: int = 50) -> GeometricProfile:
        matrix = self._as_grayscale_matrix(data)
        height, width = matrix.shape
        values = [value for row in matrix for value in row]
        thresholds = linspace(min(values), max(values), n_thresholds) if values else CoreVector()
        bits = []
        for threshold in thresholds:
            bits.append(CoreMatrix([[1.0 if value > threshold else 0.0 for value in row] for row in matrix]))
        mid_idx = len(bits) // 2 if bits else 0
        betti = compute_betti_numbers(bits[mid_idx] if bits else CoreMatrix())
        capacity = compute_information_capacity(bits[-1] if bits else CoreMatrix())
        complexity = self._compute_complexity(bits, thresholds)
        centroids = self._compute_centroids(bits[-1] if bits else CoreMatrix())
        euler = compute_euler_characteristic(betti)
        return GeometricProfile(bits, thresholds, centroids, betti, euler, capacity, complexity)

    def _as_grayscale_matrix(self, data) -> CoreMatrix:
        matrix = to_matrix(data)
        if len(matrix.shape) == 2:
            return matrix
        return matrix

    def _compute_betti(self, binary) -> Tuple[int, int]:
        components = self._count_components(binary)
        inverted = CoreMatrix([[1.0 - value for value in row] for row in to_matrix(binary)])
        holes = max(0, self._count_components(inverted) - 1)
        return (components, holes)

    def _count_components(self, binary) -> int:
        matrix = to_matrix(binary)
        if not matrix:
            return 0
        height, width = matrix.shape
        visited = [[False for _ in range(width)] for _ in range(height)]
        count = 0
        for row in range(height):
            for col in range(width):
                if matrix[row][col] > 0.5 and not visited[row][col]:
                    count += 1
                    stack = [(row, col)]
                    while stack:
                        y, x = stack.pop()
                        if visited[y][x]:
                            continue
                        visited[y][x] = True
                        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                            if 0 <= ny < height and 0 <= nx < width and matrix[ny][nx] > 0.5:
                                stack.append((ny, nx))
        return count

    def _compute_centroids(self, binary) -> list[tuple[float, float]]:
        matrix = to_matrix(binary)
        height, width = matrix.shape
        visited = [[False for _ in range(width)] for _ in range(height)]
        centroids = []
        for row in range(height):
            for col in range(width):
                if matrix[row][col] > 0.5 and not visited[row][col]:
                    pixels = []
                    stack = [(row, col)]
                    while stack:
                        y, x = stack.pop()
                        if visited[y][x]:
                            continue
                        visited[y][x] = True
                        pixels.append((y, x))
                        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                            if 0 <= ny < height and 0 <= nx < width and matrix[ny][nx] > 0.5:
                                stack.append((ny, nx))
                    if pixels:
                        centroids.append((sum(p[0] for p in pixels) / len(pixels), sum(p[1] for p in pixels) / len(pixels)))
        return centroids

    def _compute_complexity(self, bits, thresholds) -> float:
        if len(bits) < 2:
            return 0.0
        component_counts = [self._count_components(binary) for binary in bits]
        diffs = [abs(component_counts[index + 1] - component_counts[index]) for index in range(len(component_counts) - 1)]
        if not diffs:
            return 0.0
        max_idx = max(range(len(diffs)), key=lambda index: diffs[index])
        return thresholds[max_idx]

    def render_sdf(self, params: RenderParams, profile: Optional[GeometricProfile] = None) -> Image:
        return self.render_fractal("mandelbrot", params, profile)

    def _color_by_capacity(self, capacity: float) -> Pixel:
        h = max(0.0, min(1.0, capacity / 10.0))
        return (
            int((math.sin(h * math.tau) * 0.5 + 0.5) * 255),
            int((math.sin(h * math.tau + math.pi / 3) * 0.5 + 0.5) * 255),
            int((math.sin(h * math.tau + math.tau / 3) * 0.5 + 0.5) * 255),
        )

    def render_fractal(
        self,
        formula: str = "mandelbrot",
        params: RenderParams = None,
        profile: Optional[GeometricProfile] = None,
        boost: bool = True,
    ) -> Image:
        if params is None:
            params = RenderParams()
        renderer = {
            "julia": self._render_julia,
            "burning_ship": self._render_burning_ship,
            "newton": self._render_newton,
        }.get(formula, self._render_mandelbrot)
        image = renderer(params)
        if profile is not None and boost:
            for name, candidate in self.profiles.items():
                if candidate is profile:
                    self.boost_correlation(name, boost=0.05)
                    break
        return image

    def _grid_point(self, row: int, col: int, params: RenderParams) -> complex:
        x = -params.zoom + (2 * params.zoom * col / max(params.width - 1, 1)) + params.offset_x
        y = -params.zoom + (2 * params.zoom * row / max(params.height - 1, 1)) + params.offset_y
        return complex(x, y)

    def _render_mandelbrot(self, params: RenderParams) -> Image:
        image: Image = []
        for row in range(params.height):
            line = []
            for col in range(params.width):
                c = self._grid_point(row, col, params)
                z = c
                count = 0
                for iteration in range(params.iterations):
                    if abs(z) >= params.escape_radius:
                        break
                    z = z * z + c
                    count = iteration
                m = count / max(params.iterations, 1)
                line.append(self._phase_color(m))
            image.append(line)
        return image

    def _render_julia(self, params: RenderParams) -> Image:
        c = params.Julia_c if params.Julia_c is not None else complex(-0.4, 0.6)
        image: Image = []
        for row in range(params.height):
            line = []
            for col in range(params.width):
                z = self._grid_point(row, col, params)
                count = 0
                for iteration in range(params.iterations):
                    if abs(z) >= params.escape_radius:
                        break
                    z = z * z + c
                    count = iteration
                m = count / max(params.iterations, 1)
                line.append((int((m**0.5) * 255), int((m**0.3) * 255), int((m**0.7) * 255)))
            image.append(line)
        return image

    def _render_burning_ship(self, params: RenderParams) -> Image:
        image: Image = []
        for row in range(params.height):
            line = []
            for col in range(params.width):
                c = self._grid_point(row, col, params)
                z = c
                count = 0
                for iteration in range(params.iterations):
                    if abs(z) >= params.escape_radius:
                        break
                    z = complex(abs(z.real), abs(z.imag)) ** 2 + c
                    count = iteration
                m = count / max(params.iterations, 1)
                line.append((int(m * 255), int((m**0.5) * 255), int((m**0.3) * 255)))
            image.append(line)
        return image

    def _render_newton(self, params: RenderParams) -> Image:
        image: Image = []
        for row in range(params.height):
            line = []
            for col in range(params.width):
                z = self._grid_point(row, col, params)
                count = 0
                for iteration in range(params.iterations):
                    derivative = 3 * z * z
                    if abs(derivative) < 1.0e-10:
                        break
                    z = z - (z**3 - 1) / derivative
                    count = iteration
                m = count / max(params.iterations, 1)
                angle = math.atan2(z.imag, z.real)
                line.append(
                    (
                        int(((math.sin(angle * 3) + 1) / 2) * m * 255),
                        int(((math.sin(angle * 3 + math.pi / 2) + 1) / 2) * m * 255),
                        int(((math.sin(angle * 3 + math.pi) + 1) / 2) * m * 255),
                    )
                )
            image.append(line)
        return image

    def _phase_color(self, m: float) -> Pixel:
        return (
            int((math.sin(m * math.tau) * 0.5 + 0.5) * 255),
            int((math.sin(m * math.tau + math.pi / 3) * 0.5 + 0.5) * 255),
            int((math.sin(m * math.tau + math.tau / 3) * 0.5 + 0.5) * 255),
        )

    def render_horizon(self, profile: GeometricProfile, params: RenderParams = None) -> Image:
        if params is None:
            params = RenderParams()
        result: Image = [[(0, 0, 0) for _ in range(params.width)] for _ in range(params.height)]
        if not profile.bits:
            return result
        min_threshold = min(profile.thresholds) if profile.thresholds else 0.0
        max_threshold = max(profile.thresholds) if profile.thresholds else 1.0
        for index, threshold in enumerate(profile.thresholds):
            if index >= len(profile.bits):
                break
            layer = profile.bits[index]
            t_norm = (threshold - min_threshold) / (max_threshold - min_threshold + 1.0e-10)
            color = int(t_norm * 255)
            for row in range(min(params.height, len(layer))):
                for col in range(min(params.width, len(layer[row]))):
                    if layer[row][col] > 0.5:
                        result[row][col] = (color, color, color)
        for cy, cx in profile.centroids:
            y, x = int(cy), int(cx)
            if 0 <= y < params.height and 0 <= x < params.width:
                result[y][x] = (255, 0, 0)
        return result

    def compress_profiles(self, k: int = 16) -> dict:
        if not self.profiles:
            return {}
        names = list(self.profiles.keys())
        rows = []
        for profile in self.profiles.values():
            rows.append([value for matrix in profile.bits for row in matrix for value in row])
        basis = compress_layer(CoreMatrix(rows), k)
        basis["names"] = names
        self._svd_basis = basis
        return basis

    def generate_from_basis(self, coefficients, params: RenderParams = None):
        if self._svd_basis is None:
            raise ValueError("Сначала вызови compress_profiles()")
        restored = decompress_layer({"U": self._svd_basis["U"], "S": CoreVector(coefficients), "Vt": self._svd_basis["Vt"]})
        if params is None:
            return restored
        return self.render_horizon(
            GeometricProfile(
                bits=[restored],
                thresholds=linspace(0.0, 1.0, len(restored)),
                centroids=[],
                betti=(0, 0),
                euler=0,
                capacity=0.0,
                complexity=0.0,
            ),
            params,
        )
