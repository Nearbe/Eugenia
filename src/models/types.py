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
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

import numpy as np
import torch


@dataclass
class VisualizationData:
    """
    Контейнер для данных визуализации.
    Используется дата класс вместо словаря для лучшей типизации.
    """

    device: torch.device
    original_data: torch.Tensor
    delta_field: torch.Tensor
    labels: torch.Tensor
    height: int
    width: int
    channels: int
    number_of_classes: int
    symbol_delta_fields: List[torch.Tensor]
    is_color: bool
    color_space: str
    symbol_names: Optional[List[str]]
    delta_min: float
    delta_max: float
    config: Dict[str, Any]

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(f"VisualizationData has no attribute or key '{key}'")

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default


@dataclass
class SweepResults:
    """
    Контейнер для результатов алгоритма развертки.
    """

    thresholds: np.ndarray
    occupancy_rates: torch.Tensor
    jump_events: List[Any]
    jump_count: int

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(f"SweepResults has no attribute or key '{key}'")

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default
