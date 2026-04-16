"""
Nucleus - Deterministic Knowledge System

This package contains the core NUCLEUS modules:
- deterministic_core: Pattern-based knowledge representation
- universal_knowledge_map: Compressed knowledge storage (111GB → 50MB)
- nucleus_knowledge_system: Data absorption and generation
- knowledge_graph: Pattern graph with auto-connections
- geometric_extractor: BINARY SWEEP → TOPOLOGY
- correlation_compressor: SVD weight compression
- nucleus_seed_system: Correlation seed system
"""

from .deterministic_core import SemanticPattern, PatternRelationship, DeterministicKnowledgeCore
from .universal_knowledge_map import UniversalKnowledgeMap, KnowledgeNavigator
from .nucleus_knowledge_system import PatternNode, GeometricExtractor, KnowledgeSystem
from .knowledge_graph import KnowledgeGraph
from .correlation_compressor import CorrelationCompressor
from .nucleus_seed_system import Seed, CorrelationEngine, Explorer

__all__ = [
    # Deterministic Core
    "SemanticPattern",
    "PatternRelationship",
    "DeterministicKnowledgeCore",
    # Universal Knowledge Map
    "UniversalKnowledgeMap",
    "KnowledgeNavigator",
    # Knowledge System
    "PatternNode",
    "GeometricExtractor",
    "KnowledgeSystem",
    # Knowledge Graph
    "KnowledgeGraph",
    # Correlation Compressor
    "CorrelationCompressor",
    # Seed System
    "Seed",
    "CorrelationEngine",
    "Explorer",
]

__version__ = "0.1.0"
