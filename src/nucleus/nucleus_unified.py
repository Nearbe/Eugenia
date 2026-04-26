"""Compatibility exports for the unified Nucleus API."""

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
from __future__ import annotations

from .geometric_extractor import GeometricExtractor, GeometricFeatures
from .knowledge_graph import KnowledgeGraph
from .nucleus_knowledge_system import GeometricExtractor as SystemGeometricExtractor
from .nucleus_knowledge_system import KnowledgeSystem, PatternNode
from .nucleus_seed_system import CorrelationEngine, Explorer, Seed

__all__ = [
    "CorrelationEngine",
    "Explorer",
    "GeometricExtractor",
    "GeometricFeatures",
    "KnowledgeGraph",
    "KnowledgeSystem",
    "PatternNode",
    "Seed",
    "SystemGeometricExtractor",
]
