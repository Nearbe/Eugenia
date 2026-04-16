#!/usr/bin/env python3
"""
EUGENIA Unified System
======================

Объединяет:
- Model Pattern Extractor (веса → паттерны)
- Geometric Engine (генерация из паттернов)
- Duality System (DET/RND как одно целое)

111GB весов → ~1GB паттернов → генерация в рантайме
"""

import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
from enum import Enum

from core.division import div_safe, safe_divide
from eugenia_graphics import GeometricEngine, GeometricProfile, RenderParams
from eugenia_model_patterns import ModelLoader, PatternExtractor, ModelProfile
from eugenia_duality import UnifiedSystem, DualState


class TaskMode(Enum):
    INFERENCE = "inference"  # Генерация (DET)
    EXPLORATION = "exploration"  # Исследование (RND)
    HYBRID = "hybrid"  # Баланс


@dataclass
class EugeniaState:
    """Состояние всей системы"""

    duality: DualState
    graphics_engine: GeometricEngine
    pattern_extractor: PatternExtractor
    loaded_profiles: Dict[str, ModelProfile]
    active_model: Optional[str]


class EugeniaUnified:
    """
    Единая система Eugenia

    Ключевые возможности:
    1. Загрузка моделей → извлечение паттернов
    2. Паттерны → геометрические профили
    3. Профили → генерация изображений
    4. Duality → управление режимом работы
    5. Runtime learning → усиление корреляций
    """

    def __init__(self, k: int = 16):
        self.k = k

        # Ядро
        self.graphics = GeometricEngine()
        self.extractor = PatternExtractor(k=k)
        self.duality = UnifiedSystem(balance=0.5)

        # Данные
        self.model_profiles: Dict[str, ModelProfile] = {}
        self.pattern_cache: Dict[str, GeometricProfile] = {}
        self.active_model: Optional[str] = None

        # Статистика
        self.stats = {
            "total_patterns": 0,
            "total_uses": 0,
            "compression_ratio": 0.0,
        }

    def load_model(self, model_path: str) -> bool:
        """Загружает модель и извлекает паттерны"""
        print(f"\n[Eugenia] Загрузка модели: {model_path}")

        loader = ModelLoader(str(Path(model_path).parent))
        layers = {}

        # Определяем формат
        ext = Path(model_path).suffix.lower()

        if ext == ".safetensors":
            layers = loader.load_safetensors(model_path)
        elif ext == ".npy":
            layers = {"layer_0": np.load(model_path)}
        else:
            print(f"  Формат {ext} не поддерживается напрямую")
            return False

        if not layers:
            print("  Не удалось загрузить слои")
            return False

        print(f"  Загружено слоёв: {len(layers)}")

        # SVD паттерны
        profiles = self.extractor.extract_all_layers(layers, k=self.k)
        self.model_profiles.update(profiles)

        # Регистрируем в graphics engine
        for name, profile in profiles.items():
            geo = self.extractor.get_pattern_geometry(profile)
            self.graphics.register_profile(name, self._profile_to_geo(profile))

        self.active_model = model_path
        self._update_stats()

        print(f"  Паттернов извлечено: {len(profiles)}")
        print(f"  Compression ratio: {self.stats['compression_ratio']:.4f}x")

        return True

    def _profile_to_geo(self, model_profile: ModelProfile) -> GeometricProfile:
        """Конвертирует ModelProfile в GeometricProfile"""

        shape = model_profile.original_shape

        # Создаём синтетический бинарный профиль из SVD
        S = model_profile.svd_S

        # normalization
        S_max = S.max()
        if S_max == 0:
            S_norm = np.zeros_like(S)
        else:
            S_norm = S / S_max

        # Create 2D representation of singular values
        H, W = shape[-2:]
        bits = np.zeros((len(S), H, W))

        for i, s in enumerate(S_norm):
            bits[i, : int(s * H), : int(s * W)] = 1.0

        # Compute information capacity
        S_sum = S.sum()
        capacity = float(S_sum / (len(S) + 1) if len(S) > 0 else 0.0)

        return GeometricProfile(
            bits=bits,
            thresholds=np.linspace(0, 1, len(S)),
            centroids=np.array([[H / 2, W / 2]]),
            betti=(int(S_sum > 0.5), 0),
            euler=1,
            capacity=capacity,
            complexity=float(S_norm[0] if len(S_norm) > 0 else 0),
        )

    def generate(
        self,
        prompt: str,
        mode: TaskMode = TaskMode.HYBRID,
        width: int = 512,
        height: int = 512,
        formula: str = "mandelbrot",
    ) -> np.ndarray:
        """
        Генерирует изображение из паттернов

        prompt: описание (влияет на параметры через duality)
        mode: INFERENCE/DET, EXPLORATION/RND, HYBRID
        """
        # Duality переход
        exploration_factor = 0.1 if mode == TaskMode.EXPLORATION else 0.01

        result, state = self.duality.transition(prompt, exploration_factor)

        # Параметры рендера
        params = RenderParams(
            width=width,
            height=height,
            zoom=1.0 + state.omega * 0.5,
            iterations=50 + int(state.pi * 50),
        )

        # Выбираем профиль
        if self.model_profiles:
            profile_name = list(self.model_profiles.keys())[0]
            model_profile = self.model_profiles[profile_name]
            geo_profile = self._profile_to_geo(model_profile)
        else:
            geo_profile = None

        # Рендер
        img = self.graphics.render_fractal(
            formula=formula,
            params=params,
            profile=geo_profile,
            boost=True,  # Усиливаем корреляции
        )

        self.stats["total_uses"] += 1

        return img

    def learn_from_feedback(self, success: bool, boost: float = 0.1):
        """Усиливает корреляции на основе фидбека"""

        # Duality обновление
        if success:
            new_balance = min(1.0, self.duality.state.pi * (1 + boost))
            self.duality.state = DualState(
                omega=1.0 - new_balance,
                pi=new_balance,
            )

        # Graphics корреляции
        for name in self.model_profiles.keys():
            self.graphics.boost_correlation(name, boost=boost)

        self._update_stats()

    def _update_stats(self):
        """Обновляет статистику"""
        self.stats["total_patterns"] = len(self.model_profiles)

        if self.model_profiles:
            ratios = [p.compression_ratio for p in self.model_profiles.values()]
            self.stats["compression_ratio"] = np.mean(ratios)

    def get_state(self) -> dict:
        """Возвращает текущее состояние системы"""
        return {
            "active_model": self.active_model,
            "patterns_loaded": len(self.model_profiles),
            "duality": {
                "omega": self.duality.state.omega,
                "pi": self.duality.state.pi,
                "delta": self.duality.state.delta,
                "mode": "DET"
                if self.duality.state.is_deterministic
                else ("RND" if self.duality.state.is_exploratory else "HYBRID"),
            },
            "graphics": {
                "correlations": {k: v["strength"] for k, v in self.graphics.correlations.items()},
            },
            "stats": self.stats,
        }


# ─────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────


def demo_unified():
    """Демонстрация объединённой системы"""
    print("=" * 60)
    print("EUGENIA UNIFIED SYSTEM")
    print("=" * 60)

    # Создаём систему
    eugenia = EugeniaUnified(k=16)

    # Тест генерации (без модели)
    print("\n1. Генерация (без модели):")
    img = eugenia.generate(
        prompt="тестовая генерация",
        mode=TaskMode.HYBRID,
        width=256,
        height=256,
    )
    print(f"   Результат: {img.shape}")

    # Тест симулированных весов
    print("\n2. SVD из весов:")
    np.random.seed(42)
    weights = np.random.randn(512, 2048)
    profile = eugenia.extractor.extract_from_weights(weights, "test_layer")
    geo = eugenia.extractor.get_pattern_geometry(profile)
    print(f"   Энтропия: {geo['entropy']:.2f}")
    print(f"   Сжатие: {geo['compression_ratio']:.4f}x")

    # Регистрируем
    eugenia.model_profiles["test"] = profile
    eugenia.graphics.register_profile("test", eugenia._profile_to_geo(profile))

    # Фидбек
    print("\n3. Runtime learning:")
    for i in range(5):
        eugenia.generate("запрос", mode=TaskMode.INFERENCE)
        eugenia.learn_from_feedback(success=True, boost=0.05)

    state = eugenia.get_state()
    print(f"   Паттернов: {state['patterns_loaded']}")
    print(f"   Duality: {state['duality']['mode']}, pi={state['duality']['pi']:.2f}")
    print(f"   Compression: {state['stats']['compression_ratio']:.4f}x")

    print("\n" + "=" * 60)
    print("АРХИТЕКТУРА:")
    print("=" * 60)
    print("""
    ┌─────────────────────────────────────────────┐
    │           EUGENIA UNIFIED                   │
    ├─────────────────────────────────────────────┤
    │  ┌─────────────┐    ┌─────────────┐        │
    │  │   Duality  │◄──►│   Graphics  │        │
    │  │  System    │    │   Engine    │        │
    │  └─────────────┘    └─────────────┘        │
    │         │                  │               │
    │         ▼                  ▼               │
    │  ┌─────────────────────────────────┐      │
    │  │     Pattern Extractor           │      │
    │  │  (SVD из весов моделей)         │      │
    │  └─────────────────────────────────┘      │
    │                    │                       │
    │                    ▼                       │
    │  ┌─────────────────────────────────┐      │
    │  │     Model Profiles               │      │
    │  │  111GB → ~1GB паттернов         │      │
    │  └─────────────────────────────────┘      │
    └─────────────────────────────────────────────┘
    
    Результат:
    - Веса моделей сжимаются в паттерны
    - Паттерны генерируют графику в рантайме
    - Duality управляет режимом (DET/RND)
    - Корреляции усиливаются при использовании
    """)
