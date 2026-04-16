import os
import sys

import pytest
import torch

# Добавляем директорию src в путь поиска модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sweep import compute_sweep
from models import VisualizationData


def test_delta_field_math():
    """Проверка математической корректности преобразования дельта-поля."""
    # X в диапазоне [0, 255]
    X = torch.tensor([0.0, 127.5, 255.0])
    # D = log(X + 1) - log(256 - X)
    D = torch.log(X + 1.0) - torch.log(256.0 - X)

    # Средняя точка (127.5) должна быть 0
    assert torch.allclose(D[1], torch.tensor(0.0), atol=1e-5)

    # Граничные значения должны быть симметричны и выходить за пределы 5.545
    assert D[0] < -5.545
    assert D[2] > 5.545
    assert torch.abs(D[0] + D[2]) < 1e-5


@pytest.mark.parametrize("number_of_classes", [1, 3, 10])
def test_sweep_logic_structure(number_of_classes):
    """Проверка структуры результата алгоритма развертки."""
    device = torch.device("cpu")

    # Создаем фиктивные данные
    symbol_delta_fields = [torch.randn(28, 28) for _ in range(number_of_classes)]

    data = VisualizationData(
        device=device,
        original_data=torch.zeros(1),
        delta_field=torch.zeros(1),
        labels=torch.zeros(1),
        symbol_delta_fields=symbol_delta_fields,
        number_of_classes=number_of_classes,
        height=28,
        width=28,
        channels=1,
        is_color=False,
        color_space="Grayscale",
        symbol_names=None,
        delta_min=-5.0,
        delta_max=5.0,
        config={"jump_threshold": 1.0}
    )

    sweep = compute_sweep(data)

    assert hasattr(sweep, "thresholds")
    assert hasattr(sweep, "occupancy_rates")
    assert sweep.occupancy_rates.shape[1] == number_of_classes
    assert len(sweep.thresholds) == sweep.occupancy_rates.shape[0]


def test_sweep_occupancy_limits():
    """Проверка предельных значений заполненности при развертке."""
    device = torch.device("cpu")
    # Линейное распределение от min до max
    delta_field = torch.linspace(-5.6, 5.6, 100)

    data = VisualizationData(
        device=device,
        original_data=torch.zeros(1),
        delta_field=torch.zeros(1),
        labels=torch.zeros(1),
        symbol_delta_fields=[delta_field],
        number_of_classes=1,
        height=1,
        width=100,
        channels=1,
        is_color=False,
        color_space="Grayscale",
        symbol_names=None,
        delta_min=-5.6,
        delta_max=5.6,
        config={"jump_threshold": 1.0}
    )

    sweep = compute_sweep(data)
    rates = sweep.occupancy_rates[:, 0]

    # При минимальном пороге заполненность должна быть близка к 100%
    assert rates[0] >= 95.0
    # При максимальном пороге заполненность должна быть близка к 0%
    assert rates[-1] <= 5.0
    # Заполненность должна быть монотонно невозрастающей
    assert torch.all(rates[:-1] >= rates[1:])
