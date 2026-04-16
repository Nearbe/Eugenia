import os
import sys

import pytest

# Добавляем директорию src в путь поиска модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from orchestrator import load_data, compute_sweep
from models.types import VisualizationData, SweepResults


def test_mnist_pipeline_components():
    """Интеграционный тест компонентов загрузки и обработки для MNIST."""
    # Проверяем наличие данных
    mnist_path = os.path.join(os.path.dirname(__file__), '..', '..', 'eugenia_data', 'mnist.npz')
    if not os.path.exists(mnist_path):
        pytest.skip("Файл данных MNIST не найден")

    # Настраиваем окружение
    os.environ['VIZ_SOURCE'] = 'mnist'

    # Тест загрузки
    data = load_data()
    assert isinstance(data, VisualizationData)
    assert data.number_of_classes == 10
    assert data.height == 28
    assert data.width == 28

    # Тест вычисления развертки
    sweep = compute_sweep()
    assert isinstance(sweep, SweepResults)
    assert len(sweep.thresholds) > 0
    assert sweep.occupancy_rates.shape[1] == 10


def test_png_pipeline_components():
    """Интеграционный тест для PNG (используя Eugene.jpeg из корня)."""
    # Проверяем наличие файла Eugene.jpeg в корне проекта
    root_dir = os.path.join(os.path.dirname(__file__), '..')
    img_path = os.path.join(root_dir, 'Eugene.jpeg')
    if not os.path.exists(img_path):
        pytest.skip("Eugene.jpeg не найден в корне проекта")

    # Сбрасываем кэш для корректной загрузки новых данных в рамках одного процесса
    import orchestrator
    orchestrator._cached_data = None
    orchestrator._cached_sweep = None

    os.environ['VIZ_SOURCE'] = 'png'
    os.environ['VIZ_SOURCE_FILE'] = 'Eugene.jpeg'

    data = load_data()
    assert isinstance(data, VisualizationData)
    # Eugene.jpeg скорее всего содержит один связный компонент (или несколько)
    assert data.number_of_classes >= 1
