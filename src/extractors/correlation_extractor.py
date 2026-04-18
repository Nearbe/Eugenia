"""
Correlation Extractor — выжимка корреляций из весов модели.

Использует математику Universe:
- SVD для разложения весов (A = UΣV*)
- Корреляция Пирсона: ρ = Cov(X,Y) / (σ_X · σ_Y)
- Параметр Δ: Δ = ln(|Re|) - ln(|Im|) для анализа отклонения
- Спектральная теорема: A = UΛU* для эрмитовых матриц

Пайплайн:
  GGUF weights → NumPy arrays → SVD decomposition → correlation analysis
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from .gguf_extractor import GGUFExtractor


@dataclass
class WeightSpectrum:
    """Спектр весов — сингулярные значения + важность."""

    tensor_name: str
    shape: tuple[int, ...]
    dtype: np.dtype
    singular_values: np.ndarray  # Σ (сингулярные числа)
    energy: float = 0.0  # √(Σ σ_i²) — норма Фробениуса
    rank: int = 0  # число ненулевых сингулярных чисел
    condition_number: float = 0.0  # σ_max / σ_min

    @property
    def compression_ratio(self) -> float:
        """Сколько раз можно сжать через SVD (k/n)."""
        n = max(self.shape) if self.shape else 1
        return n / max(self.rank, 1)

    def top_k_energy_fraction(self, k: int = 32) -> float:
        """Доля энергии в top-k сингулярных числах."""
        if len(self.singular_values) == 0:
            return 0.0
        total_energy = np.sum(self.singular_values**2)
        top_k_energy = np.sum(self.singular_values[:k] ** 2)
        return float(top_k_energy / total_energy) if total_energy > 0 else 0.0


@dataclass
class DeltaField:
    """Delta-поле весов: Δ = ln(|w|+1) - log(max_w - |w|)."""

    tensor_name: str
    values: np.ndarray  # Δ для каждого веса
    mean_delta: float = 0.0
    std_delta: float = 0.0
    min_delta: float = 0.0
    max_delta: float = 0.0

    @classmethod
    def compute(cls, weights: np.ndarray, tensor_name: str = "") -> "DeltaField":
        """Вычислить delta-поле для весов."""
        abs_w = np.abs(weights)
        max_abs = np.max(abs_w) if abs_w.size > 0 else 1.0
        # Δ = log(|w| + 1) - log(max_w - |w|)
        delta = np.log(abs_w + 1.0) - np.log(max_abs - abs_w + 1e-15)
        return cls(
            tensor_name=tensor_name,
            values=delta.flatten(),
            mean_delta=float(np.mean(delta)),
            std_delta=float(np.std(delta)),
            min_delta=float(np.min(delta)),
            max_delta=float(np.max(delta)),
        )


@dataclass
class LayerCorrelation:
    """Корреляция между двумя весовыми матрицами."""

    layer_a: str
    layer_b: str
    pearson_r: float  # [-1, 1]
    spearman_rho: float  # ранговая корреляция
    delta_sync: float  # синхронизация Δ (0-1)
    energy_ratio: float  # отношение энергий

    def __str__(self) -> str:
        return (
            f"{self.layer_a} ↔ {self.layer_b}: "
            r"ρ={self.pearson_r:.4f}, τ={self.spearman_rho:.4f}, "
            f"Δ-синх={self.delta_sync:.4f}"
        )


@dataclass
class CorrelationReport:
    """Отчёт по корреляциям весов."""

    model_name: str = ""
    architecture: str = ""
    total_tensors: int = 0
    total_params: int = 0
    weight_spectra: list[WeightSpectrum] = field(default_factory=list)
    delta_fields: list[DeltaField] = field(default_factory=list)
    layer_correlations: list[LayerCorrelation] = field(default_factory=list)

    def summary(self) -> str:
        lines = [f"=== Correlation Report: {self.model_name} ==="]
        lines.append(f"Architecture: {self.architecture}")
        lines.append(f"Tensors: {self.total_tensors}, Params: {self.total_params:,}")
        lines.append("")

        # Weight spectra summary
        if self.weight_spectra:
            lines.append("--- Weight Spectra ---")
            for spec in self.weight_spectra[:10]:  # top 10
                lines.append(
                    f"  {spec.tensor_name}: "
                    f"σ₁={spec.singular_values[0]:.4f}, "
                    f"rank={spec.rank}, "
                    f"cond={spec.condition_number:.2f}, "
                    f"top32_energy={spec.top_k_energy_fraction(32):.4f}"
                )

        # Delta fields summary
        if self.delta_fields:
            lines.append("")
            lines.append("--- Delta Fields ---")
            for df in self.delta_fields[:10]:
                lines.append(
                    f"  {df.tensor_name}: "
                    f"mean={df.mean_delta:.4f}, "
                    f"std={df.std_delta:.4f}, "
                    f"[{df.min_delta:.2f}, {df.max_delta:.2f}]"
                )

        # Layer correlations summary
        if self.layer_correlations:
            lines.append("")
            lines.append("--- Layer Correlations ---")
            for corr in self.layer_correlations[:15]:
                lines.append(f"  {corr}")

        return "\n".join(lines)


class CorrelationExtractor:
    """Извлечение корреляций из весов модели.

    Пайплайн:
      1. Загрузка весов через GGUFExtractor
      2. SVD разложение каждой weight matrix
      3. Вычисление delta-поля для каждого тензора
      4. Вычисление корреляций между слоями

    Пример:
        extractor = CorrelationExtractor("path/to/model.gguf")
        report = extractor.extract_all()
        print(report.summary())

        # Или по паттерну:
        report = extractor.extract(pattern="*.q_proj.weight")

        # Или конкретный тензор:
        spectrum = extractor.extract_spectrum("model.layers.0.self_attn.q_proj.weight")
    """

    def __init__(self, gguf_path: str | Path) -> None:
        """Инициализация экстрактора.

        Args:
            gguf_path: Путь к GGUF файлу модели.
        """
        self._gguf = GGUFExtractor(gguf_path)

    @property
    def gguf(self) -> GGUFExtractor:
        """GGUF экстрактор для прямого доступа."""
        return self._gguf

    def get_model_info(self) -> dict[str, Any]:
        """Получить информацию о модели из GGUF."""
        return self._gguf.get_model_info()

    def get_weight_keys(self, pattern: str = "*.weight") -> list[str]:
        """Получить имена тензоров по паттерну."""
        return self._gguf.get_weight_keys(pattern)

    def extract_spectrum(self, tensor_name: str, k_max: int | None = None) -> WeightSpectrum:
        """Извлечь спектр весов (SVD) для одного тензора.

        Args:
            tensor_name: Имя тензора (например, "model.layers.0.self_attn.q_proj.weight").
            k_max: Максимальное число сингулярных чисел (ограничение памяти).

        Returns:
            WeightSpectrum с сингулярными значениями и метриками.

        Raises:
            ValueError: Если тензор не найден.
        """
        weights = self._gguf.extract_tensor(tensor_name)
        if weights is None:
            raise ValueError(f"Tensor not found: {tensor_name}")

        # SVD разложение
        try:
            U, sigma, Vt = np.linalg.svd(weights, full_matrices=False)
        except np.linalg.LinAlgError:
            # Fallback: if SVD fails, use zero spectrum
            sigma = np.zeros(min(weights.shape))

        # Ограничение k_max (для больших матриц)
        if k_max is not None and len(sigma) > k_max:
            sigma = sigma[:k_max]

        # Метрики
        energy = float(np.sqrt(np.sum(sigma**2))) if len(sigma) > 0 else 0.0
        nonzero = np.sum(np.abs(sigma) > 1e-10) if len(sigma) > 0 else 0
        cond = float(sigma[0] / sigma[-1]) if len(sigma) > 1 and sigma[-1] > 0 else float("inf")

        return WeightSpectrum(
            tensor_name=tensor_name,
            shape=weights.shape,
            dtype=weights.dtype,
            singular_values=sigma,
            energy=energy,
            rank=max(nonzero, 1),
            condition_number=cond if not math.isinf(cond) else 1e15,
        )

    def extract_delta_field(self, tensor_name: str) -> DeltaField:
        """Извлечь delta-поле для тензора.

        Args:
            tensor_name: Имя тензора.

        Returns:
            DeltaField с вычисленными Δ для каждого веса.
        """
        weights = self._gguf.extract_tensor(tensor_name)
        if weights is None:
            raise ValueError(f"Tensor not found: {tensor_name}")

        return DeltaField.compute(weights, tensor_name)

    def compute_pearson_correlation(self, name_a: str, name_b: str) -> float:
        """Вычислить корреляцию Пирсона между двумя тензорами.

        ρ = Σ(x_i - x̄)(y_i - ȳ) / (σ_x · σ_y)

        Args:
            name_a: Имя первого тензора.
            name_b: Имя второго тензора.

        Returns:
            Коэффициент корреляции [-1, 1].
        """
        a = self._gguf.extract_tensor(name_a)
        b = self._gguf.extract_tensor(name_b)

        if a is None or b is None:
            raise ValueError("One or both tensors not found")

        # Flatten to 1D vectors
        a_flat = a.flatten().astype(np.float64)
        b_flat = b.flatten().astype(np.float64)

        # Match lengths (take minimum)
        min_len = min(len(a_flat), len(b_flat))
        a_flat = a_flat[:min_len]
        b_flat = b_flat[:min_len]

        # Pearson correlation
        a_mean = np.mean(a_flat)
        b_mean = np.mean(b_flat)

        a_centered = a_flat - a_mean
        b_centered = b_flat - b_mean

        cov = np.sum(a_centered * b_centered)
        std_a = np.sqrt(np.sum(a_centered**2))
        std_b = np.sqrt(np.sum(b_centered**2))

        if std_a < 1e-15 or std_b < 1e-15:
            return 0.0

        rho = cov / (std_a * std_b)
        return float(np.clip(rho, -1.0, 1.0))

    def compute_spearman_correlation(self, name_a: str, name_b: str) -> float:
        """Вычислить ранговую корреляцию Спирмена.

        ρ = 1 - 6·Σd_i² / (n(n²-1))

        Args:
            name_a: Имя первого тензора.
            name_b: Имя второго тензора.

        Returns:
            Ранговая корреляция [-1, 1].
        """
        a = self._gguf.extract_tensor(name_a)
        b = self._gguf.extract_tensor(name_b)

        if a is None or b is None:
            raise ValueError("One or both tensors not found")

        a_flat = a.flatten().astype(np.float64)
        b_flat = b.flatten().astype(np.float64)

        min_len = min(len(a_flat), len(b_flat))
        a_flat = a_flat[:min_len]
        b_flat = b_flat[:min_len]

        # Rank transformation (ties handled by average rank)
        a_ranks = self._compute_ranks(a_flat)
        b_ranks = self._compute_ranks(b_flat)

        d_sq = (a_ranks - b_ranks) ** 2
        n = len(a_ranks)

        if n <= 1:
            return 0.0

        rho = 1.0 - (6.0 * np.sum(d_sq)) / (n * (n**2 - 1))
        return float(np.clip(rho, -1.0, 1.0))

    @staticmethod
    def _compute_ranks(values: np.ndarray) -> np.ndarray:
        """Compute ranks with average tie handling."""
        n = len(values)
        if n == 0:
            return np.array([])

        # Argsort gives indices that would sort the array
        sorted_indices = np.argsort(values)
        ranks = np.empty(n, dtype=np.float64)

        # Assign ranks (handling ties by average rank)
        i = 0
        while i < n:
            j = i
            # Find all elements with same value
            while j + 1 < n and values[sorted_indices[j + 1]] == values[sorted_indices[i]]:
                j += 1

            # Average rank for tied elements
            avg_rank = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[sorted_indices[k]] = avg_rank

            i = j + 1

        return ranks

    def compute_delta_sync(self, name_a: str, name_b: str) -> float:
        """Вычислить синхронизацию Δ между двумя тензорами.

        𝒮 = 1 - σ(Δ) · scale, где Δ — delta-поле каждого тензора.

        Args:
            name_a: Имя первого тензора.
            name_b: Имя второго тензора.

        Returns:
            Синхронизация [0, 1].
        """
        delta_a = self.extract_delta_field(name_a)
        delta_b = self.extract_delta_field(name_b)

        # Combine deltas (average of both tensors' delta fields)
        combined_delta = np.concatenate([delta_a.values, delta_b.values])

        # Standard deviation of Δ
        sigma_delta = np.std(combined_delta)

        # Scale factor (from Universe sync formula)
        scale = 0.05

        # Synchronization
        s = 1.0 - sigma_delta * scale
        return float(np.clip(s, 0.0, 1.0))

    def compute_layer_correlation(self, name_a: str, name_b: str) -> LayerCorrelation:
        """Вычислить полную корреляцию между двумя тензорами.

        Combines Pearson, Spearman, delta-sync, and energy ratio.

        Args:
            name_a: Имя первого тензора.
            name_b: Имя второго тензора.

        Returns:
            LayerCorrelation со всеми метриками.
        """
        pearson = self.compute_pearson_correlation(name_a, name_b)
        spearman = self.compute_spearman_correlation(name_a, name_b)
        delta_sync = self.compute_delta_sync(name_a, name_b)

        # Energy ratio (smaller / larger energy)
        spec_a = self.extract_spectrum(name_a)
        spec_b = self.extract_spectrum(name_b)

        energy_a = spec_a.energy
        energy_b = spec_b.energy

        max_energy = max(energy_a, energy_b)
        if max_energy > 0:
            energy_ratio = min(energy_a, energy_b) / max_energy
        else:
            energy_ratio = 1.0

        return LayerCorrelation(
            layer_a=name_a,
            layer_b=name_b,
            pearson_r=pearson,
            spearman_rho=spearman,
            delta_sync=delta_sync,
            energy_ratio=energy_ratio,
        )

    def extract_all(self, pattern: str = "*.weight", k_max: int | None = None) -> CorrelationReport:
        """Извлечь все корреляции для тензоров по паттерну.

        Args:
            pattern: Glob-паттерн для имён тензоров (default: *.weight).
            k_max: Ограничение SVD (для больших матриц).

        Returns:
            CorrelationReport со всеми метриками.
        """
        info = self._gguf.get_model_info()

        # Get matching tensor names
        tensor_names = self.get_weight_keys(pattern)

        report = CorrelationReport(
            model_name=str(info.get("general.name", "unknown")),
            architecture=str(info.get("general.architecture", "unknown")),
            total_tensors=len(tensor_names),
        )

        # Extract spectra and delta fields
        for name in tensor_names:
            try:
                spectrum = self.extract_spectrum(name, k_max)
                report.weight_spectra.append(spectrum)

                delta = self.extract_delta_field(name)
                report.delta_fields.append(delta)

                total_params = int(np.prod(spectrum.shape))
                report.total_params += total_params
            except Exception as e:
                print(f"Warning: failed to extract '{name}': {e}")

        # Compute pairwise correlations (adjacent layers only, to avoid O(n²))
        # Group tensors by layer prefix
        layer_groups: dict[str, list[str]] = {}
        for name in tensor_names:
            # Extract layer prefix (e.g., "model.layers.0." from "model.layers.0.self_attn.q_proj.weight")
            parts = name.split(".")
            if len(parts) >= 4:
                prefix = ".".join(parts[:4]) + "."
            else:
                prefix = name

            if prefix not in layer_groups:
                layer_groups[prefix] = []
            layer_groups[prefix].append(name)

        # Correlate adjacent layers and within same layer
        sorted_layers = sorted(layer_groups.keys())

        for i, layer_a in enumerate(sorted_layers):
            tensors_a = layer_groups[layer_a]

            # Within-layer correlations (first tensor only, to limit pairs)
            if len(tensors_a) > 1:
                for j in range(1, min(len(tensors_a), 3)):
                    try:
                        corr = self.compute_layer_correlation(tensors_a[0], tensors_a[j])
                        report.layer_correlations.append(corr)
                    except Exception:
                        pass

            # Cross-layer correlations (adjacent layers, first tensor each)
            if i > 0:
                layer_b = sorted_layers[i - 1]
                tensors_b = layer_groups[layer_b]

                try:
                    corr = self.compute_layer_correlation(tensors_a[0], tensors_b[0])
                    report.layer_correlations.append(corr)
                except Exception:
                    pass

            if i < len(sorted_layers) - 1:
                layer_c = sorted_layers[i + 1]
                tensors_c = layer_groups[layer_c]

                try:
                    corr = self.compute_layer_correlation(tensors_a[0], tensors_c[0])
                    report.layer_correlations.append(corr)
                except Exception:
                    pass

        return report


def extract_correlations(
    gguf_path: str | Path,
    pattern: str = "*.weight",
) -> CorrelationReport:
    """Convenience function to extract correlations from a GGUF file.

    Args:
        gguf_path: Path to GGUF model file.
        pattern: Glob pattern for tensor names (default: *.weight).

    Returns:
        CorrelationReport with all metrics.
    """
    extractor = CorrelationExtractor(gguf_path)
    return extractor.extract_all(pattern=pattern)


def extract_spectrum(
    gguf_path: str | Path,
    tensor_name: str,
) -> WeightSpectrum:
    """Quick helper to extract spectrum for a single tensor.

    Args:
        gguf_path: Path to GGUF file.
        tensor_name: Tensor name to extract.

    Returns:
        WeightSpectrum with SVD decomposition and metrics.
    """
    extractor = CorrelationExtractor(gguf_path)
    return extractor.extract_spectrum(tensor_name)
