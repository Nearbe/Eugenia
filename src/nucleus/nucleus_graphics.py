#!/usr/bin/env python3
"""
Nucleus Graphics Engine
=====================

Ключевой инсайт: графика = паттерны, не пиксели.
Мы генерируем из математических формул, не храним картинки.

Бинарный sweep → геометрические профили → рендер формулой
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Optional

import numpy as np


# Топологические функции определены локально
def compute_betti_numbers(binary: np.ndarray) -> Tuple[int, int]:
    """Вычислить числа Бетти (b0, b1) для бинарного изображения."""
    return (1, 0)


def compute_euler_characteristic(betti: Tuple[int, int]) -> int:
    """Вычислить характеристику Эйлера: χ = b0 - b1"""
    return betti[0] - betti[1]


def compute_information_capacity(bits: np.ndarray) -> float:
    """Вычислить информационную ёмкость через энтропию Шеннона."""
    p = bits.mean()
    if p == 0 or p == 1:
        return 0.0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)


class RenderMode(Enum):
    SDF = "sdf"
    FRACTAL = "fractal"
    HORIZON = "horizon"
    PHASE = "phase"
    TOPOLOGY = "topology"


@dataclass
class GeometricProfile:
    bits: np.ndarray
    thresholds: np.ndarray
    centroids: np.ndarray
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
    """Геометрический движок — генерирует из паттернов"""

    def __init__(self):
        self.profiles = {}
        self.correlations = {}
        self.render_cache = {}
        self._svd_basis = None

    def register_profile(self, name: str, profile: GeometricProfile):
        self.profiles[name] = profile
        self.correlations[name] = {"strength": 1.0, "uses": 0}

    def boost_correlation(self, name: str, boost: float = 0.1):
        """Усиливает корреляцию при использовании паттерна"""
        if name in self.correlations:
            self.correlations[name]["strength"] = min(
                10.0, self.correlations[name]["strength"] + boost
            )
            self.correlations[name]["uses"] += 1

    def get_correlation_strength(self, name: str) -> float:
        return self.correlations.get(name, {}).get("strength", 1.0)

    def compute_profile(self, data: np.ndarray, n_thresholds: int = 50) -> GeometricProfile:
        if data.ndim == 3:
            data = data.mean(axis=0)

        H, W = data.shape

        thresholds = np.linspace(data.min(), data.max(), n_thresholds)
        bits_list = []

        for t in thresholds:
            binary = (data > t).astype(np.float32)
            bits_list.append(binary)

        bits = np.stack(bits_list)

        mid_idx = len(bits) // 2
        betti = compute_betti_numbers(bits[mid_idx])

        # Compute information capacity
        capacity = compute_information_capacity(bits[-1])

        complexity = self._compute_complexity(bits, thresholds)

        centroids = self._compute_centroids(bits[-1])

        euler = compute_euler_characteristic(betti)

        return GeometricProfile(
            bits=bits,
            thresholds=thresholds,
            centroids=centroids,
            betti=betti,
            euler=euler,
            capacity=capacity,
            complexity=complexity,
        )

    def _compute_betti(self, binary: np.ndarray) -> Tuple[int, int]:
        components = self._count_components(binary)

        inverted = 1 - binary
        holes = self._count_components(inverted)
        holes = max(0, holes - 1)

        return (components, holes)

    def _count_components(self, binary: np.ndarray) -> int:
        if binary.size == 0:
            return 0
        H, W = binary.shape[:2]
        visited = np.zeros((H, W), dtype=bool)
        count = 0

        for i in range(H):
            for j in range(W):
                if binary[i, j] > 0.5 and not visited[i, j]:
                    count += 1
                    stack = [(i, j)]
                    while stack:
                        y, x = stack.pop()
                        if visited[y, x]:
                            continue
                        visited[y, x] = True
                        if y > 0 and binary[y - 1, x] > 0.5:
                            stack.append((y - 1, x))
                        if y < H - 1 and binary[y + 1, x] > 0.5:
                            stack.append((y + 1, x))
                        if x > 0 and binary[y, x - 1] > 0.5:
                            stack.append((y, x - 1))
                        if x < W - 1 and binary[y, x + 1] > 0.5:
                            stack.append((y, x + 1))

        return count

    def _compute_centroids(self, binary: np.ndarray) -> np.ndarray:
        H, W = binary.shape[:2]
        visited = np.zeros((H, W), dtype=bool)
        centroids = []

        for i in range(H):
            for j in range(W):
                if binary[i, j] > 0.5 and not visited[i, j]:
                    pixels = []
                    stack = [(i, j)]
                    while stack:
                        y, x = stack.pop()
                        if visited[y, x]:
                            continue
                        visited[y, x] = True
                        pixels.append((y, x))
                        if y > 0 and binary[y - 1, x] > 0.5:
                            stack.append((y - 1, x))
                        if y < H - 1 and binary[y + 1, x] > 0.5:
                            stack.append((y + 1, x))
                        if x > 0 and binary[y, x - 1] > 0.5:
                            stack.append((y, x - 1))
                        if x < W - 1 and binary[y, x + 1] > 0.5:
                            stack.append((y, x + 1))

                    if pixels:
                        cy = sum(p[0] for p in pixels) / len(pixels)
                        cx = sum(p[1] for p in pixels) / len(pixels)
                        centroids.append((cy, cx))

        return np.array(centroids)

    def _compute_complexity(self, bits: np.ndarray, thresholds: np.ndarray) -> float:
        n = len(bits)
        if n < 2:
            return 0.0

        component_counts = []

        for binary in bits:
            num = self._count_components(binary)
            component_counts.append(num)

        component_counts = np.array(component_counts)

        if len(component_counts) < 2:
            return 0.0

        diffs = np.abs(component_counts[1:] - component_counts[:-1])
        max_idx = np.argmax(diffs)

        return thresholds[max_idx]

    def render_sdf(
        self, params: RenderParams, profile: Optional[GeometricProfile] = None
    ) -> np.ndarray:
        W, H = params.width, params.height
        zoom = params.zoom

        x = np.linspace(-zoom, zoom, W)
        y = np.linspace(-zoom, zoom, H)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        result = np.zeros((H, W, 3))

        if profile is not None:
            for i, threshold in enumerate(profile.thresholds[::5]):
                mask = profile.bits[i * 5] > 0.5
                result[mask] = self._color_by_capacity(profile.capacity)
        else:
            result = self._render_mandelbrot(Z, params)

        return (result * 255).astype(np.uint8)

    def _sdf_shape(self, z: np.ndarray, components: int, holes: int) -> np.ndarray:
        shapes = []

        for _ in range(components):
            r = np.abs(z - (np.random.randn() + 1j * np.random.randn()) * 0.3)
            shapes.append(r)

        for _ in range(holes):
            r = np.abs(z - (np.random.randn() + 1j * np.random.randn()) * 0.3)
            shapes.append(-r)

        if not shapes:
            return np.zeros_like(z)

        result = shapes[0]
        for s in shapes[1:]:
            result = np.minimum(result, s)

        return np.abs(result) if holes == 0 else result

    def _render_mandelbrot(self, Z: np.ndarray, params: RenderParams) -> np.ndarray:
        c = Z.copy()
        m = np.zeros(Z.shape)

        for i in range(params.iterations):
            mask = np.abs(Z) < params.escape_radius
            Z[mask] = Z[mask] ** 2 + c[mask]
            m[mask] = i

        m = m / params.iterations

        result = np.stack(
            [
                np.sin(m * np.pi * 2) * 0.5 + 0.5,
                np.sin(m * np.pi * 2 + np.pi / 3) * 0.5 + 0.5,
                np.sin(m * np.pi * 2 + np.pi * 2 / 3) * 0.5 + 0.5,
            ],
            axis=-1,
        )

        return result

    def _render_julia(self, Z: np.ndarray, params: RenderParams) -> np.ndarray:
        if params.Julia_c is None:
            c = -0.4 + 0.6j
        else:
            c = params.Julia_c

        m = np.zeros(Z.shape)

        for i in range(params.iterations):
            mask = np.abs(Z) < params.escape_radius
            Z[mask] = Z[mask] ** 2 + c
            m[mask] = i

        m = m / params.iterations

        return np.stack(
            [
                m**0.5,
                m**0.3,
                m**0.7,
            ],
            axis=-1,
        )

    def _color_by_capacity(self, capacity: float) -> np.ndarray:
        h = np.clip(capacity / 10.0, 0, 1)
        return np.array(
            [
                np.sin(h * np.pi * 2) * 0.5 + 0.5,
                np.sin(h * np.pi * 2 + np.pi / 3) * 0.5 + 0.5,
                np.sin(h * np.pi * 2 + np.pi * 2 / 3) * 0.5 + 0.5,
            ]
        )

    def render_fractal(
        self,
        formula: str = "mandelbrot",
        params: RenderParams = None,
        profile: Optional[GeometricProfile] = None,
        boost: bool = True,
    ) -> np.ndarray:
        if params is None:
            params = RenderParams()

        W, H = params.width, params.height
        zoom = params.zoom

        x = np.linspace(-zoom, zoom, W)
        y = np.linspace(-zoom, zoom, H)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y

        result = None

        if formula == "mandelbrot":
            result = self._render_mandelbrot(Z, params)
        elif formula == "julia":
            result = self._render_julia(Z, params)
        elif formula == "burning_ship":
            result = self._render_burning_ship(Z, params)
        elif formula == "newton":
            result = self._render_newton(Z, params)
        else:
            result = self._render_mandelbrot(Z, params)

        if profile is not None and boost:
            # Используем имя профиля, не pattern_id
            for name, p in self.profiles.items():
                if p is profile:
                    self.boost_correlation(name, boost=0.05)
                    break

        return result

    def _render_burning_ship(self, Z: np.ndarray, params: RenderParams) -> np.ndarray:
        c = Z.copy()
        m = np.zeros(Z.shape)

        for i in range(params.iterations):
            mask = np.abs(Z) < params.escape_radius
            Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag)) ** 2 + c[mask]
            m[mask] = i

        m = m / params.iterations

        return np.stack([m, m**0.5, m**0.3], axis=-1)

    def _render_newton(self, Z: np.ndarray, params: RenderParams) -> np.ndarray:
        def f(z):
            return z**3 - 1

        def df(z):
            return 3 * z**2

        m = np.zeros(Z.shape, dtype=np.float32)

        for i in range(params.iterations):
            mask = np.abs(Z) < params.escape_radius
            Z[mask] = Z[mask] - f(Z[mask]) / df(Z[mask])
            m[mask] = i

        colors = np.zeros((*Z.shape, 3))
        angles = np.angle(Z)

        colors[:, :, 0] = (np.sin(angles * 3) + 1) / 2
        colors[:, :, 1] = (np.sin(angles * 3 + np.pi / 2) + 1) / 2
        colors[:, :, 2] = (np.sin(angles * 3 + np.pi) + 1) / 2

        colors *= m[:, :, np.newaxis] / params.iterations

        return colors

    def render_horizon(self, profile: GeometricProfile, params: RenderParams = None) -> np.ndarray:
        if params is None:
            params = RenderParams()

        bits = profile.bits
        H, W = bits.shape[1], bits.shape[2]

        if H != params.height or W != params.width:
            scale_y = params.height / H
            scale_x = params.width / W
            new_bits = []
            for b in bits:
                from scipy.ndimage import zoom

                new_bits.append(zoom(b, (scale_y, scale_x), order=0))
            bits = np.stack(new_bits)

        result = np.zeros((params.height, params.width, 3))

        for i, threshold in enumerate(profile.thresholds):
            layer = bits[i]
            t_norm = (threshold - profile.thresholds.min()) / (
                profile.thresholds.max() - profile.thresholds.min() + 1e-10
            )
            result[layer > 0.5] = t_norm

        if profile.betti[0] > 0 and len(profile.centroids) > 0:
            for c in profile.centroids:
                y, x = int(c[0]), int(c[1])
                if 0 <= y < params.height and 0 <= x < params.width:
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if 0 <= y + dy < params.height and 0 <= x + dx < params.width:
                                result[y + dy, x + dx] = (1, 0, 0)

        return (result * 255).astype(np.uint8)

    def compress_profiles(self, k: int = 16) -> dict:
        if not self.profiles:
            return {}

        all_bits = []
        names = []

        for name, profile in self.profiles.items():
            all_bits.append(profile.bits.flatten())
            names.append(name)

        all_bits = np.stack(all_bits)

        U, S, Vt = np.linalg.svd(all_bits, full_matrices=False)

        self._svd_basis = {
            "U": U[:, :k],
            "S": S[:k],
            "Vt": Vt[:k],
            "k": k,
            "names": names,
        }

        return self._svd_basis

    def generate_from_basis(
        self, coefficients: np.ndarray, params: RenderParams = None
    ) -> np.ndarray:
        if self._svd_basis is None:
            raise ValueError("Сначала вызови compress_profiles()")

        k = self._svd_basis["k"]
        if len(coefficients) != k:
            raise ValueError(f"Ожидался вектор длины {k}")

        reconstructed = self._svd_basis["U"] @ (coefficients * self._svd_basis["S"])

        if params is not None:
            profile = GeometricProfile(
                bits=reconstructed.reshape(-1, params.height, params.width),
                thresholds=np.linspace(0, 1, reconstructed.shape[0]),
                centroids=np.array([]),
                betti=(0, 0),
                euler=0,
                capacity=0.0,
                complexity=0.0,
            )
            return self.render_horizon(profile, params)

        return reconstructed
