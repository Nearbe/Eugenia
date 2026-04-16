# Eugenia: Memory and Weights Storage Module

"""
Модуль для хранения памяти (states) и весов моделей в проекте Eugenia ML.

Архитектура: EUGENIA_ARCHITECTURE.md
Компрессия: COMPRESSION_SUMMARY.md
Протокол знаний: UNIVERSAL_KNOWLEDGE.md

Интегрируется с пайплайном топологического анализа изображений.
"""

from .eugenia_duality import DualState, UnifiedSystem
from .eugenia_graphics import GeometricEngine, GeometricProfile
from .eugenia_knowledge_system import GeometricExtractor, KnowledgeSystem
from .eugenia_model_patterns import ModelLoader, PatternExtractor
from .eugenia_seed_system import CorrelationEngine
# Экспорт ключевых компонентов
from .eugenia_unified import EugeniaUnified

__version__ = "0.1.0"
__all__ = [
    "EugeniaUnified", "GeometricEngine", "GeometricProfile",
    "DualState", "UnifiedSystem", "GeometricExtractor", "KnowledgeSystem",
    "ModelLoader", "PatternExtractor", "CorrelationEngine"
]
