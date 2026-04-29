"""
Model weight extractors — extract weights from model files (GGUF, etc.)

This package handles parsing of GGUF format and extracting weight tensors
for downstream pattern analysis (SVD, correlations).

Usage:
    # Extract weights directly
    from src.extractors import GGUFExtractor
    extractor = GGUFExtractor("model.gguf")
    weights = extractor.extract_tensor("layer.weight")

    # Extract correlations (SVD + correlation analysis)
    from src.extractors imports CorrelationExtractor
    extractor = CorrelationExtractor("model.gguf")
    report = extractor.extract_all()

    # Or convenience functions
    from src.extractors import extract_correlations, extract_spectrum
"""

from .gguf_extractor import GGUFExtractor
from .correlation_extractor import (
    CorrelationExtractor,
    WeightSpectrum,
    DeltaField,
    LayerCorrelation,
    CorrelationReport,
    extract_correlations,
    extract_spectrum,
)

__all__ = [
    "GGUFExtractor",
    "CorrelationExtractor",
    "WeightSpectrum",
    "DeltaField",
    "LayerCorrelation",
    "CorrelationReport",
    "extract_correlations",
    "extract_spectrum",
]
__version__ = "0.1.0"
