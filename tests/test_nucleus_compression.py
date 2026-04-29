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
from core.linear.linear_algebra import CoreMatrix
from nucleus.correlation_compressor import CorrelationCompressor


def test_correlation_compressor_decompresses_rectangular_shape():
    matrix = CoreMatrix([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    compressor = CorrelationCompressor()

    components = compressor.compress_correlation_svd(matrix, k=2)
    restored = compressor.decompress_correlation_svd()

    assert components["U"].shape == (2, 2)
    assert components["Vt"].shape == (2, 3)
    assert restored.shape == matrix.shape
